import pytest

from cryptocore.iv import (
    IV_SIZE,
    generate_iv,
    parse_iv,
    prepend_iv,
    split_iv,
)


def test_generate_iv():
    iv = generate_iv()

    assert isinstance(iv, bytes)
    assert len(iv) == IV_SIZE


def test_parse_valid_iv():
    iv_string = "AABBCCDDEEFF00112233445566778899"

    iv = parse_iv(iv_string)

    assert isinstance(iv, bytes)
    assert len(iv) == 16


def test_parse_invalid_hex_iv():
    with pytest.raises(ValueError):
        parse_iv("this-is-not-hex")


def test_parse_invalid_iv_length():
    with pytest.raises(ValueError):
        parse_iv("AABBCC")


def test_prepend_iv():
    iv = bytes.fromhex(
        "AABBCCDDEEFF00112233445566778899"
    )

    ciphertext = b"encrypted-data"

    result = prepend_iv(
        iv,
        ciphertext
    )

    assert result[:16] == iv
    assert result[16:] == ciphertext


def test_split_iv():
    iv = bytes.fromhex(
        "AABBCCDDEEFF00112233445566778899"
    )

    ciphertext = b"encrypted-data"

    data = iv + ciphertext

    extracted_iv, extracted_ciphertext = split_iv(data)

    assert extracted_iv == iv
    assert extracted_ciphertext == ciphertext


def test_split_too_short_file():
    data = b"short"

    with pytest.raises(ValueError):
        split_iv(data)