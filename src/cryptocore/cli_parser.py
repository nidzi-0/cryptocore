import argparse


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cryptocore",
        description=(
            "CryptoCore — шифрование и расшифрование "
            "файлов с помощью AES-128."
        ),
    )

    parser.add_argument(
        "--algorithm",
        required=True,
        choices=["aes"],
        help="Алгоритм шифрования. Поддерживается aes.",
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
            "gcm",
        ],
        help=(
            "Режим AES: ecb, cbc, cfb, "
            "ofb, ctr или gcm."
        ),
    )

    operation_group = (
        parser.add_mutually_exclusive_group(
            required=True
        )
    )

    operation_group.add_argument(
        "--encrypt",
        action="store_true",
        help="Зашифровать входной файл.",
    )

    operation_group.add_argument(
        "--decrypt",
        action="store_true",
        help="Расшифровать входной файл.",
    )

    parser.add_argument(
        "--key",
        required=False,
        help=(
            "AES-128 ключ в шестнадцатеричном "
            "формате. При шифровании может быть "
            "сгенерирован автоматически."
        ),
    )

    parser.add_argument(
        "--iv",
        required=False,
        help=(
            "IV в шестнадцатеричном формате. "
            "Используется при расшифровании "
            "CBC, CFB, OFB и CTR. "
            "Для GCM может использоваться "
            "как совместимый псевдоним nonce."
        ),
    )

    parser.add_argument(
        "--nonce",
        required=False,
        help=(
            "Nonce в hexadecimal-формате. "
            "Используется только при "
            "расшифровании AES-GCM."
        ),
    )

    parser.add_argument(
        "--aad",
        required=False,
        help=(
            "Associated Authenticated Data "
            "в hexadecimal-формате. "
            "Используется только с AES-GCM."
        ),
    )

    parser.add_argument(
        "--input",
        required=True,
        dest="input_file",
        help="Путь к входному файлу.",
    )

    parser.add_argument(
        "--output",
        required=False,
        dest="output_file",
        help="Путь к выходному файлу.",
    )

    return parser


def parse_key(
    key_string: str,
) -> bytes:
    try:
        key = bytes.fromhex(
            key_string
        )

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


def parse_aad(
    aad_string: str | None,
) -> bytes:
    if aad_string is None:
        return b""

    try:
        return bytes.fromhex(
            aad_string
        )

    except ValueError as error:
        raise ValueError(
            "AAD должен быть корректной "
            "шестнадцатеричной строкой."
        ) from error


def parse_nonce(
    nonce_string: str,
) -> bytes:
    try:
        nonce = bytes.fromhex(
            nonce_string
        )

    except ValueError as error:
        raise ValueError(
            "Nonce должен быть корректной "
            "шестнадцатеричной строкой."
        ) from error

    if not nonce:
        raise ValueError(
            "Nonce не может быть пустым."
        )

    return nonce


def get_arguments(argv=None):
    parser = create_parser()

    args = parser.parse_args(
        argv
    )

    if (
        args.decrypt
        and args.key is None
    ):
        parser.error(
            "Для расшифрования необходимо "
            "указать параметр --key."
        )

    if (
        args.aad is not None
        and args.mode != "gcm"
    ):
        parser.error(
            "Параметр --aad используется "
            "только в режиме GCM."
        )

    if (
        args.nonce is not None
        and args.mode != "gcm"
    ):
        parser.error(
            "Параметр --nonce используется "
            "только в режиме GCM."
        )

    if args.mode == "gcm":
        if (
            args.encrypt
            and (
                args.iv is not None
                or args.nonce is not None
            )
        ):
            parser.error(
                "При GCM-шифровании nonce "
                "генерируется автоматически. "
                "--iv и --nonce указывать нельзя."
            )

        if (
            args.iv is not None
            and args.nonce is not None
        ):
            parser.error(
                "Для GCM нельзя одновременно "
                "указывать --iv и --nonce."
            )

    else:
        if (
            args.encrypt
            and args.iv is not None
        ):
            parser.error(
                "Параметр --iv нельзя использовать "
                "при шифровании. IV генерируется "
                "автоматически."
            )

        if (
            args.mode == "ecb"
            and args.iv is not None
        ):
            parser.error(
                "Режим ECB не использует IV."
            )

    return args