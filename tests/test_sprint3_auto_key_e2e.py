import os
import re
import subprocess
import sys


GENERATED_KEY_PATTERN = re.compile(
    r"\[INFO\] Generated random key:\s*"
    r"([0-9a-fA-F]{32})"
)


def run_cryptocore(arguments):
    environment = os.environ.copy()

    environment["PYTHONUTF8"] = "1"

    return subprocess.run(
        [
            sys.executable,
            "-m",
            "cryptocore",
            *arguments,
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=environment,
    )


def test_generated_key_full_round_trip(
    tmp_path,
):
    original_file = (
        tmp_path / "original.bin"
    )

    encrypted_file = (
        tmp_path / "encrypted.bin"
    )

    decrypted_file = (
        tmp_path / "decrypted.bin"
    )

    original_data = (
        b"CryptoCore Sprint 3 "
        b"automatic key generation test."
        b"\x00\x01\x02\x03\xff"
    )

    original_file.write_bytes(
        original_data
    )

    # Шифруем БЕЗ --key.
    encrypt_result = run_cryptocore([
        "--algorithm",
        "aes",
        "--mode",
        "ctr",
        "--encrypt",
        "--input",
        str(original_file),
        "--output",
        str(encrypted_file),
    ])

    assert (
        encrypt_result.returncode
        == 0
    )

    assert encrypted_file.exists()

    match = (
        GENERATED_KEY_PATTERN.search(
            encrypt_result.stdout
        )
    )

    assert match is not None, (
        "CryptoCore не вывел автоматически "
        "сгенерированный AES-ключ."
    )

    generated_key = (
        match.group(1)
    )

    assert len(generated_key) == 32

    # Теперь расшифровываем именно
    # напечатанным программой ключом.
    decrypt_result = run_cryptocore([
        "--algorithm",
        "aes",
        "--mode",
        "ctr",
        "--decrypt",
        "--key",
        generated_key,
        "--input",
        str(encrypted_file),
        "--output",
        str(decrypted_file),
    ])

    assert (
        decrypt_result.returncode
        == 0
    )

    assert decrypted_file.exists()

    restored_data = (
        decrypted_file.read_bytes()
    )

    assert (
        restored_data
        == original_data
    )