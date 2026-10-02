import os


def generate_random_bytes(num_bytes: int) -> bytes:
    if not isinstance(num_bytes, int):
        raise TypeError(
            "Количество случайных байтов "
            "должно быть целым числом."
        )

    if num_bytes <= 0:
        raise ValueError(
            "Количество случайных байтов "
            "должно быть больше нуля."
        )

    try:
        return os.urandom(num_bytes)

    except OSError as error:
        raise RuntimeError(
            "Не удалось получить криптографически "
            "стойкие случайные данные от "
            "операционной системы."
        ) from error