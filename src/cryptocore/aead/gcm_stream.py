from secrets import compare_digest

from Crypto.Cipher import AES

from cryptocore.modes.ecb import validate_key
from cryptocore.modes.gcm import (
    AuthenticationError,
    BLOCK_SIZE,
    TAG_SIZE,
    _derive_j0,
    _gctr,
    gf_multiply,
    increment_counter32,
    xor_bytes,
)


DEFAULT_CHUNK_SIZE = 8192


def _process_full_blocks(
    state: int,
    hash_subkey: int,
    data: bytes,
) -> int:
    if len(data) % BLOCK_SIZE != 0:
        raise ValueError(
            "Размер блока GHASH должен "
            "быть кратен 16 байтам."
        )

    for offset in range(
        0,
        len(data),
        BLOCK_SIZE,
    ):
        block = data[
            offset:
            offset + BLOCK_SIZE
        ]

        block_value = int.from_bytes(
            block,
            byteorder="big",
        )

        state = gf_multiply(
            state ^ block_value,
            hash_subkey,
        )

    return state


def _finish_partial_block(
    state: int,
    hash_subkey: int,
    pending: bytes,
) -> int:
    if not pending:
        return state

    padded = (
        pending
        + b"\x00"
        * (
            BLOCK_SIZE
            - len(pending)
        )
    )

    return _process_full_blocks(
        state,
        hash_subkey,
        padded,
    )


def ghash_aad_stream(
    hash_subkey: bytes,
    aad_stream,
    ciphertext: bytes,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
) -> bytes:
    """
    GHASH с потоковой обработкой AAD.

    AAD читается небольшими блоками,
    поэтому полный AAD не требуется
    хранить в оперативной памяти.
    """

    if not isinstance(
        hash_subkey,
        bytes,
    ):
        raise TypeError(
            "Hash subkey должен быть bytes."
        )

    if len(hash_subkey) != BLOCK_SIZE:
        raise ValueError(
            "Hash subkey должен иметь "
            "длину 16 байт."
        )

    if not isinstance(
        ciphertext,
        bytes,
    ):
        raise TypeError(
            "Ciphertext должен быть bytes."
        )

    if (
        not isinstance(chunk_size, int)
        or chunk_size <= 0
    ):
        raise ValueError(
            "chunk_size должен быть "
            "положительным целым числом."
        )

    h = int.from_bytes(
        hash_subkey,
        byteorder="big",
    )

    state = 0
    aad_length = 0
    pending = b""

    while True:
        chunk = aad_stream.read(
            chunk_size
        )

        if not chunk:
            break

        if not isinstance(
            chunk,
            (
                bytes,
                bytearray,
                memoryview,
            ),
        ):
            raise TypeError(
                "AAD stream должен "
                "возвращать байтовые данные."
            )

        chunk = bytes(
            chunk
        )

        aad_length += len(
            chunk
        )

        combined = (
            pending
            + chunk
        )

        full_length = (
            len(combined)
            // BLOCK_SIZE
            * BLOCK_SIZE
        )

        if full_length:
            state = _process_full_blocks(
                state,
                h,
                combined[:full_length],
            )

        pending = (
            combined[full_length:]
        )

    state = _finish_partial_block(
        state,
        h,
        pending,
    )

    ciphertext_length = len(
        ciphertext
    )

    full_length = (
        ciphertext_length
        // BLOCK_SIZE
        * BLOCK_SIZE
    )

    if full_length:
        state = _process_full_blocks(
            state,
            h,
            ciphertext[:full_length],
        )

    remaining = (
        ciphertext[full_length:]
    )

    state = _finish_partial_block(
        state,
        h,
        remaining,
    )

    max_length = (
        ((1 << 64) - 1)
        // 8
    )

    if aad_length > max_length:
        raise ValueError(
            "AAD слишком большой."
        )

    if ciphertext_length > max_length:
        raise ValueError(
            "Ciphertext слишком большой."
        )

    length_block = (
        (
            aad_length * 8
        ).to_bytes(
            8,
            byteorder="big",
        )
        + (
            ciphertext_length * 8
        ).to_bytes(
            8,
            byteorder="big",
        )
    )

    state = _process_full_blocks(
        state,
        h,
        length_block,
    )

    return state.to_bytes(
        BLOCK_SIZE,
        byteorder="big",
    )


class GCMStreamingAAD:
    """
    AES-GCM с потоковым AAD.

    Plaintext/ciphertext остаётся обычным
    bytes-интерфейсом, а AAD читается
    через file-like stream по частям.
    """

    def __init__(
        self,
        key: bytes,
        nonce: bytes,
    ):
        validate_key(
            key
        )

        if not isinstance(
            nonce,
            bytes,
        ):
            raise TypeError(
                "Nonce должен быть bytes."
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

    def _tag(
        self,
        aad_stream,
        ciphertext: bytes,
        chunk_size: int,
    ) -> bytes:
        authentication_data = (
            ghash_aad_stream(
                self._hash_subkey,
                aad_stream,
                ciphertext,
                chunk_size,
            )
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
        aad_stream,
        chunk_size: int = DEFAULT_CHUNK_SIZE,
    ) -> tuple[bytes, bytes]:
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

        tag = self._tag(
            aad_stream,
            ciphertext,
            chunk_size,
        )

        return (
            ciphertext,
            tag,
        )

    def decrypt(
        self,
        ciphertext: bytes,
        tag: bytes,
        aad_stream,
        chunk_size: int = DEFAULT_CHUNK_SIZE,
    ) -> bytes:
        if len(tag) != TAG_SIZE:
            raise AuthenticationError(
                "Authentication failed: "
                "некорректная длина tag."
            )

        expected_tag = self._tag(
            aad_stream,
            ciphertext,
            chunk_size,
        )

        # Расшифрование выполняется
        # только после проверки tag.
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