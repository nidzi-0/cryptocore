from Crypto.Cipher import AES

from .cbc import xor_bytes, validate_iv
from .ecb import validate_key


BLOCK_SIZE = 16


def process_ofb(data: bytes, key: bytes, iv: bytes) -> bytes:
    validate_key(key)
    validate_iv(iv)

    # Используем AES только для шифрования блоков.
    cipher = AES.new(key, AES.MODE_ECB)

    result_blocks = []

    # Первым входным блоком AES является IV.
    feedback = iv

    for offset in range(0, len(data), BLOCK_SIZE):
        data_block = data[offset:offset + BLOCK_SIZE]

        # Получаем следующий блок потока байтов.
        feedback = cipher.encrypt(feedback)

        # Для неполного блока берём только нужные байты.
        keystream = feedback[:len(data_block)]

        # Объединяем исходные данные с потоком через XOR.
        result_block = xor_bytes(data_block, keystream)

        result_blocks.append(result_block)

    return b"".join(result_blocks)


def encrypt_ofb(data: bytes, key: bytes, iv: bytes) -> bytes:
    """ Шифрует данные в режиме AES-128 OFB. """
    return process_ofb(data, key, iv)


def decrypt_ofb(data: bytes, key: bytes, iv: bytes) -> bytes:
    """ Расшифровывает данные в режиме AES-128 OFB. """
    return process_ofb(data, key, iv)