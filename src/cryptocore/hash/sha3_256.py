MASK_64 = 0xFFFFFFFFFFFFFFFF

RATE_BYTES = 136
DIGEST_SIZE = 32


ROUND_CONSTANTS = [
    0x0000000000000001,
    0x0000000000008082,
    0x800000000000808A,
    0x8000000080008000,
    0x000000000000808B,
    0x0000000080000001,
    0x8000000080008081,
    0x8000000000008009,
    0x000000000000008A,
    0x0000000000000088,
    0x0000000080008009,
    0x000000008000000A,
    0x000000008000808B,
    0x800000000000008B,
    0x8000000000008089,
    0x8000000000008003,
    0x8000000000008002,
    0x8000000000000080,
    0x000000000000800A,
    0x800000008000000A,
    0x8000000080008081,
    0x8000000000008080,
    0x0000000080000001,
    0x8000000080008008,
]


ROTATION_OFFSETS = [
    [0, 36, 3, 41, 18],
    [1, 44, 10, 45, 2],
    [62, 6, 43, 15, 61],
    [28, 55, 25, 21, 56],
    [27, 20, 39, 8, 14],
]


def rotate_left(
    value: int,
    amount: int,
) -> int:
    value &= MASK_64

    if amount == 0:
        return value

    return (
        (value << amount)
        | (value >> (64 - amount))
    ) & MASK_64


def keccak_f1600(
    state: list[int],
) -> list[int]:
    if len(state) != 25:
        raise ValueError(
            "Состояние Keccak-f[1600] "
            "должно содержать 25 элементов."
        )

    state = state.copy()

    for round_constant in ROUND_CONSTANTS:
        # Theta
        column_parity = [0] * 5

        for x in range(5):
            column_parity[x] = (
                state[x]
                ^ state[x + 5]
                ^ state[x + 10]
                ^ state[x + 15]
                ^ state[x + 20]
            )

        d = [0] * 5

        for x in range(5):
            d[x] = (
                column_parity[(x - 1) % 5]
                ^ rotate_left(
                    column_parity[(x + 1) % 5],
                    1,
                )
            )

        for x in range(5):
            for y in range(5):
                index = x + 5 * y

                state[index] = (
                    state[index] ^ d[x]
                ) & MASK_64

        # Rho + Pi
        temporary_state = [0] * 25

        for x in range(5):
            for y in range(5):
                source_index = x + 5 * y

                new_x = y
                new_y = (
                    2 * x + 3 * y
                ) % 5

                destination_index = (
                    new_x + 5 * new_y
                )

                temporary_state[
                    destination_index
                ] = rotate_left(
                    state[source_index],
                    ROTATION_OFFSETS[x][y],
                )

        # Chi
        for x in range(5):
            for y in range(5):
                index = x + 5 * y

                first = temporary_state[
                    ((x + 1) % 5)
                    + 5 * y
                ]

                second = temporary_state[
                    ((x + 2) % 5)
                    + 5 * y
                ]

                state[index] = (
                    temporary_state[index]
                    ^ ((~first) & second)
                ) & MASK_64

        # Iota
        state[0] ^= round_constant
        state[0] &= MASK_64

    return state


def absorb_block(
    state: list[int],
    block: bytes,
) -> list[int]:
    if len(block) != RATE_BYTES:
        raise ValueError(
            "Блок SHA3-256 должен иметь "
            "длину ровно 136 байт."
        )

    state = state.copy()

    lane_count = RATE_BYTES // 8

    for lane_index in range(lane_count):
        offset = lane_index * 8

        lane = int.from_bytes(
            block[offset:offset + 8],
            byteorder="little",
        )

        state[lane_index] ^= lane
        state[lane_index] &= MASK_64

    return keccak_f1600(state)


class SHA3_256:
    def __init__(self):
        self._state = [0] * 25
        self._buffer = bytearray()

    def update(
        self,
        data: bytes | bytearray | memoryview,
    ) -> "SHA3_256":
        if not isinstance(
            data,
            (bytes, bytearray, memoryview),
        ):
            raise TypeError(
                "SHA3-256 принимает только "
                "байтовые данные."
            )

        self._buffer.extend(bytes(data))

        while len(self._buffer) >= RATE_BYTES:
            block = bytes(
                self._buffer[:RATE_BYTES]
            )

            del self._buffer[:RATE_BYTES]

            self._state = absorb_block(
                self._state,
                block,
            )

        return self

    def _final_state(self) -> list[int]:
        state = self._state.copy()

        padded_data = bytearray(
            self._buffer
        )

        # Domain separation suffix SHA-3.
        padded_data.append(0x06)

        zero_count = (
            RATE_BYTES
            - (
                len(padded_data)
                % RATE_BYTES
            )
        ) % RATE_BYTES

        padded_data.extend(
            b"\x00" * zero_count
        )

        # Последний бит padding.
        padded_data[-1] |= 0x80

        for offset in range(
            0,
            len(padded_data),
            RATE_BYTES,
        ):
            block = bytes(
                padded_data[
                    offset:offset + RATE_BYTES
                ]
            )

            state = absorb_block(
                state,
                block,
            )

        return state

    def digest(self) -> bytes:
        state = self._final_state()

        output = bytearray()

        lane_count = RATE_BYTES // 8

        for lane_index in range(lane_count):
            output.extend(
                state[lane_index].to_bytes(
                    8,
                    byteorder="little",
                )
            )

            if len(output) >= DIGEST_SIZE:
                break

        return bytes(
            output[:DIGEST_SIZE]
        )

    def hexdigest(self) -> str:
        return self.digest().hex()

    @classmethod
    def hash(
        cls,
        data: bytes | bytearray | memoryview,
    ) -> str:
        sha3 = cls()
        sha3.update(data)

        return sha3.hexdigest()