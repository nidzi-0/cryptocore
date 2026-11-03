import hashlib

import pytest

from cryptocore.hash.sha256 import (
    SHA256,
    process_block,
)


def test_sha256_empty_input():
    sha256 = SHA256()

    assert sha256.hexdigest() == (
        "e3b0c44298fc1c149afbf4c8996fb924"
        "27ae41e4649b934ca495991b7852b855"
    )


def test_sha256_abc():
    sha256 = SHA256()
    sha256.update(b"abc")

    assert sha256.hexdigest() == (
        "ba7816bf8f01cfea414140de5dae2223"
        "b00361a396177a9cb410ff61f20015ad"
    )


def test_sha256_long_known_vector():
    data = (
        b"abcdbcdecdefdefgefghfghighijhijk"
        b"ijkljklmklmnlmnomnopnopq"
    )

    assert SHA256.hash(data) == (
        "248d6a61d20638b8e5c026930c3e6039"
        "a33ce45964ff2167f6ecedd419db06c1"
    )


def test_sha256_incremental_update():
    sha256 = SHA256()

    sha256.update(b"Crypto")
    sha256.update(b"Core")
    sha256.update(b" Sprint 4")

    data = b"CryptoCore Sprint 4"

    assert sha256.hexdigest() == (
        hashlib.sha256(data).hexdigest()
    )


@pytest.mark.parametrize(
    "size",
    [
        1,
        55,
        56,
        63,
        64,
        65,
        127,
        128,
        129,
        1000,
        8192,
    ],
)
def test_sha256_various_lengths(size):
    data = bytes(
        index % 256
        for index in range(size)
    )

    assert SHA256.hash(data) == (
        hashlib.sha256(data).hexdigest()
    )


def test_sha256_digest_is_repeatable():
    sha256 = SHA256()
    sha256.update(b"abc")

    first = sha256.hexdigest()
    second = sha256.hexdigest()

    assert first == second


def test_sha256_can_continue_after_digest():
    sha256 = SHA256()

    sha256.update(b"abc")

    assert sha256.hexdigest() == (
        hashlib.sha256(b"abc").hexdigest()
    )

    sha256.update(b"def")

    assert sha256.hexdigest() == (
        hashlib.sha256(b"abcdef").hexdigest()
    )


def test_sha256_rejects_non_bytes():
    sha256 = SHA256()

    with pytest.raises(TypeError):
        sha256.update("abc")


def test_process_block_rejects_wrong_size():
    with pytest.raises(ValueError):
        process_block(
            b"too short",
            [0] * 8,
        )