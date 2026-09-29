import argparse

def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cryptocore",
        description=(
            "CryptoCore — шифрование и расшифрование "
            "файлов с помощью AES-128."
        )
    )

    parser.add_argument(
        "--algorithm",
        required=True,
        choices=["aes"],
        help="Алгоритм шифрования. Поддерживается aes."
    )

    parser.add_argument(
        "--mode",
        required=True,
        choices=[
            "ecb",
            "cbc",
            "cfb",
            "ofb",
            "ctr",
        ],
        help=(
            "Режим AES: ecb, cbc, cfb, ofb или ctr."
        )
    )

    operation_group = parser.add_mutually_exclusive_group(
        required=True
    )

    operation_group.add_argument(
        "--encrypt",
        action="store_true",
        help="Зашифровать входной файл."
    )

    operation_group.add_argument(
        "--decrypt",
        action="store_true",
        help="Расшифровать входной файл."
    )

    parser.add_argument(
        "--key",
        required=True,
        help=(
            "AES-128 ключ в шестнадцатеричном "
            "формате."
        )
    )

    parser.add_argument(
        "--iv",
        required=False,
        help=(
            "IV в шестнадцатеричном формате. "
            "Используется только при расшифровании "
            "CBC, CFB, OFB и CTR."
        )
    )

    parser.add_argument(
        "--input",
        required=True,
        dest="input_file",
        help="Путь к входному файлу."
    )

    parser.add_argument(
        "--output",
        required=False,
        dest="output_file",
        help="Путь к выходному файлу."
    )

    return parser


def parse_key(key_string: str) -> bytes:
    try:
        key = bytes.fromhex(key_string)
    except ValueError as error:
        raise ValueError(
            "Ключ должен быть корректной "
            "шестнадцатеричной строкой."
        ) from error

    if len(key) != 16:
        raise ValueError(
            "Для AES-128 ключ должен содержать "
            "ровно 16 байт "
            "(32 шестнадцатеричных символа)."
        )

    return key


def get_arguments(argv=None):
    parser = create_parser()

    args = parser.parse_args(argv)

    if args.encrypt and args.iv is not None:
        parser.error(
            "Параметр --iv нельзя использовать "
            "при шифровании. IV генерируется "
            "автоматически."
        )

    if args.mode == "ecb" and args.iv is not None:
        parser.error(
            "Режим ECB не использует IV."
        )

    return args