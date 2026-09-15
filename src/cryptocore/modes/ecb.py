from Crypto.Cipher import AES

from ..padding import pad, unpad


BLOCK_SIZE = 16
KEY_SIZE = 16


def validate_key(key: bytes) -> None:
    if len(key) != KEY_SIZE:
        raise ValueError(
            "Для AES-128 ключ должен иметь длину ровно 16 байт."
        )


def encrypt_ecb(data: bytes, key: bytes) -> bytes:
    validate_key(key)

    padded_data = pad(data, BLOCK_SIZE)

    cipher = AES.new(key, AES.MODE_ECB)

    encrypted_blocks = []

    for offset in range(0, len(padded_data), BLOCK_SIZE):
        block = padded_data[offset:offset + BLOCK_SIZE]

        encrypted_block = cipher.encrypt(block)

        encrypted_blocks.append(encrypted_block)

    return b"".join(encrypted_blocks)


def decrypt_ecb(data: bytes, key: bytes) -> bytes:
    validate_key(key)

    if not data:
        raise ValueError(
            "Зашифрованные данные не могут быть пустыми."
        )

    if len(data) % BLOCK_SIZE != 0:
        raise ValueError(
            "Длина зашифрованных данных должна быть кратна 16 байтам."
        )

    cipher = AES.new(key, AES.MODE_ECB)

    decrypted_blocks = []

    for offset in range(0, len(data), BLOCK_SIZE):
        block = data[offset:offset + BLOCK_SIZE]

        decrypted_block = cipher.decrypt(block)

        decrypted_blocks.append(decrypted_block)

    decrypted_data = b"".join(decrypted_blocks)

    return unpad(decrypted_data, BLOCK_SIZE)