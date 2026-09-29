import sys

from .cli_parser import get_arguments, parse_key
from .file_io import read_file, write_file
from .iv import (
    generate_iv,
    parse_iv,
    prepend_iv,
    split_iv,
)
from .modes.ecb import encrypt_ecb, decrypt_ecb
from .modes.cbc import encrypt_cbc, decrypt_cbc
from .modes.cfb import encrypt_cfb, decrypt_cfb
from .modes.ofb import encrypt_ofb, decrypt_ofb
from .modes.ctr import encrypt_ctr, decrypt_ctr


ENCRYPT_FUNCTIONS = {
    "cbc": encrypt_cbc,
    "cfb": encrypt_cfb,
    "ofb": encrypt_ofb,
    "ctr": encrypt_ctr,
}

DECRYPT_FUNCTIONS = {
    "cbc": decrypt_cbc,
    "cfb": decrypt_cfb,
    "ofb": decrypt_ofb,
    "ctr": decrypt_ctr,
}


def get_default_output_name(
    input_file: str,
    encrypt: bool
) -> str:
    if encrypt:
        return input_file + ".enc"

    return input_file + ".dec"


def encrypt_data(
    data: bytes,
    key: bytes,
    mode: str
) -> tuple[bytes, bytes | None]:
    if mode == "ecb":
        encrypted = encrypt_ecb(
            data=data,
            key=key
        )

        return encrypted, None

    iv = generate_iv()

    encrypt_function = ENCRYPT_FUNCTIONS[mode]

    ciphertext = encrypt_function(
        data=data,
        key=key,
        iv=iv
    )

    result = prepend_iv(
        iv=iv,
        ciphertext=ciphertext
    )

    return result, iv


def decrypt_data(
    data: bytes,
    key: bytes,
    mode: str,
    iv_string: str | None = None
) -> bytes:
    if mode == "ecb":
        return decrypt_ecb(
            data=data,
            key=key
        )

    if iv_string is not None:
        iv = parse_iv(iv_string)
        ciphertext = data
    else:
        iv, ciphertext = split_iv(data)

    decrypt_function = DECRYPT_FUNCTIONS[mode]

    return decrypt_function(
        data=ciphertext,
        key=key,
        iv=iv
    )


def main() -> int:
    try:
        args = get_arguments()

        key = parse_key(args.key)

        input_data = read_file(
            args.input_file
        )

        generated_iv = None

        if args.encrypt:
            result, generated_iv = encrypt_data(
                data=input_data,
                key=key,
                mode=args.mode
            )

            operation_name = "Шифрование"

        else:
            result = decrypt_data(
                data=input_data,
                key=key,
                mode=args.mode,
                iv_string=args.iv
            )

            operation_name = "Расшифрование"

        output_file = args.output_file

        if output_file is None:
            output_file = get_default_output_name(
                input_file=args.input_file,
                encrypt=args.encrypt
            )

        write_file(
            file_path=output_file,
            data=result
        )

        print(
            f"{operation_name} успешно завершено."
        )

        print(
            f"Результат сохранён в: {output_file}"
        )

        if generated_iv is not None:
            print(
                f"IV: {generated_iv.hex().upper()}"
            )

        return 0

    except (
        ValueError,
        FileNotFoundError,
        PermissionError,
        IsADirectoryError,
        OSError,
        KeyError
    ) as error:
        print(
            f"Ошибка: {error}",
            file=sys.stderr
        )

        return 1


if __name__ == "__main__":
    sys.exit(main())