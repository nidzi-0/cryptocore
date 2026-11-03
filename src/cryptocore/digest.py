import sys
from pathlib import Path
from secrets import compare_digest
from typing import BinaryIO

from .digest_cli import get_digest_arguments
from .hash.sha256 import SHA256
from .hash.sha3_256 import SHA3_256
from .mac.hmac import HMACSHA256


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


def parse_hmac_key(
    key_string: str,
) -> bytes:
    if len(key_string) % 2 != 0:
        raise ValueError(
            "HMAC-ключ должен содержать "
            "чётное количество hexadecimal-символов."
        )

    allowed = set(
        "0123456789abcdefABCDEF"
    )

    if any(
        character not in allowed
        for character in key_string
    ):
        raise ValueError(
            "HMAC-ключ должен быть корректной "
            "hexadecimal-строкой."
        )

    return bytes.fromhex(
        key_string
    )


def hash_stream(
    stream: BinaryIO,
    algorithm: str,
) -> str:
    hasher = create_hasher(
        algorithm
    )

    while True:
        chunk = stream.read(
            CHUNK_SIZE
        )

        if not chunk:
            break

        hasher.update(
            chunk
        )

    return hasher.hexdigest()


def hash_file(
    file_path: str,
    algorithm: str,
) -> str:
    path = Path(
        file_path
    )

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


def hmac_stream(
    stream: BinaryIO,
    key: bytes,
) -> str:
    mac = HMACSHA256(
        key
    )

    while True:
        chunk = stream.read(
            CHUNK_SIZE
        )

        if not chunk:
            break

        mac.update(
            chunk
        )

    return mac.hexdigest()


def hmac_file(
    file_path: str,
    key: bytes,
) -> str:
    path = Path(
        file_path
    )

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
            return hmac_stream(
                file,
                key,
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
    path = Path(
        output_file
    )

    try:
        parent_directory = (
            path.parent
        )

        if not parent_directory.exists():
            parent_directory.mkdir(
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
            "Невозможно записать результат: "
            f"'{output_file}' является папкой."
        ) from error

    except OSError as error:
        raise OSError(
            "Ошибка при записи файла "
            f"'{output_file}': {error}"
        ) from error


def read_expected_hmac(
    file_path: str,
) -> str:
    path = Path(
        file_path
    )

    if not path.exists():
        raise FileNotFoundError(
            "Файл с ожидаемым HMAC "
            f"не найден: {file_path}"
        )

    if not path.is_file():
        raise IsADirectoryError(
            "Путь к ожидаемому HMAC "
            f"не является файлом: {file_path}"
        )

    try:
        content = path.read_text(
            encoding="utf-8"
        ).strip()

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

    if not content:
        raise ValueError(
            "Файл с ожидаемым HMAC пуст."
        )

    # Формат:
    # HMAC_VALUE  INPUT_FILE
    #
    # Имя файла после HMAC можно игнорировать.
    expected_hmac = (
        content.split()[0]
        .strip()
        .lower()
    )

    if (
        len(expected_hmac) != 64
        or any(
            character
            not in "0123456789abcdef"
            for character in expected_hmac
        )
    ):
        raise ValueError(
            "Файл проверки не содержит "
            "корректный HMAC-SHA256."
        )

    return expected_hmac


def verify_hmac(
    computed_hmac: str,
    verify_file: str,
) -> bool:
    expected_hmac = read_expected_hmac(
        verify_file
    )

    return compare_digest(
        computed_hmac.lower(),
        expected_hmac,
    )


def digest_main(argv=None) -> int:
    args = get_digest_arguments(
        argv
    )

    try:
        if args.hmac:
            key = parse_hmac_key(
                args.key
            )

            if args.input_file == "-":
                digest_value = hmac_stream(
                    sys.stdin.buffer,
                    key,
                )

            else:
                digest_value = hmac_file(
                    args.input_file,
                    key,
                )

        else:
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

        if args.verify_file is not None:
            if verify_hmac(
                digest_value,
                args.verify_file,
            ):
                print(
                    "[OK] HMAC verification successful"
                )

                return 0

            print(
                "[ERROR] HMAC verification failed",
                file=sys.stderr,
            )

            return 1

        if args.output_file is not None:
            write_digest_result(
                args.output_file,
                result,
            )

        else:
            print(
                result
            )

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