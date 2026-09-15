import pytest

from cryptocore.cli_parser import parse_key


def test_valid_key():
    key_string = "000102030405060708090a0b0c0d0e0f"

    key = parse_key(key_string)

    assert isinstance(key, bytes)
    assert len(key) == 16


def test_invalid_key_length():
    with pytest.raises(ValueError):
        parse_key("001122")


def test_invalid_hex_key():
    with pytest.raises(ValueError):
        parse_key("this-is-not-hex")