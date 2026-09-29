import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


KEY_HEX = "000102030405060708090a0b0c0d0e0f"

FIXED_IV_HEX = (
    "AABBCCDDEEFF00112233445566778899"
)

MODES = [
    "ecb",
    "cbc",
    "cfb",
    "ofb",
    "ctr",
]


def run_command(command: list[str]) -> None:
    subprocess.run(
        command,
        check=True
    )


def check_files_equal(
    first_file: Path,
    second_file: Path
) -> bool:
    return (
        first_file.read_bytes()
        == second_file.read_bytes()
    )


def cryptocore_to_openssl(
    mode: str,
    directory: Path,
    original_file: Path
) -> bool:
    cryptocore_file = (
        directory / f"{mode}_cryptocore.bin"
    )

    openssl_decrypted_file = (
        directory / f"{mode}_openssl_decrypted.bin"
    )

    run_command([
        sys.executable,
        "-m",
        "cryptocore",
        "--algorithm",
        "aes",
        "--mode",
        mode,
        "--encrypt",
        "--key",
        KEY_HEX,
        "--input",
        str(original_file),
        "--output",
        str(cryptocore_file),
    ])

    # ECB не использует IV.
    if mode == "ecb":
        run_command([
            "openssl",
            "enc",
            "-aes-128-ecb",
            "-d",
            "-K",
            KEY_HEX,
            "-nosalt",
            "-in",
            str(cryptocore_file),
            "-out",
            str(openssl_decrypted_file),
        ])

    else:
        encrypted_data = cryptocore_file.read_bytes()

        if len(encrypted_data) < 16:
            raise ValueError(
                "Файл CryptoCore не содержит "
                "16-байтовый IV."
            )

        # Первые 16 байт файла — IV.
        iv = encrypted_data[:16]

        # Остальные байты — ciphertext.
        ciphertext = encrypted_data[16:]

        ciphertext_file = (
            directory / f"{mode}_ciphertext.bin"
        )

        ciphertext_file.write_bytes(
            ciphertext
        )

        run_command([
            "openssl",
            "enc",
            f"-aes-128-{mode}",
            "-d",
            "-K",
            KEY_HEX,
            "-iv",
            iv.hex(),
            "-in",
            str(ciphertext_file),
            "-out",
            str(openssl_decrypted_file),
        ])

    return check_files_equal(
        original_file,
        openssl_decrypted_file
    )


def openssl_to_cryptocore(
    mode: str,
    directory: Path,
    original_file: Path
) -> bool:
    openssl_ciphertext_file = (
        directory / f"{mode}_openssl.bin"
    )

    cryptocore_decrypted_file = (
        directory / f"{mode}_cryptocore_decrypted.bin"
    )

    # ECB не использует IV.
    if mode == "ecb":
        run_command([
            "openssl",
            "enc",
            "-aes-128-ecb",
            "-e",
            "-K",
            KEY_HEX,
            "-nosalt",
            "-in",
            str(original_file),
            "-out",
            str(openssl_ciphertext_file),
        ])

        run_command([
            sys.executable,
            "-m",
            "cryptocore",
            "--algorithm",
            "aes",
            "--mode",
            "ecb",
            "--decrypt",
            "--key",
            KEY_HEX,
            "--input",
            str(openssl_ciphertext_file),
            "--output",
            str(cryptocore_decrypted_file),
        ])

    else:
        run_command([
            "openssl",
            "enc",
            f"-aes-128-{mode}",
            "-e",
            "-K",
            KEY_HEX,
            "-iv",
            FIXED_IV_HEX,
            "-in",
            str(original_file),
            "-out",
            str(openssl_ciphertext_file),
        ])

        run_command([
            sys.executable,
            "-m",
            "cryptocore",
            "--algorithm",
            "aes",
            "--mode",
            mode,
            "--decrypt",
            "--key",
            KEY_HEX,
            "--iv",
            FIXED_IV_HEX,
            "--input",
            str(openssl_ciphertext_file),
            "--output",
            str(cryptocore_decrypted_file),
        ])

    return check_files_equal(
        original_file,
        cryptocore_decrypted_file
    )


