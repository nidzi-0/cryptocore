import pytest

from cryptocore.cli_parser import (
    get_arguments,
    parse_key,
)


def test_valid_key():
    key_string = (
        "000102030405060708090a0b0c0d0e0f"
    )

    key = parse_key(key_string)

    assert isinstance(key, bytes)
    assert len(key) == 16


def test_invalid_key_length():
    with pytest.raises(ValueError):
        parse_key("001122")


def test_invalid_hex_key():
    with pytest.raises(ValueError):
        parse_key("this-is-not-hex")


@pytest.mark.parametrize(
    "mode",
    [
        "ecb",
        "cbc",
        "cfb",
        "ofb",
        "ctr",
    ]
)
def test_supported_modes(mode):
    args = get_arguments([
        "--algorithm",
        "aes",
        "--mode",
        mode,
        "--encrypt",
        "--key",
        "000102030405060708090a0b0c0d0e0f",
        "--input",
        "input.bin",
    ])

    assert args.mode == mode


def test_iv_allowed_during_decryption():
    args = get_arguments([
        "--algorithm",
        "aes",
        "--mode",
        "cbc",
        "--decrypt",
        "--key",
        "000102030405060708090a0b0c0d0e0f",
        "--iv",
        "AABBCCDDEEFF00112233445566778899",
        "--input",
        "cipher.bin",
    ])

    assert args.iv == (
        "AABBCCDDEEFF00112233445566778899"
    )


def test_iv_rejected_during_encryption():
    with pytest.raises(SystemExit):
        get_arguments([
            "--algorithm",
            "aes",
            "--mode",
            "cbc",
            "--encrypt",
            "--key",
            "000102030405060708090a0b0c0d0e0f",
            "--iv",
            "AABBCCDDEEFF00112233445566778899",
            "--input",
            "input.bin",
        ])


def test_iv_rejected_for_ecb():
    with pytest.raises(SystemExit):
        get_arguments([
            "--algorithm",
            "aes",
            "--mode",
            "ecb",
            "--decrypt",
            "--key",
            "000102030405060708090a0b0c0d0e0f",
            "--iv",
            "AABBCCDDEEFF00112233445566778899",
            "--input",
            "cipher.bin",
        ])