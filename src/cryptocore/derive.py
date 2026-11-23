import argparse
import sys

from .csprng import generate_random_bytes
from .file_io import write_file
from .kdf.pbkdf2 import pbkdf2_hmac_sha256


DEFAULT_ITERATIONS = 100_000
DEFAULT_LENGTH = 32
SALT_SIZE = 16


def create_derive_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cryptocore derive",
        description=(
            "Получение криптографического "
            "ключа из пароля с помощью PBKDF2."
        ),
    )

    parser.add_argument(
        "--password",
        required=True,
        help="Пароль для получения ключа.",
    )

    parser.add_argument(
        "--salt",
        required=False,
        help=(
            "Salt в hexadecimal-формате. "
            "Если не указан, генерируется "
            "случайный salt длиной 16 байт."
        ),
    )

    parser.add_argument(
        "--iterations",
        type=int,
        default=DEFAULT_ITERATIONS,
        help=(
            "Количество итераций PBKDF2. "
            "По умолчанию 100000."
        ),
    )

    parser.add_argument(
        "--length",
        type=int,
        default=DEFAULT_LENGTH,
        help=(
            "Длина производного ключа "
            "в байтах. По умолчанию 32."
        ),
    )

    parser.add_argument(
        "--algorithm",
        choices=[
            "pbkdf2",
        ],
        default="pbkdf2",
        help=(
            "Алгоритм KDF. "
            "Поддерживается pbkdf2."
        ),
    )

    parser.add_argument(
        "--output",
        required=False,
        dest="output_file",
        help=(
            "Файл для сохранения "
            "производного ключа."
        ),
    )

    return parser


def parse_salt(
    salt_string: str | None,
) -> bytes:
    if salt_string is None:
        return generate_random_bytes(
            SALT_SIZE
        )

    try:
        salt = bytes.fromhex(
            salt_string
        )

    except ValueError as error:
        raise ValueError(
            "Salt должен быть корректной "
            "шестнадцатеричной строкой."
        ) from error

    if not salt:
        raise ValueError(
            "Salt не может быть пустым."
        )

    return salt


def derive_main(
    argv=None,
) -> int:
    parser = create_derive_parser()

    args = parser.parse_args(
        argv
    )

    try:
        if args.iterations <= 0:
            raise ValueError(
                "Количество итераций "
                "должно быть больше нуля."
            )

        if args.length <= 0:
            raise ValueError(
                "Длина ключа должна быть "
                "больше нуля."
            )

        salt = parse_salt(
            args.salt
        )

        derived_key = pbkdf2_hmac_sha256(
            password=args.password,
            salt=salt,
            iterations=args.iterations,
            dklen=args.length,
        )

        print(
            f"{derived_key.hex()} "
            f"{salt.hex()}"
        )

        if args.output_file is not None:
            write_file(
                file_path=args.output_file,
                data=derived_key,
            )

        return 0

    except (
        ValueError,
        RuntimeError,
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