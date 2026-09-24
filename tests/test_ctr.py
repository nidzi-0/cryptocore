import pytest

from cryptocore.modes.ctr import (
    encrypt_ctr,
    decrypt_ctr,
    increment_counter,
)


KEY = bytes.fromhex(
    "000102030405060708090a0b0c0d0e0f"
)

IV = bytes.fromhex(
    "AABBCCDDEEFF00112233445566778899"
)


def test_ctr_encrypt_decrypt_text():
    """ Проверяет шифрование и расшифрование текста. """
    data = b"Hello CryptoCore CTR!"

    encrypted = encrypt_ctr(data, KEY, IV)
    decrypted = decrypt_ctr(encrypted, KEY, IV)

    assert decrypted == data


def test_ctr_multiple_blocks():
    """ Проверяет обработку нескольких блоков. """
    data = b"A" * 100

    encrypted = encrypt_ctr(data, KEY, IV)
    decrypted = decrypt_ctr(encrypted, KEY, IV)

    assert decrypted == data
    assert len(encrypted) == len(data)


def test_ctr_partial_block():
    """ Проверяет последний неполный блок. """
    data = b"Hello"

    encrypted = encrypt_ctr(data, KEY, IV)
    decrypted = decrypt_ctr(encrypted, KEY, IV)

    assert len(encrypted) == 5
    assert decrypted == data


def test_ctr_exact_block():
    """ Проверяет данные размером ровно 16 байт. """
    data = b"A" * 16

    encrypted = encrypt_ctr(data, KEY, IV)
    decrypted = decrypt_ctr(encrypted, KEY, IV)

    assert len(encrypted) == 16
    assert decrypted == data


def test_ctr_binary_data():
    """ Проверяет обработку бинарных данных. """
    data = bytes(range(256))

    encrypted = encrypt_ctr(data, KEY, IV)
    decrypted = decrypt_ctr(encrypted, KEY, IV)

    assert decrypted == data
    assert len(encrypted) == len(data)


def test_ctr_empty_data():
    """ Проверяет обработку пустых данных. """
    data = b""

    encrypted = encrypt_ctr(data, KEY, IV)
    decrypted = decrypt_ctr(encrypted, KEY, IV)

    assert encrypted == b""
    assert decrypted == data


def test_ctr_invalid_key():
    """ Проверяет неправильную длину ключа. """
    with pytest.raises(ValueError):
        encrypt_ctr(
            data=b"Hello",
            key=b"12345",
            iv=IV
        )


def test_ctr_invalid_iv():
    """ Проверяет неправильную длину IV. """
    with pytest.raises(ValueError):
        encrypt_ctr(
            data=b"Hello",
            key=KEY,
            iv=b"12345"
        )


def test_increment_counter():
    """ Проверяет увеличение счётчика на единицу. """
    counter = bytes.fromhex(
        "00000000000000000000000000000001"
    )

    expected = bytes.fromhex(
        "00000000000000000000000000000002"
    )

    result = increment_counter(counter)

    assert result == expected


def test_increment_counter_carry():
    """ Проверяет перенос при увеличении счётчика. """
    counter = bytes.fromhex(
        "000000000000000000000000000000FF"
    )

    expected = bytes.fromhex(
        "00000000000000000000000000000100"
    )

    result = increment_counter(counter)

    assert result == expected


def test_increment_counter_overflow():
    """ Проверяет переполнение 128-битного счётчика. """
    counter = b"\xff" * 16

    result = increment_counter(counter)

    assert result == b"\x00" * 16


def test_ctr_known_vector():
    key = bytes.fromhex(
        "2b7e151628aed2a6abf7158809cf4f3c"
    )

    iv = bytes.fromhex(
        "f0f1f2f3f4f5f6f7f8f9fafbfcfdfeff"
    )

    plaintext = bytes.fromhex(
        "6bc1bee22e409f96e93d7e117393172a"
        "ae2d8a571e03ac9c9eb76fac45af8e51"
    )

    expected_ciphertext = bytes.fromhex(
        "874d6191b620e3261bef6864990db6ce"
        "9806f66b7970fdff8617187bb9fffdff"
    )

    encrypted = encrypt_ctr(
        plaintext,
        key,
        iv
    )

    decrypted = decrypt_ctr(
        expected_ciphertext,
        key,
        iv
    )

    assert encrypted == expected_ciphertext
    assert decrypted == plaintext