import pytest

from cryptocore.main import (
    encrypt_data,
    decrypt_data,
)

from cryptocore.modes.cbc import encrypt_cbc
from cryptocore.modes.cfb import encrypt_cfb
from cryptocore.modes.ofb import encrypt_ofb
from cryptocore.modes.ctr import encrypt_ctr


KEY = bytes.fromhex(
    "000102030405060708090a0b0c0d0e0f"
)

IV = bytes.fromhex(
    "AABBCCDDEEFF00112233445566778899"
)


@pytest.mark.parametrize(
    "mode",
    [
        "cbc",
        "cfb",
        "ofb",
        "ctr",
    ]
)
def test_round_trip_with_iv_in_file(mode):
    data = (
        b"CryptoCore Sprint 2 integration test."
    )

    encrypted_file_data, iv = encrypt_data(
        data=data,
        key=KEY,
        mode=mode
    )

    assert iv is not None

    # Первые 16 байт файла должны содержать IV.
    assert encrypted_file_data[:16] == iv

    decrypted = decrypt_data(
        data=encrypted_file_data,
        key=KEY,
        mode=mode
    )

    assert decrypted == data


@pytest.mark.parametrize(
    "mode,encrypt_function",
    [
        ("cbc", encrypt_cbc),
        ("cfb", encrypt_cfb),
        ("ofb", encrypt_ofb),
        ("ctr", encrypt_ctr),
    ]
)
def test_decryption_with_explicit_iv(
    mode,
    encrypt_function
):
    data = b"External ciphertext test."

    ciphertext = encrypt_function(
        data=data,
        key=KEY,
        iv=IV
    )

    decrypted = decrypt_data(
        data=ciphertext,
        key=KEY,
        mode=mode,
        iv_string=IV.hex()
    )

    assert decrypted == data


@pytest.mark.parametrize(
    "mode",
    [
        "cbc",
        "cfb",
        "ofb",
        "ctr",
    ]
)
def test_too_short_file_without_iv(mode):
    with pytest.raises(ValueError):
        decrypt_data(
            data=b"short",
            key=KEY,
            mode=mode
        )


def test_ecb_still_works():
    data = b"Sprint 1 must continue working."

    encrypted, iv = encrypt_data(
        data=data,
        key=KEY,
        mode="ecb"
    )

    assert iv is None

    decrypted = decrypt_data(
        data=encrypted,
        key=KEY,
        mode="ecb"
    )

    assert decrypted == data
def test_generated_encryption_key(monkeypatch):
    from cryptocore.main import get_encryption_key

    expected_key = bytes.fromhex(
        "00112233445566778899AABBCCDDEEFF"
    )

    def fake_generate_random_bytes(num_bytes):
        assert num_bytes == 16
        return expected_key

    monkeypatch.setattr(
        "cryptocore.main.generate_random_bytes",
        fake_generate_random_bytes
    )

    key, generated = get_encryption_key(None)

    assert generated is True
    assert key == expected_key
    assert len(key) == 16


def test_user_key_is_not_replaced():
    from cryptocore.main import get_encryption_key

    key_hex = (
        "000102030405060708090A0B0C0D0E0F"
    )

    key, generated = get_encryption_key(
        key_hex
    )

    assert generated is False
    assert key == bytes.fromhex(key_hex)