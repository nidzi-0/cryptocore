import pytest

from cryptocore.modes.ecb import encrypt_ecb, decrypt_ecb


KEY = bytes.fromhex(
    "000102030405060708090a0b0c0d0e0f"
)


def test_encrypt_decrypt_text():
    data = b"Hello CryptoCore!"

    encrypted = encrypt_ecb(data, KEY)
    decrypted = decrypt_ecb(encrypted, KEY)

    assert decrypted == data


def test_encrypt_decrypt_multiple_blocks():
    data = b"A" * 100

    encrypted = encrypt_ecb(data, KEY)
    decrypted = decrypt_ecb(encrypted, KEY)

    assert len(encrypted) % 16 == 0
    assert decrypted == data


def test_encrypt_decrypt_binary_data():
    data = bytes(range(256))

    encrypted = encrypt_ecb(data, KEY)
    decrypted = decrypt_ecb(encrypted, KEY)

    assert decrypted == data


def test_invalid_key_length():
    wrong_key = b"12345"

    with pytest.raises(ValueError):
        encrypt_ecb(b"Hello", wrong_key)


def test_invalid_ciphertext_length():
    with pytest.raises(ValueError):
        decrypt_ecb(b"12345", KEY)