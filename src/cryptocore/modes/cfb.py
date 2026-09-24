from Crypto.Cipher import AES

from .cbc import xor_bytes, validate_iv
from .ecb import validate_key


BLOCK_SIZE = 16


def encrypt_cfb(data: bytes, key: bytes, iv: bytes) -> bytes:
    validate_key(key)
    validate_iv(iv)

    # Используем AES только для шифрования отдельных блоков.
    cipher = AES.new(key, AES.MODE_ECB)

    encrypted_blocks = []

    # Для первого блока используется IV.
    feedback = iv

    for offset in range(0, len(data), BLOCK_SIZE):
        plaintext_block = data[offset:offset + BLOCK_SIZE]

        # Шифруем IV или предыдущий блок шифротекста.
        encrypted_feedback = cipher.encrypt(feedback)

        # Выполняем XOR с открытым текстом.
        # Последний блок может быть короче 16 байт.
        ciphertext_block = xor_bytes(
            plaintext_block,
            encrypted_feedback[:len(plaintext_block)]
        )

        encrypted_blocks.append(ciphertext_block)

        # Следующий блок использует предыдущий шифротекст.
        # Обновление требуется только для полного блока.
        if len(ciphertext_block) == BLOCK_SIZE:
            feedback = ciphertext_block

    return b"".join(encrypted_blocks)


def decrypt_cfb(data: bytes, key: bytes, iv: bytes) -> bytes:
    validate_key(key)
    validate_iv(iv)

    cipher = AES.new(key, AES.MODE_ECB)

    decrypted_blocks = []

    # Для первого блока используется IV.
    feedback = iv

    for offset in range(0, len(data), BLOCK_SIZE):
        ciphertext_block = data[offset:offset + BLOCK_SIZE]

        # Получаем поток байтов для расшифрования.
        encrypted_feedback = cipher.encrypt(feedback)

        # Восстанавливаем исходный текст.
        plaintext_block = xor_bytes(
            ciphertext_block,
            encrypted_feedback[:len(ciphertext_block)]
        )

        decrypted_blocks.append(plaintext_block)

        # Для следующего блока используется исходный
        # шифротекст, а не расшифрованные данные.
        if len(ciphertext_block) == BLOCK_SIZE:
            feedback = ciphertext_block

    return b"".join(decrypted_blocks)