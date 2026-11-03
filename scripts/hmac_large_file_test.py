from pathlib import Path
import hashlib
import hmac

from cryptocore.digest import hmac_file


TEST_FILE = Path(
    "large_hmac_test.bin"
)

FILE_SIZE = (
    10 * 1024 * 1024
)

KEY = bytes.fromhex(
    "00112233445566778899aabbccddeeff"
)


def create_test_file():
    print(
        f"Создание файла: "
        f"{FILE_SIZE:,} байт"
    )

    block = bytes(
        range(256)
    )

    remaining = FILE_SIZE

    with TEST_FILE.open("wb") as file:
        while remaining > 0:
            part = block[
                :min(
                    len(block),
                    remaining,
                )
            ]

            file.write(part)

            remaining -= len(part)


def reference_hmac():
    mac = hmac.new(
        KEY,
        digestmod=hashlib.sha256,
    )

    with TEST_FILE.open("rb") as file:
        while True:
            chunk = file.read(
                8192
            )

            if not chunk:
                break

            mac.update(chunk)

    return mac.hexdigest()


def main():
    try:
        create_test_file()

        print(
            "Вычисление HMAC CryptoCore..."
        )

        result = hmac_file(
            str(TEST_FILE),
            KEY,
        )

        print(
            "Вычисление эталонного HMAC..."
        )

        expected = reference_hmac()

        print()
        print(
            f"CryptoCore: {result}"
        )

        print(
            f"Reference:  {expected}"
        )

        if result != expected:
            print(
                "Large HMAC test: FAILED"
            )

            return 1

        print(
            "Large HMAC test: PASSED"
        )

        return 0

    finally:
        if TEST_FILE.exists():
            TEST_FILE.unlink()

            print(
                "Временный файл удалён."
            )


if __name__ == "__main__":
    raise SystemExit(
        main()
    )