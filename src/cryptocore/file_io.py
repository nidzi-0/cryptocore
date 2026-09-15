from pathlib import Path

def read_file(file_path: str) -> bytes:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Входной файл не найден: {file_path}"
        )

    if not path.is_file():
        raise IsADirectoryError(
            f"Указанный путь не является файлом: {file_path}"
        )

    try:
        with path.open("rb") as file:
            return file.read()

    except PermissionError as error:
        raise PermissionError(
            f"Нет прав на чтение файла: {file_path}"
        ) from error

    except OSError as error:
        raise OSError(
            f"Ошибка при чтении файла '{file_path}': {error}"
        ) from error


def write_file(file_path: str, data: bytes) -> None:
    path = Path(file_path)

    try:
        parent_directory = path.parent

        if not parent_directory.exists():
            parent_directory.mkdir(
                parents=True,
                exist_ok=True
            )

        with path.open("wb") as file:
            file.write(data)

    except PermissionError as error:
        raise PermissionError(
            f"Нет прав на запись файла: {file_path}"
        ) from error

    except IsADirectoryError as error:
        raise IsADirectoryError(
            f"Невозможно записать данные: '{file_path}' является папкой."
        ) from error

    except OSError as error:
        raise OSError(
            f"Ошибка при записи файла '{file_path}': {error}"
        ) from error