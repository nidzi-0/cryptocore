import pytest

from cryptocore.padding import pad, unpad


def test_pad_short_data():
    data = b"Hello"

    padded = pad(data)

    assert len(padded) == 16
    assert unpad(padded) == data


def test_pad_exact_block():
    data = b"A" * 16

    padded = pad(data)

    assert len(padded) == 32
    assert unpad(padded) == data


def test_pad_multiple_blocks():
    data = b"B" * 40

    padded = pad(data)

    assert len(padded) % 16 == 0
    assert unpad(padded) == data


def test_unpad_empty_data():
    with pytest.raises(ValueError):
        unpad(b"")


def test_unpad_invalid_padding():
    invalid_data = b"1234567890123450"

    with pytest.raises(ValueError):
        unpad(invalid_data)