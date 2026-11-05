from secrets import compare_digest

from Crypto.Cipher import AES

from .ecb import validate_key


BLOCK_SIZE = 16
NONCE_SIZE = 12
TAG_SIZE = 16

GF_R = (
    0xE1000000000000000000000000000000
)

COUNTER_MODULUS = 1 << 32


class AuthenticationError(ValueError):
    """Ошибка аутентификации AES-GCM."""

def _to_bytes(
    value,
    name: str,
) -> bytes:
    if not isinstance(
        value,
        (
            bytes,
            bytearray,
            memoryview,
        ),
    ):
        raise TypeError(
            f"{name} должен быть "
            "байтовой строкой."
        )

    return bytes(value)


def xor_bytes(
    first: bytes,
    second: bytes,
) -> bytes:
    if len(first) != len(second):
        raise ValueError(
            "Для XOR длины блоков "
            "должны совпадать."
        )

    return bytes(
        a ^ b
        for a, b
        in zip(first, second)
    )


def gf_multiply(
    x: int,
    y: int,
) -> int:

    if not isinstance(x, int):
        raise TypeError(
            "x должен быть целым числом."
        )

    if not isinstance(y, int):
        raise TypeError(
            "y должен быть целым числом."
        )

    if not 0 <= x < (1 << 128):
        raise ValueError(
            "x должен помещаться в 128 бит."
        )

    if not 0 <= y < (1 << 128):
        raise ValueError(
            "y должен помещаться в 128 бит."
        )

    z = 0
    v = y

    for bit_index in range(128):
        bit = (
            x
            >> (
                127
                - bit_index
            )
        ) & 1

        if bit:
            z ^= v

        if v & 1:
            v = (
                v >> 1
            ) ^ GF_R

        else:
            v >>= 1

    return z


def _ghash_blocks(
    state: int,
    hash_subkey: int,
    data: bytes,
) -> int:
    for offset in range(
        0,
        len(data),
        BLOCK_SIZE,
    ):
        block = data[
            offset:
            offset + BLOCK_SIZE
        ]

        if len(block) < BLOCK_SIZE:
            block = (
                block
                + b"\x00"
                * (
                    BLOCK_SIZE
                    - len(block)
                )
            )

        block_value = int.from_bytes(
            block,
            byteorder="big",
        )

        state = gf_multiply(
            state ^ block_value,
            hash_subkey,
        )

    return state


def ghash(
    hash_subkey: bytes,
    aad: bytes = b"",
    ciphertext: bytes = b"",
) -> bytes:
    hash_subkey = _to_bytes(
        hash_subkey,
        "Hash subkey",
    )

    aad = _to_bytes(
        aad,
        "AAD",
    )

    ciphertext = _to_bytes(
        ciphertext,
        "Ciphertext",
    )

    if len(hash_subkey) != BLOCK_SIZE:
        raise ValueError(
            "Hash subkey должен иметь "
            "длину 16 байт."
        )

    max_length = (
        ((1 << 64) - 1)
        // 8
    )

    if len(aad) > max_length:
        raise ValueError(
            "AAD слишком большой."
        )

    if len(ciphertext) > max_length:
        raise ValueError(
            "Ciphertext слишком большой."
        )

    h = int.from_bytes(
        hash_subkey,
        byteorder="big",
    )

    state = 0

    state = _ghash_blocks(
        state,
        h,
        aad,
    )

    state = _ghash_blocks(
        state,
        h,
        ciphertext,
    )

    length_block = (
        (
            len(aad) * 8
        ).to_bytes(
            8,
            byteorder="big",
        )
        + (
            len(ciphertext) * 8
        ).to_bytes(
            8,
            byteorder="big",
        )
    )

    state = _ghash_blocks(
        state,
        h,
        length_block,
    )

    return state.to_bytes(
        BLOCK_SIZE,
        byteorder="big",
    )


def increment_counter32(
    counter: bytes,
) -> bytes:

    counter = _to_bytes(
        counter,
        "Counter",
    )

    if len(counter) != BLOCK_SIZE:
        raise ValueError(
            "Счётчик должен иметь "
            "длину 16 байт."
        )

    prefix = counter[:12]

    value = int.from_bytes(
        counter[12:],
        byteorder="big",
    )

    value = (
        value + 1
    ) % COUNTER_MODULUS

    return (
        prefix
        + value.to_bytes(
            4,
            byteorder="big",
        )
    )


