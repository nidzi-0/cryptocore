import hashlib
from io import BytesIO

import pytest

from cryptocore.digest import (
    CHUNK_SIZE,
    format_digest_result,
    hash_file,
    hash_stream,
)


def test_hash_file_sha256(tmp_path):
    input_file = tmp_path / "test.bin"

    data = b"CryptoCore Sprint 4"

    input_file.write_bytes(data)

    result = hash_file(
        str(input_file),
        "sha256",
    )

    expected = hashlib.sha256(
        data
    ).hexdigest()

    assert result == expected


def test_hash_file_sha3_256(tmp_path):
    input_file = tmp_path / "test.bin"

    data = b"CryptoCore Sprint 4"

    input_file.write_bytes(data)

    result = hash_file(
        str(input_file),
        "sha3-256",
    )

    expected = hashlib.sha3_256(
        data
    ).hexdigest()

    assert result == expected


def test_empty_file_sha256(tmp_path):
    input_file = tmp_path / "empty.bin"

    input_file.write_bytes(b"")

    result = hash_file(
        str(input_file),
        "sha256",
    )

    assert result == (
        "e3b0c44298fc1c149afbf4c8996fb924"
        "27ae41e4649b934ca495991b7852b855"
    )


def test_empty_file_sha3_256(tmp_path):
    input_file = tmp_path / "empty.bin"

    input_file.write_bytes(b"")

    result = hash_file(
        str(input_file),
        "sha3-256",
    )

    assert result == (
        "a7ffc6f8bf1ed76651c14756a061d662"
        "f580ff4de43b49fa82d80a4b80f8434a"
    )


def test_hash_stream_large_data():
    data = (
        b"A"
        * (CHUNK_SIZE * 3 + 123)
    )

    stream = BytesIO(data)

    result = hash_stream(
        stream,
        "sha256",
    )

    expected = hashlib.sha256(
        data
    ).hexdigest()

    assert result == expected


def test_digest_output_format():
    digest_value = "abc123"

    result = format_digest_result(
        digest_value,
        "file.bin",
    )

    assert result == (
        "abc123  file.bin"
    )


def test_missing_file():
    with pytest.raises(
        FileNotFoundError
    ):
        hash_file(
            "definitely_missing_file.bin",
            "sha256",
        )


def test_directory_rejected(tmp_path):
    with pytest.raises(
        IsADirectoryError
    ):
        hash_file(
            str(tmp_path),
            "sha256",
        )


def test_unknown_algorithm():
    stream = BytesIO(b"data")

    with pytest.raises(ValueError):
        hash_stream(
            stream,
            "unknown",
        )