import sys

from .cli_parser import get_arguments, parse_key
from .file_io import read_file, write_file
from .modes.ecb import encrypt_ecb, decrypt_ecb

def get_default_output_name(input_file: str, encrypt: bool) -> str:
    if encrypt:
        return input_file + ".enc"

    return input_file + ".dec"


def main() -> int:
    try:
        args = get_arguments()

        key = parse_key(args.key)

        input_data = read_file(args.input_file)

        if args.encrypt:
            result = encrypt_ecb(
                data=input_data,
                key=key
            )

            operation_name = "Шифрование"

        else:
            result = decrypt_ecb(
                data=input_data,
                key=key
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

        print(f"{operation_name} успешно завершено.")
        print(f"Результат сохранён в: {output_file}")

        return 0

    except (
        ValueError,
        FileNotFoundError,
        PermissionError,
        IsADirectoryError,
        OSError
    ) as error:
        print(
            f"Ошибка: {error}",
            file=sys.stderr
        )
        return 1

if __name__ == "__main__":
    sys.exit(main())