import sys

from .digest import digest_main
from .cli_parser import (
    get_arguments,
    parse_aad,
    parse_key,
    parse_nonce,
)
from .csprng import generate_random_bytes
from .file_io import (
    read_file,
    write_file,
)
from .iv import (
    generate_iv,
    parse_iv,
    prepend_iv,
    split_iv,
)
from .modes.ecb import (
    encrypt_ecb,
    decrypt_ecb,
)
from .modes.cbc import (
    encrypt_cbc,
    decrypt_cbc,
)
from .modes.cfb import (
    encrypt_cfb,
    decrypt_cfb,
)
from .modes.ofb import (
    encrypt_ofb,
    decrypt_ofb,
)
from .modes.ctr import (
    encrypt_ctr,
    decrypt_ctr,
)
from .modes.gcm import (
    AuthenticationError,
    NONCE_SIZE,
    TAG_SIZE,
    decrypt_gcm,
    encrypt_gcm,
)


KEY_SIZE = 16


WEAK_SEQUENTIAL_KEY = bytes(
    range(16)
)

WEAK_REVERSE_SEQUENTIAL_KEY = bytes(
    range(
        15,
        -1,
        -1,
    )
)


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
    encrypt: bool,
) -> str:
    if encrypt:
        return (
            input_file
            + ".enc"
        )

    return (
        input_file
        + ".dec"
    )


def get_weak_key_reason(
    key: bytes,
) -> str | None:
    if len(set(key)) == 1:
        return (
            "ключ состоит из одного "
            "повторяющегося байта"
        )

    if (
        key
        == WEAK_SEQUENTIAL_KEY
    ):
        return (
            "ключ содержит последовательные "
            "байты от 00 до 0F"
        )

    if (
        key
        == WEAK_REVERSE_SEQUENTIAL_KEY
    ):
        return (
            "ключ содержит обратную "
            "последовательность байтов"
        )

    return None


def warn_if_weak_key(
    key: bytes,
) -> None:
    reason = get_weak_key_reason(
        key
    )

    if reason is not None:
        print(
            "[WARNING] Обнаружен потенциально "
            f"слабый AES-ключ: {reason}.",
            file=sys.stderr,
        )


def get_encryption_key(
    key_string: str | None,
) -> tuple[bytes, bool]:
    if key_string is not None:
        return (
            parse_key(
                key_string
            ),
            False,
        )

    key = generate_random_bytes(
        KEY_SIZE
    )

    return (
        key,
        True,
    )


def encrypt_data(
    data: bytes,
    key: bytes,
    mode: str,
    aad: bytes = b"",
) -> tuple[
    bytes,
    bytes | None,
]:
    if mode == "ecb":
        encrypted = encrypt_ecb(
            data=data,
            key=key,
        )

        return (
            encrypted,
            None,
        )

    if mode == "gcm":
        nonce = generate_random_bytes(
            NONCE_SIZE
        )

        ciphertext, tag = (
            encrypt_gcm(
                data=data,
                key=key,
                nonce=nonce,
                aad=aad,
            )
        )

        result = (
            nonce
            + ciphertext
            + tag
        )

        return (
            result,
            nonce,
        )

    iv = generate_iv()

    encrypt_function = (
        ENCRYPT_FUNCTIONS[
            mode
        ]
    )

    ciphertext = encrypt_function(
        data=data,
        key=key,
        iv=iv,
    )

    result = prepend_iv(
        iv=iv,
        ciphertext=ciphertext,
    )

    return (
        result,
        iv,
    )


