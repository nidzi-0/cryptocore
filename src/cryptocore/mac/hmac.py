from cryptocore.hash.sha256 import (
    SHA256,
    process_block,
)


BLOCK_SIZE = 64
DIGEST_SIZE = 32

IPAD_BYTE = 0x36
OPAD_BYTE = 0x5C


def xor_bytes(
    first: bytes,
    second: bytes,
) -> bytes:
    if len(first) != len(second):
        raise ValueError(
            "Для XOR длины массивов "
            "должны совпадать."
        )

    return bytes(
        first_byte ^ second_byte
        for first_byte, second_byte
        in zip(first, second)
    )


def _hash_values_to_bytes(
    values: list[int],
) -> bytes:
    return b"".join(
        value.to_bytes(
            4,
            byteorder="big",
        )
        for value in values
    )


class HMACSHA256:
    def __init__(
        self,
        key: bytes,
    ):
        if not isinstance(
            key,
            bytes,
        ):
            raise TypeError(
                "Ключ HMAC должен быть "
                "байтовой строкой."
            )

        self._key = self._process_key(
            key
        )

        self._ipad = xor_bytes(
            self._key,
            bytes(
                [IPAD_BYTE]
                * BLOCK_SIZE
            ),
        )

        self._opad = xor_bytes(
            self._key,
            bytes(
                [OPAD_BYTE]
                * BLOCK_SIZE
            ),
        )

        self._inner_base = SHA256()
        self._inner_base.update(
            self._ipad
        )

        self._outer_base = SHA256()
        self._outer_base.update(
            self._opad
        )

        self._inner_hash = (
            self._inner_base.copy()
        )

    @staticmethod
    def _process_key(
        key: bytes,
    ) -> bytes:
        if len(key) > BLOCK_SIZE:
            hasher = SHA256()

            hasher.update(
                key
            )

            key = hasher.digest()

        if len(key) < BLOCK_SIZE:
            key = (
                key
                + b"\x00"
                * (
                    BLOCK_SIZE
                    - len(key)
                )
            )

        return key

    def update(
        self,
        data: bytes
        | bytearray
        | memoryview,
    ) -> "HMACSHA256":
        if not isinstance(
            data,
            (
                bytes,
                bytearray,
                memoryview,
            ),
        ):
            raise TypeError(
                "HMAC принимает только "
                "байтовые данные."
            )

        self._inner_hash.update(
            bytes(data)
        )

        return self

    def digest(self) -> bytes:
        inner_digest = (
            self._inner_hash.digest()
        )

        outer_hash = (
            self._outer_base.copy()
        )

        outer_hash.update(
            inner_digest
        )

        return outer_hash.digest()

    def hexdigest(self) -> str:
        return self.digest().hex()

    def digest_message(
        self,
        message: bytes
        | bytearray
        | memoryview,
    ) -> bytes:
        if not isinstance(
            message,
            (
                bytes,
                bytearray,
                memoryview,
            ),
        ):
            raise TypeError(
                "HMAC принимает только "
                "байтовые данные."
            )

        message = bytes(
            message
        )

        # Быстрый путь для коротких сообщений.
        #
        # После ipad уже обработано 64 байта.
        # Если сообщение <= 55 байт,
        # SHA-256 padding помещается ещё
        # ровно в один блок.
        if len(message) <= 55:
            total_length = (
                BLOCK_SIZE
                + len(message)
            )

            padding_length = (
                55
                - len(message)
            )

            inner_block = (
                message
                + b"\x80"
                + b"\x00"
                * padding_length
                + (
                    total_length * 8
                ).to_bytes(
                    8,
                    byteorder="big",
                )
            )

            inner_values = process_block(
                inner_block,
                self._inner_base
                ._hash_values,
            )

            inner_digest = (
                _hash_values_to_bytes(
                    inner_values
                )
            )

            # Outer HMAC всегда получает
            # SHA-256 digest длиной 32 байта.
            outer_total_length = (
                BLOCK_SIZE
                + DIGEST_SIZE
            )

            outer_block = (
                inner_digest
                + b"\x80"
                + b"\x00" * 23
                + (
                    outer_total_length * 8
                ).to_bytes(
                    8,
                    byteorder="big",
                )
            )

            outer_values = process_block(
                outer_block,
                self._outer_base
                ._hash_values,
            )

            return (
                _hash_values_to_bytes(
                    outer_values
                )
            )

        # Обычный путь для длинных сообщений.
        inner_hash = (
            self._inner_base.copy()
        )

        inner_hash.update(
            message
        )

        inner_digest = (
            inner_hash.digest()
        )

        outer_hash = (
            self._outer_base.copy()
        )

        outer_hash.update(
            inner_digest
        )

        return outer_hash.digest()

    def compute(
        self,
        message: bytes
        | bytearray
        | memoryview,
    ) -> str:
        return self.digest_message(
            message
        ).hex()