def _gctr(
    cipher,
    initial_counter: bytes,
    data: bytes,
) -> bytes:

    data = _to_bytes(
        data,
        "Data",
    )

    if not data:
        return b""

    block_count = (
        len(data)
        + BLOCK_SIZE
        - 1
    ) // BLOCK_SIZE

    if block_count >= COUNTER_MODULUS:
        raise ValueError(
            "Слишком большой объём "
            "данных для GCM counter."
        )

    counter = initial_counter

    result = []

    for offset in range(
        0,
        len(data),
        BLOCK_SIZE,
    ):
        block = data[
            offset:
            offset + BLOCK_SIZE
        ]

        keystream = cipher.encrypt(
            counter
        )

        encrypted_block = xor_bytes(
            block,
            keystream[
                :len(block)
            ],
        )

        result.append(
            encrypted_block
        )

        counter = increment_counter32(
            counter
        )

    return b"".join(
        result
    )


def _derive_j0(
    hash_subkey: bytes,
    nonce: bytes,
) -> bytes:


    nonce = _to_bytes(
        nonce,
        "Nonce",
    )

    if not nonce:
        raise ValueError(
            "Nonce не может быть пустым."
        )

    if len(nonce) == NONCE_SIZE:
        return (
            nonce
            + b"\x00\x00\x00\x01"
        )

    return ghash(
        hash_subkey,
        b"",
        nonce,
    )


class GCM:


    def __init__(
        self,
        key: bytes,
        nonce: bytes,
    ):
        key = _to_bytes(
            key,
            "Key",
        )

        nonce = _to_bytes(
            nonce,
            "Nonce",
        )

        validate_key(
            key
        )

        if not nonce:
            raise ValueError(
                "Nonce не может быть пустым."
            )

        self.key = key
        self.nonce = nonce

        self._cipher = AES.new(
            key,
            AES.MODE_ECB,
        )

        self._hash_subkey = (
            self._cipher.encrypt(
                b"\x00" * BLOCK_SIZE
            )
        )

        self._j0 = _derive_j0(
            self._hash_subkey,
            nonce,
        )

    def _authentication_tag(
        self,
        aad: bytes,
        ciphertext: bytes,
    ) -> bytes:
        authentication_data = ghash(
            self._hash_subkey,
            aad,
            ciphertext,
        )

        tag_mask = (
            self._cipher.encrypt(
                self._j0
            )
        )

        return xor_bytes(
            tag_mask,
            authentication_data,
        )

    def encrypt(
        self,
        plaintext: bytes,
        aad: bytes = b"",
    ) -> tuple[bytes, bytes]:
        plaintext = _to_bytes(
            plaintext,
            "Plaintext",
        )

        aad = _to_bytes(
            aad,
            "AAD",
        )

        initial_counter = (
            increment_counter32(
                self._j0
            )
        )

        ciphertext = _gctr(
            self._cipher,
            initial_counter,
            plaintext,
        )

        tag = self._authentication_tag(
            aad,
            ciphertext,
        )

        return (
            ciphertext,
            tag,
        )

    def decrypt(
        self,
        ciphertext: bytes,
        tag: bytes,
        aad: bytes = b"",
    ) -> bytes:
        ciphertext = _to_bytes(
            ciphertext,
            "Ciphertext",
        )

        tag = _to_bytes(
            tag,
            "Authentication tag",
        )

        aad = _to_bytes(
            aad,
            "AAD",
        )

        if len(tag) != TAG_SIZE:
            raise AuthenticationError(
                "Authentication failed: "
                "некорректная длина tag."
            )

        expected_tag = (
            self._authentication_tag(
                aad,
                ciphertext,
            )
        )

        # ВАЖНО:
        # plaintext вычисляется только
        # после успешной проверки tag.
        if not compare_digest(
            tag,
            expected_tag,
        ):
            raise AuthenticationError(
                "Authentication failed: "
                "AAD mismatch or "
                "ciphertext/tag tampered."
            )

        initial_counter = (
            increment_counter32(
                self._j0
            )
        )

        return _gctr(
            self._cipher,
            initial_counter,
            ciphertext,
        )


def encrypt_gcm(
    data: bytes,
    key: bytes,
    nonce: bytes,
    aad: bytes = b"",
) -> tuple[bytes, bytes]:
    gcm = GCM(
        key,
        nonce,
    )

    return gcm.encrypt(
        data,
        aad,
    )


def decrypt_gcm(
    data: bytes,
    tag: bytes,
    key: bytes,
    nonce: bytes,
    aad: bytes = b"",
) -> bytes:
    gcm = GCM(
        key,
        nonce,
    )

    return gcm.decrypt(
        data,
        tag,
        aad,
    )