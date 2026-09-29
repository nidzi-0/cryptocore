import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


KEY_HEX = "000102030405060708090a0b0c0d0e0f"


def main() -> int:
    if shutil.which("openssl") is None:
        print("ERROR: OpenSSL не найден в PATH.")
        return 1

    print("Sprint 1 TEST-3: AES-128-ECB / OpenSSL")
    print(
        subprocess.run(
            ["openssl", "version"],
            check=True,
            capture_output=True,
            text=True
        ).stdout.strip()
    )

    with tempfile.TemporaryDirectory() as temp_dir:
        directory = Path(temp_dir)

        plaintext_file = directory / "plaintext.bin"
        cryptocore_file = directory / "cryptocore.bin"
        openssl_file = directory / "openssl.bin"

        # Длина специально не кратна 16 байтам,
        # чтобы одновременно проверить PKCS#7 padding.
        plaintext = (
            b"CryptoCore Sprint 1 OpenSSL verification."
            b"\x00\x01\x02\xff"
        )

        plaintext_file.write_bytes(plaintext)

        # Шифруем через CryptoCore.
        subprocess.run(
            [
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
                str(plaintext_file),
                "--output",
                str(cryptocore_file),
            ],
            check=True
        )

        # Шифруем те же данные через OpenSSL.
        # OpenSSL по умолчанию использует PKCS#7 padding.
        subprocess.run(
            [
                "openssl",
                "enc",
                "-aes-128-ecb",
                "-e",
                "-K",
                KEY_HEX,
                "-nosalt",
                "-in",
                str(plaintext_file),
                "-out",
                str(openssl_file),
            ],
            check=True
        )

        cryptocore_ciphertext = cryptocore_file.read_bytes()
        openssl_ciphertext = openssl_file.read_bytes()

        print()
        print(
            f"CryptoCore ciphertext: "
            f"{cryptocore_ciphertext.hex().upper()}"
        )

        print(
            f"OpenSSL ciphertext:   "
            f"{openssl_ciphertext.hex().upper()}"
        )

        print()

        if cryptocore_ciphertext == openssl_ciphertext:
            print(
                "PASS: ciphertext CryptoCore полностью "
                "совпадает с ciphertext OpenSSL."
            )
            return 0

        print(
            "FAIL: ciphertext CryptoCore и OpenSSL различаются."
        )

        print(
            f"CryptoCore size: {len(cryptocore_ciphertext)} bytes"
        )

        print(
            f"OpenSSL size:   {len(openssl_ciphertext)} bytes"
        )

        return 1


if __name__ == "__main__":
    raise SystemExit(main())