from cryptocore import digest


ONE_GIB = 1024 * 1024 * 1024

TEST_SIZE = ONE_GIB + 1


class VirtualLargeStream:
    """
    Виртуальный поток размером больше 1 GiB.

    В памяти одновременно находится не более
    одного небольшого chunk.
    """

    def __init__(self, size: int):
        self.remaining = size
        self.total_read = 0
        self.max_requested_size = 0

    def read(self, size: int) -> bytes:
        self.max_requested_size = max(
            self.max_requested_size,
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

        return b"\x00" * amount


class CountingHasher:
    """
    Тестовый hasher.

    Здесь нам важно проверить именно файловый
    streaming-код CryptoCore, а не повторно
    выполнять криптографические NIST-тесты.
    """

    def __init__(self):
        self.total_bytes = 0

    def update(self, data: bytes):
        self.total_bytes += len(data)
        return self

    def hexdigest(self) -> str:
        return format(
            self.total_bytes,
            "x",
        )


def test_hash_stream_handles_more_than_1_gib(
    monkeypatch,
):
    stream = VirtualLargeStream(
        TEST_SIZE
    )

    monkeypatch.setitem(
        digest.HASH_ALGORITHMS,
        "counting-test",
        CountingHasher,
    )

    result = digest.hash_stream(
        stream,
        "counting-test",
    )

    assert stream.total_read == TEST_SIZE

    assert stream.remaining == 0

    assert (
        stream.max_requested_size
        == digest.CHUNK_SIZE
    )

    assert result == format(
        TEST_SIZE,
        "x",
    )


def test_large_stream_is_processed_in_chunks(
    monkeypatch,
):
    stream = VirtualLargeStream(
        TEST_SIZE
    )

    monkeypatch.setitem(
        digest.HASH_ALGORITHMS,
        "counting-test",
        CountingHasher,
    )

    digest.hash_stream(
        stream,
        "counting-test",
    )

    assert digest.CHUNK_SIZE == 8192

    assert (
        stream.max_requested_size
        <= digest.CHUNK_SIZE
    )