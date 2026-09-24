import pytest

from cryptocore.modes.ofb import (
    encrypt_ofb,
    decrypt_ofb,
)


KEY = bytes.fromhex(
    "000102030405060708090a0b0c0d0e0f"
)

IV = bytes.fromhex(
    "AABBCCDDEEFF00112233445566778899"
)


def test_ofb_encrypt_decrypt_text():
    """ Проверяет шифрование и расшифрование текста. """
    data = b"Hello CryptoCore OFB!"

    encrypted = encrypt_ofb(data, KEY, IV)
    decrypted = decrypt_ofb(encrypted, KEY, IV)

    assert decrypted == data


def test_ofb_multiple_blocks():
    """ Проверяет обработку нескольких блоков. """
    data = b"A" * 100

    encrypted = encrypt_ofb(data, KEY, IV)
    decrypted = decrypt_ofb(encrypted, KEY, IV)

    assert decrypted == data
    assert len(encrypted) == len(data)


def test_ofb_partial_block():
    """ Проверяет последний неполный блок. """
    data = b"Hello"

    encrypted = encrypt_ofb(data, KEY, IV)
    decrypted = decrypt_ofb(encrypted, KEY, IV)

    assert len(encrypted) == 5
    assert decrypted == data


def test_ofb_exact_block():
    """ Проверяет данные размером ровно 16 байт. """
    data = b"A" * 16

    encrypted = encrypt_ofb(data, KEY, IV)
    decrypted = decrypt_ofb(encrypted, KEY, IV)

    assert len(encrypted) == 16
    assert decrypted == data


def test_ofb_binary_data():
    """ Проверяет обработку бинарных данных. """
    data = bytes(range(256))

    encrypted = encrypt_ofb(data, KEY, IV)
    decrypted = decrypt_ofb(encrypted, KEY, IV)

    assert decrypted == data
    assert len(encrypted) == len(data)


def test_ofb_empty_data():
    """ Проверяет пустые данные. """
    data = b""

    encrypted = encrypt_ofb(data, KEY, IV)
    decrypted = decrypt_ofb(encrypted, KEY, IV)

    assert encrypted == b""
    assert decrypted == data


def test_ofb_invalid_key():
    """ Проверяет неправильную длину ключа. """
    with pytest.raises(ValueError):
        encrypt_ofb(
            data=b"Hello",
            key=b"12345",
            iv=IV
        )


def test_ofb_invalid_iv():
    """ Проверяет неправильную длину IV. """
    with pytest.raises(ValueError):
        encrypt_ofb(
            data=b"Hello",
            key=KEY,
            iv=b"12345"
        )


def test_ofb_invalid_iv_decryption():
    """ Проверяет IV при расшифровании. """
    with pytest.raises(ValueError):
        decrypt_ofb(
            data=b"Hello",
            key=KEY,
            iv=b"12345"
        )


def test_ofb_known_vector():
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
        "7789508d16918f03f53c52dac54ed825"
    )

    encrypted = encrypt_ofb(
        plaintext,
        key,
        iv
    )

    decrypted = decrypt_ofb(
        expected_ciphertext,
        key,
        iv
    )

    assert encrypted == expected_ciphertext
    assert decrypted == plaintext