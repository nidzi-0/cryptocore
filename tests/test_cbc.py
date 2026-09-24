import pytest

from cryptocore.modes.cbc import (
    encrypt_cbc,
    decrypt_cbc,
)


KEY = bytes.fromhex(
    "000102030405060708090a0b0c0d0e0f"
)

IV = bytes.fromhex(
    "AABBCCDDEEFF00112233445566778899"
)


def test_cbc_encrypt_decrypt_text():
    data = b"Hello CryptoCore CBC!"

    encrypted = encrypt_cbc(
        data=data,
        key=KEY,
        iv=IV
    )

    decrypted = decrypt_cbc(
        data=encrypted,
        key=KEY,
        iv=IV
    )

    assert decrypted == data


def test_cbc_multiple_blocks():
    data = b"A" * 100

    encrypted = encrypt_cbc(
        data=data,
        key=KEY,
        iv=IV
    )

    decrypted = decrypt_cbc(
        data=encrypted,
        key=KEY,
        iv=IV
    )

    assert len(encrypted) % 16 == 0
    assert decrypted == data


def test_cbc_binary_data():
    data = bytes(range(256))

    encrypted = encrypt_cbc(
        data=data,
        key=KEY,
        iv=IV
    )

    decrypted = decrypt_cbc(
        data=encrypted,
        key=KEY,
        iv=IV
    )

    assert decrypted == data


def test_cbc_invalid_iv():
    invalid_iv = b"12345"

    with pytest.raises(ValueError):
        encrypt_cbc(
            data=b"Hello",
            key=KEY,
            iv=invalid_iv
        )


def test_cbc_invalid_ciphertext_length():
    with pytest.raises(ValueError):
        decrypt_cbc(
            data=b"12345",
            key=KEY,
            iv=IV
        )


def test_cbc_known_vector_first_block():
    key = bytes.fromhex(
        "2b7e151628aed2a6abf7158809cf4f3c"
    )

    iv = bytes.fromhex(
        "000102030405060708090a0b0c0d0e0f"
    )

    plaintext = bytes.fromhex(
        "6bc1bee22e409f96e93d7e117393172a"
    )

    expected_first_block = bytes.fromhex(
        "7649abac8119b246cee98e9b12e9197d"
    )

    encrypted = encrypt_cbc(
        data=plaintext,
        key=key,
        iv=iv
    )

    assert encrypted[:16] == expected_first_block