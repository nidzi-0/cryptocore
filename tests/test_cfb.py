import pytest

from cryptocore.modes.cfb import (
    encrypt_cfb,
    decrypt_cfb,
)


KEY = bytes.fromhex(
    "000102030405060708090a0b0c0d0e0f"
)

IV = bytes.fromhex(
    "AABBCCDDEEFF00112233445566778899"
)


def test_cfb_encrypt_decrypt_text():
    """ Проверяет шифрование и расшифрование текста. """
    data = b"Hello CryptoCore CFB!"

    encrypted = encrypt_cfb(data, KEY, IV)
    decrypted = decrypt_cfb(encrypted, KEY, IV)

    assert decrypted == data


def test_cfb_multiple_blocks():
    """ Проверяет обработку нескольких блоков. """
    data = b"A" * 100

    encrypted = encrypt_cfb(data, KEY, IV)
    decrypted = decrypt_cfb(encrypted, KEY, IV)

    assert decrypted == data
    assert len(encrypted) == len(data)


def test_cfb_partial_block():
    """ Проверяет последний неполный блок. """
    data = b"Hello"

    encrypted = encrypt_cfb(data, KEY, IV)
    decrypted = decrypt_cfb(encrypted, KEY, IV)

    assert len(encrypted) == 5
    assert decrypted == data


def test_cfb_exact_block():
    """ Проверяет данные размером ровно 16 байт. """
    data = b"A" * 16

    encrypted = encrypt_cfb(data, KEY, IV)
    decrypted = decrypt_cfb(encrypted, KEY, IV)

    assert len(encrypted) == 16
    assert decrypted == data


def test_cfb_binary_data():
    """ Проверяет работу с бинарными данными. """
    data = bytes(range(256))

    encrypted = encrypt_cfb(data, KEY, IV)
    decrypted = decrypt_cfb(encrypted, KEY, IV)

    assert decrypted == data
    assert len(encrypted) == len(data)


def test_cfb_empty_data():
    """ Проверяет обработку пустых данных. """
    data = b""

    encrypted = encrypt_cfb(data, KEY, IV)
    decrypted = decrypt_cfb(encrypted, KEY, IV)

    assert encrypted == b""
    assert decrypted == data


def test_cfb_invalid_key():
    """ Проверяет неправильную длину ключа. """
    with pytest.raises(ValueError):
        encrypt_cfb(
            data=b"Hello",
            key=b"12345",
            iv=IV
        )


def test_cfb_invalid_iv():
    """ Проверяет неправильную длину IV. """
    with pytest.raises(ValueError):
        encrypt_cfb(
            data=b"Hello",
            key=KEY,
            iv=b"12345"
        )


def test_cfb_known_vector():
    key = bytes.fromhex(
        "2b7e151628aed2a6abf7158809cf4f3c"
    )

    iv = bytes.fromhex(
        "000102030405060708090a0b0c0d0e0f"
    )

    plaintext = bytes.fromhex(
        "6bc1bee22e409f96e93d7e117393172a"
        "ae2d8a571e03ac9c9eb76fac45af8e51"
    )

    expected_ciphertext = bytes.fromhex(
        "3b3fd92eb72dad20333449f8e83cfb4a"
        "c8a64537a0b3a93fcde3cdad9f1ce58b"
    )

    encrypted = encrypt_cfb(
        plaintext,
        key,
        iv
    )

    decrypted = decrypt_cfb(
        expected_ciphertext,
        key,
        iv
    )

    assert encrypted == expected_ciphertext
    assert decrypted == plaintext