def decrypt_data(
    data: bytes,
    key: bytes,
    mode: str,
    iv_string: str | None = None,
    nonce_string: str | None = None,
    aad: bytes = b"",
) -> bytes:
    if mode == "ecb":
        return decrypt_ecb(
            data=data,
            key=key,
        )

    if mode == "gcm":
        explicit_nonce = (
            nonce_string
            if nonce_string
            is not None
            else iv_string
        )

        if explicit_nonce is not None:
            nonce = parse_nonce(
                explicit_nonce
            )

            if len(data) < TAG_SIZE:
                raise ValueError(
                    "GCM ciphertext слишком "
                    "короткий: отсутствует "
                    "16-байтовый authentication tag."
                )

            ciphertext = (
                data[:-TAG_SIZE]
            )

            tag = (
                data[-TAG_SIZE:]
            )

        else:
            minimum_size = (
                NONCE_SIZE
                + TAG_SIZE
            )

            if len(data) < minimum_size:
                raise ValueError(
                    "GCM-файл слишком короткий: "
                    "необходимы 12-байтовый nonce "
                    "и 16-байтовый tag."
                )

            nonce = (
                data[:NONCE_SIZE]
            )

            ciphertext = (
                data[
                    NONCE_SIZE:
                    -TAG_SIZE
                ]
            )

            tag = (
                data[-TAG_SIZE:]
            )

        return decrypt_gcm(
            data=ciphertext,
            tag=tag,
            key=key,
            nonce=nonce,
            aad=aad,
        )

    if iv_string is not None:
        iv = parse_iv(
            iv_string
        )

        ciphertext = data

    else:
        iv, ciphertext = split_iv(
            data
        )

    decrypt_function = (
        DECRYPT_FUNCTIONS[
            mode
        ]
    )

    return decrypt_function(
        data=ciphertext,
        key=key,
        iv=iv,
    )


def main() -> int:
    if (
        len(sys.argv) > 1
        and sys.argv[1] == "dgst"
    ):
        return digest_main(
            sys.argv[2:]
        )

    try:
        args = get_arguments()

        generated_key = False

        if args.encrypt:
            (
                key,
                generated_key,
            ) = get_encryption_key(
                args.key
            )

            if generated_key:
                print(
                    "[INFO] Generated random key: "
                    f"{key.hex()}"
                )

            else:
                warn_if_weak_key(
                    key
                )

        else:
            key = parse_key(
                args.key
            )

            warn_if_weak_key(
                key
            )

        aad = parse_aad(
            args.aad
        )

        input_data = read_file(
            args.input_file
        )

        generated_iv_or_nonce = None

        if args.encrypt:
            (
                result,
                generated_iv_or_nonce,
            ) = encrypt_data(
                data=input_data,
                key=key,
                mode=args.mode,
                aad=aad,
            )

            operation_name = (
                "Шифрование"
            )

        else:
            result = decrypt_data(
                data=input_data,
                key=key,
                mode=args.mode,
                iv_string=args.iv,
                nonce_string=args.nonce,
                aad=aad,
            )

            operation_name = (
                "Расшифрование"
            )

        output_file = (
            args.output_file
        )

        if output_file is None:
            output_file = (
                get_default_output_name(
                    input_file=(
                        args.input_file
                    ),
                    encrypt=args.encrypt,
                )
            )

        # ВАЖНО:
        # write_file() вызывается только
        # ПОСЛЕ успешной GCM-аутентификации.
        write_file(
            file_path=output_file,
            data=result,
        )

        print(
            f"{operation_name} "
            "успешно завершено."
        )

        print(
            "Результат сохранён в: "
            f"{output_file}"
        )

        if (
            generated_iv_or_nonce
            is not None
        ):
            if args.mode == "gcm":
                print(
                    "Nonce: "
                    f"{generated_iv_or_nonce.hex().upper()}"
                )

            else:
                print(
                    "IV: "
                    f"{generated_iv_or_nonce.hex().upper()}"
                )

        return 0

    except AuthenticationError as error:
        print(
            f"[ERROR] {error}",
            file=sys.stderr,
        )

        return 1

    except (
        ValueError,
        RuntimeError,
        FileNotFoundError,
        PermissionError,
        IsADirectoryError,
        OSError,
        KeyError,
    ) as error:
        print(
            f"Ошибка: {error}",
            file=sys.stderr,
        )

        return 1


if __name__ == "__main__":
    raise SystemExit(
        main()
    )