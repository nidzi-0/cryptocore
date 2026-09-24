from Crypto.Cipher import AES

from ..padding import pad, unpad
from .ecb import validate_key


BLOCK_SIZE = 16


def xor_bytes(first: bytes, second: bytes) -> bytes:
    if len(first) != len(second):
        raise ValueError(
            "Для операции XOR длины блоков должны совпадать."
        )

    return bytes(
        a ^ b
        for a, b in zip(first, second)
    )


def validate_iv(iv: bytes) -> None:
    if len(iv) != BLOCK_SIZE:
        raise ValueError(
            "IV должен иметь длину ровно 16 байт."
        )


def encrypt_cbc(
    data: bytes,
    key: bytes,
    iv: bytes
) -> bytes:
    validate_key(key)
    validate_iv(iv)

    padded_data = pad(
        data,
        BLOCK_SIZE
    )

    cipher = AES.new(
        key,
        AES.MODE_ECB
    )

    encrypted_blocks = []

    previous_block = iv

    for offset in range(
        0,
        len(padded_data),
        BLOCK_SIZE
    ):
        plaintext_block = padded_data[
            offset:offset + BLOCK_SIZE
        ]

        xored_block = xor_bytes(
            plaintext_block,
            previous_block
        )

        encrypted_block = cipher.encrypt(
            xored_block
        )

        encrypted_blocks.append(
            encrypted_block
        )

        previous_block = encrypted_block

    return b"".join(
        encrypted_blocks
    )


def decrypt_cbc(
    data: bytes,
    key: bytes,
    iv: bytes
) -> bytes:
    validate_key(key)
    validate_iv(iv)

    if not data:
        raise ValueError(
            "Зашифрованные данные не могут быть пустыми."
        )

    if len(data) % BLOCK_SIZE != 0:
        raise ValueError(
            "Длина ciphertext для CBC должна быть "
            "кратна 16 байтам."
        )

    cipher = AES.new(
        key,
        AES.MODE_ECB
    )

    decrypted_blocks = []

    previous_block = iv

    for offset in range(
        0,
        len(data),
        BLOCK_SIZE
    ):
        ciphertext_block = data[
            offset:offset + BLOCK_SIZE
        ]

        decrypted_block = cipher.decrypt(
            ciphertext_block
        )

        plaintext_block = xor_bytes(
            decrypted_block,
            previous_block
        )

        decrypted_blocks.append(
            plaintext_block
        )

        previous_block = ciphertext_block

    decrypted_data = b"".join(
        decrypted_blocks
    )

    return unpad(
        decrypted_data,
        BLOCK_SIZE
    )