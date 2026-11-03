MASK_32 = 0xFFFFFFFF
BLOCK_SIZE = 64
DIGEST_SIZE = 32


INITIAL_HASH_VALUES = [
    0x6A09E667,
    0xBB67AE85,
    0x3C6EF372,
    0xA54FF53A,
    0x510E527F,
    0x9B05688C,
    0x1F83D9AB,
    0x5BE0CD19,
]


ROUND_CONSTANTS = [
    0x428A2F98,
    0x71374491,
    0xB5C0FBCF,
    0xE9B5DBA5,
    0x3956C25B,
    0x59F111F1,
    0x923F82A4,
    0xAB1C5ED5,
    0xD807AA98,
    0x12835B01,
    0x243185BE,
    0x550C7DC3,
    0x72BE5D74,
    0x80DEB1FE,
    0x9BDC06A7,
    0xC19BF174,
    0xE49B69C1,
    0xEFBE4786,
    0x0FC19DC6,
    0x240CA1CC,
    0x2DE92C6F,
    0x4A7484AA,
    0x5CB0A9DC,
    0x76F988DA,
    0x983E5152,
    0xA831C66D,
    0xB00327C8,
    0xBF597FC7,
    0xC6E00BF3,
    0xD5A79147,
    0x06CA6351,
    0x14292967,
    0x27B70A85,
    0x2E1B2138,
    0x4D2C6DFC,
    0x53380D13,
    0x650A7354,
    0x766A0ABB,
    0x81C2C92E,
    0x92722C85,
    0xA2BFE8A1,
    0xA81A664B,
    0xC24B8B70,
    0xC76C51A3,
    0xD192E819,
    0xD6990624,
    0xF40E3585,
    0x106AA070,
    0x19A4C116,
    0x1E376C08,
    0x2748774C,
    0x34B0BCB5,
    0x391C0CB3,
    0x4ED8AA4A,
    0x5B9CCA4F,
    0x682E6FF3,
    0x748F82EE,
    0x78A5636F,
    0x84C87814,
    0x8CC70208,
    0x90BEFFFA,
    0xA4506CEB,
    0xBEF9A3F7,
    0xC67178F2,
]


def right_rotate(value: int, amount: int) -> int:
    value &= MASK_32

    return (
        (value >> amount)
        | (value << (32 - amount))
    ) & MASK_32


def choose(x: int, y: int, z: int) -> int:
    return (x & y) ^ ((~x) & z)


def majority(x: int, y: int, z: int) -> int:
    return (x & y) ^ (x & z) ^ (y & z)


def big_sigma_0(value: int) -> int:
    return (
        right_rotate(value, 2)
        ^ right_rotate(value, 13)
        ^ right_rotate(value, 22)
    )


def big_sigma_1(value: int) -> int:
    return (
        right_rotate(value, 6)
        ^ right_rotate(value, 11)
        ^ right_rotate(value, 25)
    )


def small_sigma_0(value: int) -> int:
    return (
        right_rotate(value, 7)
        ^ right_rotate(value, 18)
        ^ (value >> 3)
    )


def small_sigma_1(value: int) -> int:
    return (
        right_rotate(value, 17)
        ^ right_rotate(value, 19)
        ^ (value >> 10)
    )


def process_block(
    block: bytes,
    hash_values: list[int],
) -> list[int]:
    if len(block) != BLOCK_SIZE:
        raise ValueError(
            "Блок SHA-256 должен иметь длину "
            "ровно 64 байта."
        )

    words = []

    for offset in range(0, BLOCK_SIZE, 4):
        word = int.from_bytes(
            block[offset:offset + 4],
            byteorder="big",
        )
        words.append(word)

    for index in range(16, 64):
        new_word = (
            small_sigma_1(words[index - 2])
            + words[index - 7]
            + small_sigma_0(words[index - 15])
            + words[index - 16]
        ) & MASK_32

        words.append(new_word)

    (
        a,
        b,
        c,
        d,
        e,
        f,
        g,
        h,
    ) = hash_values

    for index in range(64):
        temp1 = (
            h
            + big_sigma_1(e)
            + choose(e, f, g)
            + ROUND_CONSTANTS[index]
            + words[index]
        ) & MASK_32

        temp2 = (
            big_sigma_0(a)
            + majority(a, b, c)
        ) & MASK_32

        h = g
        g = f
        f = e
        e = (d + temp1) & MASK_32
        d = c
        c = b
        b = a
        a = (temp1 + temp2) & MASK_32

    return [
        (hash_values[0] + a) & MASK_32,
        (hash_values[1] + b) & MASK_32,
        (hash_values[2] + c) & MASK_32,
        (hash_values[3] + d) & MASK_32,
        (hash_values[4] + e) & MASK_32,
        (hash_values[5] + f) & MASK_32,
        (hash_values[6] + g) & MASK_32,
        (hash_values[7] + h) & MASK_32,
    ]


class SHA256:
    def __init__(self):
        self._hash_values = INITIAL_HASH_VALUES.copy()
        self._buffer = bytearray()
        self._message_length = 0

    def update(
        self,
        data: bytes | bytearray | memoryview,
    ) -> "SHA256":
        if not isinstance(
            data,
            (bytes, bytearray, memoryview),
        ):
            raise TypeError(
                "SHA-256 принимает только байтовые данные."
            )

        data = bytes(data)

        self._message_length += len(data)
        self._buffer.extend(data)

        while len(self._buffer) >= BLOCK_SIZE:
            block = bytes(
                self._buffer[:BLOCK_SIZE]
            )

            del self._buffer[:BLOCK_SIZE]

            self._hash_values = process_block(
                block,
                self._hash_values,
            )

        return self

    def _final_hash_values(self) -> list[int]:
        hash_values = self._hash_values.copy()

        remaining_data = bytes(self._buffer)

        message_length_bits = (
            self._message_length * 8
        )

        padding = b"\x80"

        zero_padding_length = (
            56
            - (
                len(remaining_data)
                + len(padding)
            ) % BLOCK_SIZE
        ) % BLOCK_SIZE

        final_data = (
            remaining_data
            + padding
            + b"\x00" * zero_padding_length
            + message_length_bits.to_bytes(
                8,
                byteorder="big",
            )
        )

        for offset in range(
            0,
            len(final_data),
            BLOCK_SIZE,
        ):
            block = final_data[
                offset:offset + BLOCK_SIZE
            ]

            hash_values = process_block(
                block,
                hash_values,
            )

        return hash_values

    def digest(self) -> bytes:
        hash_values = self._final_hash_values()

        return b"".join(
            value.to_bytes(
                4,
                byteorder="big",
            )
            for value in hash_values
        )

    def hexdigest(self) -> str:
        return self.digest().hex()

    @classmethod
    def hash(
        cls,
        data: bytes | bytearray | memoryview,
    ) -> str:
        sha256 = cls()
        sha256.update(data)

        return sha256.hexdigest()