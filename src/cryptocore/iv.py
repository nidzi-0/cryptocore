import os

IV_SIZE = 16

def generate_iv() -> bytes:
    return os.urandom(IV_SIZE)


def parse_iv(iv_string: str) -> bytes:
    try:
        iv = bytes.fromhex(iv_string)
    except ValueError as error:
        raise ValueError(
            "IV должен быть корректной шестнадцатеричной строкой."
        ) from error

    if len(iv) != IV_SIZE:
        raise ValueError(
            "IV должен иметь длину ровно 16 байт "
            "(32 шестнадцатеричных символа)."
        )

    return iv


def prepend_iv(iv: bytes, ciphertext: bytes) -> bytes:
    if len(iv) != IV_SIZE:
        raise ValueError(
            "IV должен иметь длину ровно 16 байт."
        )

    return iv + ciphertext


def split_iv(data: bytes) -> tuple[bytes, bytes]:
    if len(data) < IV_SIZE:
        raise ValueError(
            "Зашифрованный файл слишком короткий: "
            "невозможно прочитать 16-байтовый IV."
        )

    iv = data[:IV_SIZE]
    ciphertext = data[IV_SIZE:]

    return iv, ciphertext