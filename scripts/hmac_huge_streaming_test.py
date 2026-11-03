from cryptocore import digest


GIB = 1024 * 1024 * 1024

LOGICAL_SIZE = 20 * GIB + 123


class VirtualHugeFile:
    """
    иртуальный вход размером больше 20 GiB.
     памяти одновременно находится только один chunk.
    """

    def __init__(self, size: int):
        self.remaining = size
        self.total_read = 0
        self.max_read_size = 0
        self.chunk = b"\x00" * digest.CHUNK_SIZE

    def read(self, size: int) -> bytes:
        self.max_read_size = max(
            self.max_read_size,
            size,
        )

        if self.remaining == 0:
            return b""

        amount = min(
            size,
            self.remaining,
        )

        self.remaining -= amount
        self.total_read += amount

        if amount == len(self.chunk):
            return self.chunk

        return self.chunk[:amount]


class CountingHMAC:
    """
    Тестовое ядро для проверки только
    потоковой обработки больших данных.
    """

    def __init__(self, key: bytes):
        self.key = key
        self.total_bytes = 0

    def update(self, data: bytes):
        self.total_bytes += len(data)
        return self

    def hexdigest(self):
        return format(
            self.total_bytes,
            "x",
        )


def main() -> int:
    original_hmac = digest.HMACSHA256

    stream = VirtualHugeFile(
        LOGICAL_SIZE
    )

    key = bytes.fromhex(
        "00112233445566778899aabbccddeeff"
    )

    try:
        digest.HMACSHA256 = CountingHMAC

        result = digest.hmac_stream(
            stream,
            key,
        )

    finally:
        digest.HMACSHA256 = original_hmac

    expected = format(
        LOGICAL_SIZE,
        "x",
    )

    print(
        f"Logical input size: "
        f"{LOGICAL_SIZE:,} bytes"
    )

    print(
        f"Processed: "
        f"{stream.total_read:,} bytes"
    )

    print(
        f"Maximum read: "
        f"{stream.max_read_size} bytes"
    )

    if stream.total_read != LOGICAL_SIZE:
        print(
            "Huge HMAC streaming test: FAILED"
        )
        return 1

    if result != expected:
        print(
            "Huge HMAC streaming test: FAILED"
        )
        return 1

    if stream.max_read_size > digest.CHUNK_SIZE:
        print(
            "Huge HMAC streaming test: FAILED"
        )
        return 1

    print()
    print(
        "Huge HMAC streaming test: PASSED"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
