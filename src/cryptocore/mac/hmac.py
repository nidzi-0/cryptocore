from cryptocore.hash.sha256 import SHA256


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

        self._original_key = key

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

        self._inner_hash = SHA256()

        self._inner_hash.update(
            self._ipad
        )

    @staticmethod
    def _process_key(
        key: bytes,
    ) -> bytes:
        if len(key) > BLOCK_SIZE:
            hasher = SHA256()
            hasher.update(key)

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
        # H((K XOR ipad) || message)
        inner_digest = (
            self._inner_hash.digest()
        )

        # H((K XOR opad) || inner_hash)
        outer_hash = SHA256()

        outer_hash.update(
            self._opad
        )

        outer_hash.update(
            inner_digest
        )

        return outer_hash.digest()

    def hexdigest(self) -> str:
        return self.digest().hex()

    def compute(
        self,
        message: bytes
        | bytearray
        | memoryview,
    ) -> str:
        hmac = HMACSHA256(
            self._original_key
        )

        hmac.update(
            message
        )

        return hmac.hexdigest()