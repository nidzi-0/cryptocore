import hashlib

import pytest

from cryptocore.hash.sha3_256 import (
    SHA3_256,
    absorb_block,
    keccak_f1600,
)


def test_sha3_256_empty_input():
    sha3 = SHA3_256()

    assert sha3.hexdigest() == (
        "a7ffc6f8bf1ed76651c14756a061d662"
        "f580ff4de43b49fa82d80a4b80f8434a"
    )


def test_sha3_256_abc():
    sha3 = SHA3_256()
    sha3.update(b"abc")

    assert sha3.hexdigest() == (
        "3a985da74fe225b2045c172d6bd390bd"
        "855f086e3e9d525b46bfe24511431532"
    )


def test_sha3_256_long_known_vector():
    data = (
        b"abcdbcdecdefdefgefghfghighijhijk"
        b"ijkljklmklmnlmnomnopnopq"
    )

    assert SHA3_256.hash(data) == (
        "41c0dba2a9d6240849100376a8235e2c"
        "82e1b9998a999e21db32dd97496d3376"
    )


def test_sha3_256_incremental_update():
    sha3 = SHA3_256()

    sha3.update(b"Crypto")
    sha3.update(b"Core")
    sha3.update(b" Sprint 4")

    data = b"CryptoCore Sprint 4"

    assert sha3.hexdigest() == (
        hashlib.sha3_256(data).hexdigest()
    )


@pytest.mark.parametrize(
    "size",
    [
        1,
        10,
        135,
        136,
        137,
        271,
        272,
        273,
        1000,
        8192,
    ],
)
def test_sha3_256_various_lengths(size):
    data = bytes(
        index % 256
        for index in range(size)
    )

    expected = hashlib.sha3_256(
        data
    ).hexdigest()

    assert SHA3_256.hash(data) == expected


def test_sha3_256_digest_is_repeatable():
    sha3 = SHA3_256()
    sha3.update(b"abc")

    first = sha3.hexdigest()
    second = sha3.hexdigest()

    assert first == second


def test_sha3_256_can_continue_after_digest():
    sha3 = SHA3_256()

    sha3.update(b"abc")

    assert sha3.hexdigest() == (
        hashlib.sha3_256(
            b"abc"
        ).hexdigest()
    )

    sha3.update(b"def")

    assert sha3.hexdigest() == (
        hashlib.sha3_256(
            b"abcdef"
        ).hexdigest()
    )


def test_sha3_256_rejects_non_bytes():
    sha3 = SHA3_256()

    with pytest.raises(TypeError):
        sha3.update("abc")


def test_keccak_rejects_wrong_state_size():
    with pytest.raises(ValueError):
        keccak_f1600([0] * 24)


def test_absorb_rejects_wrong_block_size():
    with pytest.raises(ValueError):
        absorb_block(
            [0] * 25,
            b"short",
        )