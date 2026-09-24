from Crypto.Cipher import AES

from .cbc import xor_bytes, validate_iv
from .ecb import validate_key


BLOCK_SIZE = 16
COUNTER_MODULUS = 1 << 128


def increment_counter(counter: bytes) -> bytes:
    validate_iv(counter)

    # Преобразуем 16 байт в целое число.
    counter_value = int.from_bytes(
        counter,
        byteorder="big"
    )

    # Увеличиваем значение счётчика на единицу.
    counter_value = (
        counter_value + 1
    ) % COUNTER_MODULUS

    # Преобразуем число обратно в 16 байт.
    return counter_value.to_bytes(
        BLOCK_SIZE,
        byteorder="big"
    )


def process_ctr(
    data: bytes,
    key: bytes,
    iv: bytes
) -> bytes:
    validate_key(key)
    validate_iv(iv)

    # Используем AES для шифрования счётчика.
    cipher = AES.new(
        key,
        AES.MODE_ECB
    )

    result_blocks = []

    # Начальным значением счётчика является IV.
    counter = iv

    for offset in range(
        0,
        len(data),
        BLOCK_SIZE
    ):
        # Получаем очередной блок исходных данных.
        data_block = data[
            offset:offset + BLOCK_SIZE
        ]

        # Шифруем текущее значение счётчика.
        keystream = cipher.encrypt(counter)

        # Для неполного блока берём только нужные байты.
        keystream_block = keystream[:len(data_block)]

        # Выполняем XOR с исходными данными.
        result_block = xor_bytes(
            data_block,
            keystream_block
        )

        result_blocks.append(result_block)

        # Переходим к следующему значению счётчика.
        counter = increment_counter(counter)

    return b"".join(result_blocks)


def encrypt_ctr(
    data: bytes,
    key: bytes,
    iv: bytes
) -> bytes:
    """ Шифрует данные в режиме AES-128 CTR. """
    return process_ctr(data, key, iv)


def decrypt_ctr(
    data: bytes,
    key: bytes,
    iv: bytes
) -> bytes:
    """ Расшифровывает данные в режиме AES-128 CTR. """
    return process_ctr(data, key, iv)