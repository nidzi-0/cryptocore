import re
import shutil
import subprocess
import tempfile
from pathlib import Path

from cryptocore.digest import hash_file


HEX_DIGEST_PATTERN = re.compile(
    r"\b[0-9a-fA-F]{64}\b"
)


def run_command(
    command: list[str],
) -> str:
    result = subprocess.run(
        command,
        check=True,
        capture_output=True,
        text=True,
    )

    return result.stdout.strip()


def extract_digest(output: str) -> str:
    match = HEX_DIGEST_PATTERN.search(
        output
    )

    if match is None:
        raise RuntimeError(
            "Не удалось извлечь хеш "
            f"из вывода системной утилиты: {output}"
        )

    return match.group(0).lower()


def get_system_sha256(
    file_path: Path,
) -> tuple[str, str]:
    if shutil.which("sha256sum"):
        output = run_command([
            "sha256sum",
            str(file_path),
        ])

        return (
            extract_digest(output),
            "sha256sum",
        )

    if shutil.which("openssl"):
        output = run_command([
            "openssl",
            "dgst",
            "-sha256",
            str(file_path),
        ])

        return (
            extract_digest(output),
            "OpenSSL SHA-256",
        )

    raise RuntimeError(
        "Не найдена системная утилита "
        "для проверки SHA-256."
    )


def get_system_sha3_256(
    file_path: Path,
) -> tuple[str, str]:
    if shutil.which("sha3sum"):
        output = run_command([
            "sha3sum",
            "-a",
            "256",
            str(file_path),
        ])

        return (
            extract_digest(output),
            "sha3sum -a 256",
        )

    if shutil.which("sha3-256sum"):
        output = run_command([
            "sha3-256sum",
            str(file_path),
        ])

        return (
            extract_digest(output),
            "sha3-256sum",
        )

    if shutil.which("openssl"):
        output = run_command([
            "openssl",
            "dgst",
            "-sha3-256",
            str(file_path),
        ])

        return (
            extract_digest(output),
            "OpenSSL SHA3-256",
        )

    raise RuntimeError(
        "Не найдена системная утилита "
        "для проверки SHA3-256."
    )


def main() -> int:
    data = (
        b"CryptoCore Sprint 4 "
        b"hash interoperability test."
        b"\x00\x01\x02\x03\xff"
    )

    with tempfile.TemporaryDirectory() as directory:
        test_file = (
            Path(directory)
            / "interop_test.bin"
        )

        test_file.write_bytes(data)

        print(
            "CryptoCore hash interoperability test"
        )

        print("\n[SHA-256]")

        cryptocore_sha256 = hash_file(
            str(test_file),
            "sha256",
        )

        system_sha256, sha256_tool = (
            get_system_sha256(
                test_file
            )
        )

        print(
            "CryptoCore: "
            f"{cryptocore_sha256}"
        )

        print(
            f"{sha256_tool}: "
            f"{system_sha256}"
        )

        sha256_passed = (
            cryptocore_sha256
            == system_sha256
        )

        print(
            "PASS"
            if sha256_passed
            else "FAIL"
        )

        print("\n[SHA3-256]")

        cryptocore_sha3 = hash_file(
            str(test_file),
            "sha3-256",
        )

        system_sha3, sha3_tool = (
            get_system_sha3_256(
                test_file
            )
        )

        print(
            "CryptoCore: "
            f"{cryptocore_sha3}"
        )

        print(
            f"{sha3_tool}: "
            f"{system_sha3}"
        )

        sha3_passed = (
            cryptocore_sha3
            == system_sha3
        )

        print(
            "PASS"
            if sha3_passed
            else "FAIL"
        )

    if (
        sha256_passed
        and sha3_passed
    ):
        print(
            "\nHash interoperability: PASSED"
        )

        return 0

    print(
        "\nHash interoperability: FAILED"
    )

    return 1


if __name__ == "__main__":
    raise SystemExit(main())