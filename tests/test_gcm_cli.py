import os
import re
import subprocess
import sys


KEY_HEX = (
    "00112233445566778899aabbccddeeff"
)

AAD_HEX = (
    "aabbccddeeff"
)

NONCE_PATTERN = re.compile(
    r"Nonce:\s*"
    r"([0-9A-Fa-f]{24})"
)


def run_cryptocore(
    arguments,
):
    environment = os.environ.copy()

    environment[
        "PYTHONUTF8"
    ] = "1"

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


def test_gcm_cli_round_trip(
    tmp_path,
):
    original_file = (
        tmp_path
        / "original.bin"
    )

    encrypted_file = (
        tmp_path
        / "encrypted.bin"
    )

    decrypted_file = (
        tmp_path
        / "decrypted.bin"
    )

    original_data = (
        b"CryptoCore Sprint 6 "
        b"GCM CLI round trip."
        b"\x00\x01\x02\x03\xff"
    )

    original_file.write_bytes(
        original_data
    )

    encryption = run_cryptocore([
        "--algorithm",
        "aes",
        "--mode",
        "gcm",
        "--encrypt",
        "--key",
        KEY_HEX,
        "--input",
        str(original_file),
        "--output",
        str(encrypted_file),
        "--aad",
        AAD_HEX,
    ])

    assert (
        encryption.returncode
        == 0
    )

    assert encrypted_file.exists()

    encrypted_data = (
        encrypted_file.read_bytes()
    )

    # 12 byte nonce
    # + ciphertext
    # + 16 byte tag
    assert len(
        encrypted_data
    ) == (
        12
        + len(original_data)
        + 16
    )

    nonce_match = (
        NONCE_PATTERN.search(
            encryption.stdout
        )
    )

    assert (
        nonce_match
        is not None
    )

    printed_nonce = bytes.fromhex(
        nonce_match.group(1)
    )

    assert len(
        printed_nonce
    ) == 12

    assert (
        encrypted_data[:12]
        == printed_nonce
    )

    decryption = run_cryptocore([
        "--algorithm",
        "aes",
        "--mode",
        "gcm",
        "--decrypt",
        "--key",
        KEY_HEX,
        "--input",
        str(encrypted_file),
        "--output",
        str(decrypted_file),
        "--aad",
        AAD_HEX,
    ])

    assert (
        decryption.returncode
        == 0
    )

    assert (
        decrypted_file.read_bytes()
        == original_data
    )


def test_gcm_cli_empty_aad(
    tmp_path,
):
    original_file = (
        tmp_path
        / "empty_aad_original.bin"
    )

    encrypted_file = (
        tmp_path
        / "empty_aad_encrypted.bin"
    )

    decrypted_file = (
        tmp_path
        / "empty_aad_decrypted.bin"
    )

    original_data = (
        b"GCM empty AAD test"
    )

    original_file.write_bytes(
        original_data
    )

    encryption = run_cryptocore([
        "--algorithm",
        "aes",
        "--mode",
        "gcm",
        "--encrypt",
        "--key",
        KEY_HEX,
        "--input",
        str(original_file),
        "--output",
        str(encrypted_file),
    ])

    assert (
        encryption.returncode
        == 0
    )

    decryption = run_cryptocore([
        "--algorithm",
        "aes",
        "--mode",
        "gcm",
        "--decrypt",
        "--key",
        KEY_HEX,
        "--input",
        str(encrypted_file),
        "--output",
        str(decrypted_file),
    ])

    assert (
        decryption.returncode
        == 0
    )

    assert (
        decrypted_file.read_bytes()
        == original_data
    )


def test_gcm_cli_explicit_nonce(
    tmp_path,
):
    original_file = (
        tmp_path
        / "original.bin"
    )

    encrypted_file = (
        tmp_path
        / "encrypted.bin"
    )

    ciphertext_tag_file = (
        tmp_path
        / "ciphertext_tag.bin"
    )

    decrypted_file = (
        tmp_path
        / "decrypted.bin"
    )

    original_data = (
        b"Explicit nonce GCM test"
    )

    original_file.write_bytes(
        original_data
    )

    encryption = run_cryptocore([
        "--algorithm",
        "aes",
        "--mode",
        "gcm",
        "--encrypt",
        "--key",
        KEY_HEX,
        "--input",
        str(original_file),
        "--output",
        str(encrypted_file),
        "--aad",
        AAD_HEX,
    ])

    assert (
        encryption.returncode
        == 0
    )

    complete_data = (
        encrypted_file.read_bytes()
    )

    nonce = (
        complete_data[:12]
    )

    ciphertext_and_tag = (
        complete_data[12:]
    )

    ciphertext_tag_file.write_bytes(
        ciphertext_and_tag
    )

    decryption = run_cryptocore([
        "--algorithm",
        "aes",
        "--mode",
        "gcm",
        "--decrypt",
        "--key",
        KEY_HEX,
        "--nonce",
        nonce.hex(),
        "--input",
        str(ciphertext_tag_file),
        "--output",
        str(decrypted_file),
        "--aad",
        AAD_HEX,
    ])

    assert (
        decryption.returncode
        == 0
    )

    assert (
        decrypted_file.read_bytes()
        == original_data
    )