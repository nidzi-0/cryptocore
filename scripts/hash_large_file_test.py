import hashlib
from pathlib import Path

from cryptocore.hash.sha256 import SHA256
from cryptocore.hash.sha3_256 import SHA3_256


TEST_FILE = Path(
    "large_hash_test.bin"
)

FILE_SIZE = (
    1024 * 1024 * 1024
    + 1
)

CHUNK_SIZE = 1024 * 1024


def create_large_file() -> None:
    print(
        "Создание тестового файла "
        "размером > 1 GB..."
    )

    with TEST_FILE.open("wb") as file:
        file.seek(
            FILE_SIZE - 1
        )

        file.write(b"\x00")


def test_large_file() -> bool:
    custom_sha256 = SHA256()
    custom_sha3 = SHA3_256()

    reference_sha256 = (
        hashlib.sha256()
    )

    reference_sha3 = (
        hashlib.sha3_256()
    )

    bytes_processed = 0

    with TEST_FILE.open("rb") as file:
        while True:
            chunk = file.read(
                CHUNK_SIZE
            )

            if not chunk:
                break

            custom_sha256.update(
                chunk
            )

            custom_sha3.update(
                chunk
            )

            reference_sha256.update(
                chunk
            )

            reference_sha3.update(
                chunk
            )

            bytes_processed += len(
                chunk
            )

    print(
        "Обработано байт: "
        f"{bytes_processed}"
    )

    sha256_custom = (
        custom_sha256.hexdigest()
    )

    sha256_reference = (
        reference_sha256.hexdigest()
    )

    sha3_custom = (
        custom_sha3.hexdigest()
    )

    sha3_reference = (
        reference_sha3.hexdigest()
    )

    print("\nSHA-256:")
    print(
        f"CryptoCore: {sha256_custom}"
    )
    print(
        f"Reference:  {sha256_reference}"
    )

    print("\nSHA3-256:")
    print(
        f"CryptoCore: {sha3_custom}"
    )
    print(
        f"Reference:  {sha3_reference}"
    )

    sha256_ok = (
        sha256_custom
        == sha256_reference
    )

    sha3_ok = (
        sha3_custom
        == sha3_reference
    )

    return sha256_ok and sha3_ok


def main() -> int:
    try:
        create_large_file()

        print(
            f"Размер файла: "
            f"{TEST_FILE.stat().st_size} байт"
        )

        passed = test_large_file()

        if passed:
            print(
                "\nLarge file test: PASSED"
            )

            return 0

        print(
            "\nLarge file test: FAILED"
        )

        return 1

    finally:
        if TEST_FILE.exists():
            TEST_FILE.unlink()

            print(
                "Временный файл удалён."
            )


if __name__ == "__main__":
    raise SystemExit(main())