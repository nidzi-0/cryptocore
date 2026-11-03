import sys
from pathlib import Path
from typing import BinaryIO

from .digest_cli import get_digest_arguments
from .hash.sha256 import SHA256
from .hash.sha3_256 import SHA3_256


CHUNK_SIZE = 8192


HASH_ALGORITHMS = {
    "sha256": SHA256,
    "sha3-256": SHA3_256,
}


def create_hasher(algorithm: str):
    try:
        hasher_class = HASH_ALGORITHMS[
            algorithm
        ]

    except KeyError as error:
        raise ValueError(
            "Неподдерживаемый алгоритм "
            f"хеширования: {algorithm}"
        ) from error

    return hasher_class()


def hash_stream(
    stream: BinaryIO,
    algorithm: str,
) -> str:
    hasher = create_hasher(algorithm)

    while True:
        chunk = stream.read(CHUNK_SIZE)

        if not chunk:
            break

        hasher.update(chunk)

    return hasher.hexdigest()


def hash_file(
    file_path: str,
    algorithm: str,
) -> str:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Входной файл не найден: {file_path}"
        )

    if not path.is_file():
        raise IsADirectoryError(
            "Указанный путь не является "
            f"файлом: {file_path}"
        )

    try:
        with path.open("rb") as file:
            return hash_stream(
                file,
                algorithm,
            )

    except PermissionError as error:
        raise PermissionError(
            "Нет прав на чтение файла: "
            f"{file_path}"
        ) from error

    except OSError as error:
        raise OSError(
            "Ошибка при чтении файла "
            f"'{file_path}': {error}"
        ) from error


def format_digest_result(
    digest_value: str,
    input_file: str,
) -> str:
    return (
        f"{digest_value}  {input_file}"
    )


def write_digest_result(
    output_file: str,
    result: str,
) -> None:
    path = Path(output_file)

    try:
        if (
            path.parent
            and not path.parent.exists()
        ):
            path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

        path.write_text(
            result + "\n",
            encoding="utf-8",
        )

    except PermissionError as error:
        raise PermissionError(
            "Нет прав на запись файла: "
            f"{output_file}"
        ) from error

    except IsADirectoryError as error:
        raise IsADirectoryError(
            "Невозможно записать хеш: "
            f"'{output_file}' является папкой."
        ) from error

    except OSError as error:
        raise OSError(
            "Ошибка при записи файла "
            f"'{output_file}': {error}"
        ) from error


def digest_main(argv=None) -> int:
    args = get_digest_arguments(argv)

    try:
        if args.input_file == "-":
            digest_value = hash_stream(
                sys.stdin.buffer,
                args.algorithm,
            )

        else:
            digest_value = hash_file(
                args.input_file,
                args.algorithm,
            )

        result = format_digest_result(
            digest_value,
            args.input_file,
        )

        if args.output_file is not None:
            write_digest_result(
                args.output_file,
                result,
            )

        else:
            print(result)

        return 0

    except (
        ValueError,
        FileNotFoundError,
        PermissionError,
        IsADirectoryError,
        OSError,
    ) as error:
        print(
            f"Ошибка: {error}",
            file=sys.stderr,
        )

        return 1