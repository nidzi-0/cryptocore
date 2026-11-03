import hashlib
import hmac
from pathlib import Path
import sys

try:
    import resource
except ImportError:
    resource = None

from cryptocore.digest import (
    CHUNK_SIZE,
    hmac_file,
)


MIB = 1024 * 1024

EXTRA_MEMORY = 64 * MIB
FILE_OVER_LIMIT = 32 * MIB

KEY = bytes.fromhex(
    "00112233445566778899aabbccddeeff"
)

TEST_FILE = Path(
    "hmac_memory_limited_test.bin"
)


def get_current_virtual_memory() -> int:
    """
    Возвращает текущий VmSize процесса Linux.
    """

    status_file = Path(
        "/proc/self/status"
    )

    content = status_file.read_text(
        encoding="utf-8"
    )

    for line in content.splitlines():
        if line.startswith("VmSize:"):
            parts = line.split()

            kib = int(
                parts[1]
            )

            return kib * 1024

    raise RuntimeError(
        "Не удалось определить VmSize "
        "из /proc/self/status."
    )


def create_sparse_file(
    file_size: int,
) -> None:
    with TEST_FILE.open("wb") as file:
        file.seek(
            file_size - 1
        )

        file.write(
            b"\x00"
        )


def reference_hmac() -> str:
    mac = hmac.new(
        KEY,
        digestmod=hashlib.sha256,
    )

    with TEST_FILE.open("rb") as file:
        while True:
            chunk = file.read(
                CHUNK_SIZE
            )

            if not chunk:
                break

            mac.update(
                chunk
            )

    return mac.hexdigest()


def main() -> int:
    if resource is None:
        print(
            "This test must be run "
            "under Linux or WSL."
        )

        return 2

    try:
        current_vm = (
            get_current_virtual_memory()
        )

        memory_limit = (
            current_vm
            + EXTRA_MEMORY
        )

        file_size = (
            memory_limit
            + FILE_OVER_LIMIT
        )

        print(
            "Current virtual memory: "
            f"{current_vm:,} bytes"
        )

        print(
            "Memory limit for HMAC: "
            f"{memory_limit:,} bytes"
        )

        print(
            "Test file size: "
            f"{file_size:,} bytes"
        )

        assert (
            file_size
            > memory_limit
        )

        print()
        print(
            "Creating sparse test file..."
        )

        create_sparse_file(
            file_size
        )

        actual_file_size = (
            TEST_FILE.stat().st_size
        )

        assert (
            actual_file_size
            == file_size
        )

        print(
            "Computing reference HMAC..."
        )

        expected = (
            reference_hmac()
        )

        print(
            "Reference: "
            f"{expected}"
        )

        # После вычисления эталона
        # искусственно ограничиваем
        # адресное пространство процесса.
        resource.setrlimit(
            resource.RLIMIT_AS,
            (
                memory_limit,
                memory_limit,
            ),
        )

        print()
        print(
            "Memory limit enabled."
        )

        print(
            "Computing CryptoCore HMAC..."
        )

        result = hmac_file(
            str(TEST_FILE),
            KEY,
        )

        print(
            "CryptoCore: "
            f"{result}"
        )

        if result != expected:
            print(
                "Memory-limited HMAC "
                "test: FAILED"
            )

            return 1

        print()
        print(
            "File size is larger than "
            "the process memory limit."
        )

        print(
            "Chunk size: "
            f"{CHUNK_SIZE} bytes"
        )

        print()
        print(
            "Memory-limited HMAC "
            "test: PASSED"
        )

        return 0

    finally:
        if TEST_FILE.exists():
            TEST_FILE.unlink()

            print(
                "Temporary file removed."
            )


if __name__ == "__main__":
    raise SystemExit(
        main()
    )