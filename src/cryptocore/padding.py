BLOCK_SIZE = 16

def pad(data: bytes, block_size: int = BLOCK_SIZE) -> bytes:
    if block_size < 1 or block_size > 255:
        raise ValueError("Размер блока должен быть от 1 до 255 байт.")

    padding_length = block_size - (len(data) % block_size)

    padding = bytes([padding_length]) * padding_length

    return data + padding


def unpad(data: bytes, block_size: int = BLOCK_SIZE) -> bytes:
    if not data:
        raise ValueError("Невозможно удалить padding из пустых данных.")

    if len(data) % block_size != 0:
        raise ValueError(
            "Длина данных должна быть кратна размеру блока."
        )

    padding_length = data[-1]

    if padding_length < 1 or padding_length > block_size:
        raise ValueError("Некорректный PKCS#7 padding.")

    padding = data[-padding_length:]

    expected_padding = bytes([padding_length]) * padding_length

    if padding != expected_padding:
        raise ValueError("Некорректный PKCS#7 padding.")

    return data[:-padding_length]