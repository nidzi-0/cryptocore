import argparse


SUPPORTED_HASH_ALGORITHMS = [
    "sha256",
    "sha3-256",
]


def create_digest_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cryptocore dgst",
        description=(
            "Вычисление криптографического "
            "хеша или HMAC файла."
        ),
    )

    parser.add_argument(
        "--algorithm",
        required=True,
        choices=SUPPORTED_HASH_ALGORITHMS,
        help=(
            "Алгоритм: sha256 или sha3-256."
        ),
    )

    parser.add_argument(
        "--input",
        required=True,
        dest="input_file",
        help=(
            "Путь к входному файлу. "
            "Для stdin можно использовать '-'."
        ),
    )

    parser.add_argument(
        "--output",
        required=False,
        dest="output_file",
        help=(
            "Файл для сохранения результата."
        ),
    )

    parser.add_argument(
        "--hmac",
        action="store_true",
        help=(
            "Включить режим HMAC-SHA256."
        ),
    )

    parser.add_argument(
        "--key",
        required=False,
        help=(
            "Ключ HMAC в hexadecimal-формате. "
            "Поддерживается произвольная длина."
        ),
    )

    parser.add_argument(
        "--verify",
        required=False,
        dest="verify_file",
        help=(
            "Проверить HMAC по значению "
            "из указанного файла."
        ),
    )

    return parser


def get_digest_arguments(argv=None):
    parser = create_digest_parser()

    args = parser.parse_args(argv)

    if args.hmac:
        if args.key is None:
            parser.error(
                "Для HMAC необходимо "
                "указать параметр --key."
            )

        if args.algorithm != "sha256":
            parser.error(
                "HMAC в CryptoCore использует "
                "алгоритм SHA-256."
            )

    else:
        if args.key is not None:
            parser.error(
                "Параметр --key используется "
                "только вместе с --hmac."
            )

        if args.verify_file is not None:
            parser.error(
                "Параметр --verify используется "
                "только вместе с --hmac."
            )

    return args
