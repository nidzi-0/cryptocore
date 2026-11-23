import pytest

from cryptocore.kdf.hkdf import (
    derive_key,
)


MASTER_KEY = bytes.fromhex(
    "0011223344556677"
    "8899aabbccddeeff"
    "0011223344556677"
    "8899aabbccddeeff"
)


def test_derive_key_is_deterministic():
    first = derive_key(
        master_key=MASTER_KEY,
        context="encryption",
        length=32,
    )

    second = derive_key(
        master_key=MASTER_KEY,
        context="encryption",
        length=32,
    )

    assert first == second


def test_context_separation():
    encryption_key = derive_key(
        master_key=MASTER_KEY,
        context="encryption",
        length=32,
    )

    authentication_key = derive_key(
        master_key=MASTER_KEY,
        context="authentication",
        length=32,
    )

    assert (
        encryption_key
        != authentication_key
    )


@pytest.mark.parametrize(
    "length",
    [
        1,
        16,
        32,
        33,
        64,
        100,
    ],
)
def test_derive_key_length(
    length,
):
    result = derive_key(
        master_key=MASTER_KEY,
        context="test-context",
        length=length,
    )

    assert len(result) == length


def test_different_master_keys_produce_different_keys():
    first = derive_key(
        master_key=b"A" * 32,
        context="encryption",
        length=32,
    )

    second = derive_key(
        master_key=b"B" * 32,
        context="encryption",
        length=32,
    )

    assert first != second


def test_empty_context_rejected():
    with pytest.raises(
        ValueError,
        match="Context",
    ):
        derive_key(
            master_key=MASTER_KEY,
            context="",
            length=32,
        )


def test_invalid_length_rejected():
    with pytest.raises(
        ValueError,
        match="Длина ключа",
    ):
        derive_key(
            master_key=MASTER_KEY,
            context="encryption",
            length=0,
        )