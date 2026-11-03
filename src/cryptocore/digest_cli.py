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
            "хеша файла."
        ),
    )

    parser.add_argument(
        "--algorithm",
        required=True,
        choices=SUPPORTED_HASH_ALGORITHMS,
        help=(
            "Алгоритм хеширования: "
            "sha256 или sha3-256."
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
            "Файл для сохранения результата. "
            "Если не указан, результат "
            "выводится в stdout."
        ),
    )

    return parser


def get_digest_arguments(argv=None):
    parser = create_digest_parser()

    return parser.parse_args(argv)