def verify_ecb_ciphertext(
    directory: Path,
    original_file: Path
) -> bool:
    cryptocore_file = (
        directory / "ecb_cryptocore_verify.bin"
    )

    openssl_file = (
        directory / "ecb_openssl_verify.bin"
    )

    # Шифрование через CryptoCore.
    run_command([
        sys.executable,
        "-m",
        "cryptocore",
        "--algorithm",
        "aes",
        "--mode",
        "ecb",
        "--encrypt",
        "--key",
        KEY_HEX,
        "--input",
        str(original_file),
        "--output",
        str(cryptocore_file),
    ])

    run_command([
        "openssl",
        "enc",
        "-aes-128-ecb",
        "-e",
        "-K",
        KEY_HEX,
        "-nosalt",
        "-in",
        str(original_file),
        "-out",
        str(openssl_file),
    ])

    cryptocore_ciphertext = (
        cryptocore_file.read_bytes()
    )

    openssl_ciphertext = (
        openssl_file.read_bytes()
    )

    print(
        "CryptoCore ciphertext: "
        f"{cryptocore_ciphertext.hex().upper()}"
    )

    print(
        "OpenSSL ciphertext:   "
        f"{openssl_ciphertext.hex().upper()}"
    )

    return (
        cryptocore_ciphertext
        == openssl_ciphertext
    )


def main() -> int:
    if shutil.which("openssl") is None:
        print(
            "ERROR: OpenSSL не найден в PATH."
        )
        return 1

    print(
        "CryptoCore / OpenSSL interoperability test"
    )

    version_result = subprocess.run(
        ["openssl", "version"],
        check=True,
        capture_output=True,
        text=True
    )

    print(
        version_result.stdout.strip()
    )

    passed = 0

    # 5 режимов x 2 направления
    # + отдельное сравнение ciphertext ECB.
    total = len(MODES) * 2 + 1

    with tempfile.TemporaryDirectory() as temp_dir:
        directory = Path(temp_dir)

        original_file = (
            directory / "original.bin"
        )

        original_data = (
            b"CryptoCore OpenSSL interoperability test"
            b"\x00\x01\x02\x03\x04\xff"
        )

        original_file.write_bytes(
            original_data
        )

        for mode in MODES:
            print(
                f"\n[{mode.upper()}]"
            )

            if cryptocore_to_openssl(
                mode,
                directory,
                original_file
            ):
                print(
                    "PASS: CryptoCore -> OpenSSL"
                )
                passed += 1
            else:
                print(
                    "FAIL: CryptoCore -> OpenSSL"
                )

            if openssl_to_cryptocore(
                mode,
                directory,
                original_file
            ):
                print(
                    "PASS: OpenSSL -> CryptoCore"
                )
                passed += 1
            else:
                print(
                    "FAIL: OpenSSL -> CryptoCore"
                )

        print(
            "\n[SPRINT 1 TEST-3 / ECB CIPHERTEXT]"
        )

        if verify_ecb_ciphertext(
            directory,
            original_file
        ):
            print(
                "PASS: ciphertext CryptoCore ECB "
                "совпадает с ciphertext OpenSSL ECB"
            )

            passed += 1

        else:
            print(
                "FAIL: ciphertext CryptoCore ECB "
                "отличается от ciphertext OpenSSL ECB"
            )

    print(
        f"\nResult: {passed}/{total} checks passed"
    )

    if passed == total:
        print(
            "OpenSSL interoperability: PASSED"
        )

        return 0

    print(
        "OpenSSL interoperability: FAILED"
    )

    return 1


if __name__ == "__main__":
    raise SystemExit(main())