import os
import subprocess
import sys

from cryptocore.main import encrypt_data


KEY_HEX = (
    "00112233445566778899aabbccddeeff"
)

KEY = bytes.fromhex(
    KEY_HEX
)

CORRECT_AAD_HEX = (
    "aabbccddeeff"
)

WRONG_AAD_HEX = (
    "001122334455"
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


def create_gcm_file(
    tmp_path,
):
    plaintext_file = (
        tmp_path
        / "plaintext.bin"
    )

    encrypted_file = (
        tmp_path
        / "encrypted.bin"
    )

    plaintext = (
        b"CryptoCore Sprint 6 "
        b"authenticated encryption test."
        b"\x00\x01\x02\xff"
    )

    plaintext_file.write_bytes(
        plaintext
    )

    result = run_cryptocore([
        "--algorithm",
        "aes",
        "--mode",
        "gcm",
        "--encrypt",
        "--key",
        KEY_HEX,
        "--input",
        str(plaintext_file),
        "--output",
        str(encrypted_file),
        "--aad",
        CORRECT_AAD_HEX,
    ])

    assert (
        result.returncode
        == 0
    )

    assert encrypted_file.exists()

    return (
        plaintext,
        encrypted_file,
    )


def test_wrong_aad_causes_catastrophic_failure(
    tmp_path,
):
    _, encrypted_file = (
        create_gcm_file(
            tmp_path
        )
    )

    output_file = (
        tmp_path
        / "must_not_exist.bin"
    )

    result = run_cryptocore([
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
        str(output_file),
        "--aad",
        WRONG_AAD_HEX,
    ])

    assert (
        result.returncode
        != 0
    )

    assert (
        not output_file.exists()
    )

    assert (
        "Authentication failed"
        in result.stderr
    )


def test_ciphertext_tamper_causes_failure(
    tmp_path,
):
    _, encrypted_file = (
        create_gcm_file(
            tmp_path
        )
    )

    tampered_file = (
        tmp_path
        / "tampered_ciphertext.bin"
    )

    output_file = (
        tmp_path
        / "must_not_exist.bin"
    )

    data = bytearray(
        encrypted_file.read_bytes()
    )

    # Формат:
    # 12-byte nonce
    # ciphertext
    # 16-byte tag
    #
    # Меняем первый байт ciphertext.
    assert len(data) > 28

    data[12] ^= 0x01

    tampered_file.write_bytes(
        data
    )

    result = run_cryptocore([
        "--algorithm",
        "aes",
        "--mode",
        "gcm",
        "--decrypt",
        "--key",
        KEY_HEX,
        "--input",
        str(tampered_file),
        "--output",
        str(output_file),
        "--aad",
        CORRECT_AAD_HEX,
    ])

    assert (
        result.returncode
        != 0
    )

    assert (
        not output_file.exists()
    )

    assert (
        "Authentication failed"
        in result.stderr
    )


def test_tag_tamper_causes_failure(
    tmp_path,
):
    _, encrypted_file = (
        create_gcm_file(
            tmp_path
        )
    )

    tampered_file = (
        tmp_path
        / "tampered_tag.bin"
    )

    output_file = (
        tmp_path
        / "must_not_exist.bin"
    )

    data = bytearray(
        encrypted_file.read_bytes()
    )

    # Последний байт относится
    # к 16-байтовому GCM tag.
    data[-1] ^= 0x01

    tampered_file.write_bytes(
        data
    )

    result = run_cryptocore([
        "--algorithm",
        "aes",
        "--mode",
        "gcm",
        "--decrypt",
        "--key",
        KEY_HEX,
        "--input",
        str(tampered_file),
        "--output",
        str(output_file),
        "--aad",
        CORRECT_AAD_HEX,
    ])

    assert (
        result.returncode
        != 0
    )

    assert (
        not output_file.exists()
    )

    assert (
        "Authentication failed"
        in result.stderr
    )


def test_nonce_is_random_and_unique():
    nonces = set()

    for _ in range(1000):
        result, nonce = encrypt_data(
            data=b"nonce test",
            key=KEY,
            mode="gcm",
            aad=b"",
        )

        assert nonce is not None

        assert len(
            nonce
        ) == 12

        assert (
            result[:12]
            == nonce
        )

        nonces.add(
            nonce
        )

    assert len(
        nonces
    ) == 1000


def test_correct_aad_still_decrypts(
    tmp_path,
):
    (
        plaintext,
        encrypted_file,
    ) = create_gcm_file(
        tmp_path
    )

    output_file = (
        tmp_path
        / "restored.bin"
    )

    result = run_cryptocore([
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
        str(output_file),
        "--aad",
        CORRECT_AAD_HEX,
    ])

    assert (
        result.returncode
        == 0
    )

    assert output_file.exists()

    assert (
        output_file.read_bytes()
        == plaintext
    )