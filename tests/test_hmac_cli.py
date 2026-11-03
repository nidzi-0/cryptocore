import hashlib
import hmac

import pytest

from cryptocore.digest import (
    digest_main,
    hmac_file,
    parse_hmac_key,
)
from cryptocore.digest_cli import (
    get_digest_arguments,
)


KEY_HEX = (
    "00112233445566778899aabbccddeeff"
)

KEY = bytes.fromhex(
    KEY_HEX
)


def test_hmac_cli_requires_key():
    with pytest.raises(
        SystemExit
    ):
        get_digest_arguments([
            "--algorithm",
            "sha256",
            "--hmac",
            "--input",
            "file.txt",
        ])


def test_hmac_cli_accepts_key():
    args = get_digest_arguments([
        "--algorithm",
        "sha256",
        "--hmac",
        "--key",
        KEY_HEX,
        "--input",
        "file.txt",
    ])

    assert args.hmac is True
    assert args.key == KEY_HEX


def test_hmac_rejects_sha3():
    with pytest.raises(
        SystemExit
    ):
        get_digest_arguments([
            "--algorithm",
            "sha3-256",
            "--hmac",
            "--key",
            KEY_HEX,
            "--input",
            "file.txt",
        ])


def test_parse_hmac_key():
    assert parse_hmac_key(
        KEY_HEX
    ) == KEY


def test_parse_hmac_key_rejects_invalid_hex():
    with pytest.raises(
        ValueError
    ):
        parse_hmac_key(
            "not-a-key"
        )


def test_hmac_file_matches_stdlib(
    tmp_path,
):
    input_file = (
        tmp_path / "message.bin"
    )

    data = (
        b"CryptoCore Sprint 5 "
        b"HMAC test"
    )

    input_file.write_bytes(
        data
    )

    result = hmac_file(
        str(input_file),
        KEY,
    )

    expected = hmac.new(
        KEY,
        data,
        hashlib.sha256,
    ).hexdigest()

    assert result == expected


def test_hmac_empty_file(
    tmp_path,
):
    input_file = (
        tmp_path / "empty.bin"
    )

    input_file.write_bytes(
        b""
    )

    result = hmac_file(
        str(input_file),
        KEY,
    )

    expected = hmac.new(
        KEY,
        b"",
        hashlib.sha256,
    ).hexdigest()

    assert result == expected


def test_hmac_output_file(
    tmp_path,
    capsys,
):
    input_file = (
        tmp_path / "message.txt"
    )

    output_file = (
        tmp_path / "message.hmac"
    )

    input_file.write_bytes(
        b"original content"
    )

    result = digest_main([
        "--algorithm",
        "sha256",
        "--hmac",
        "--key",
        KEY_HEX,
        "--input",
        str(input_file),
        "--output",
        str(output_file),
    ])

    captured = (
        capsys.readouterr()
    )

    assert result == 0
    assert captured.out == ""

    content = output_file.read_text(
        encoding="utf-8"
    )

    expected = hmac.new(
        KEY,
        b"original content",
        hashlib.sha256,
    ).hexdigest()

    assert content.startswith(
        expected
    )


def test_hmac_verify_success(
    tmp_path,
    capsys,
):
    input_file = (
        tmp_path / "message.txt"
    )

    hmac_file_path = (
        tmp_path / "message.hmac"
    )

    input_file.write_bytes(
        b"original content"
    )

    assert digest_main([
        "--algorithm",
        "sha256",
        "--hmac",
        "--key",
        KEY_HEX,
        "--input",
        str(input_file),
        "--output",
        str(hmac_file_path),
    ]) == 0

    result = digest_main([
        "--algorithm",
        "sha256",
        "--hmac",
        "--key",
        KEY_HEX,
        "--input",
        str(input_file),
        "--verify",
        str(hmac_file_path),
    ])

    captured = (
        capsys.readouterr()
    )

    assert result == 0

    assert (
        "[OK] HMAC verification successful"
        in captured.out
    )


def test_hmac_detects_modified_file(
    tmp_path,
    capsys,
):
    input_file = (
        tmp_path / "message.txt"
    )

    hmac_file_path = (
        tmp_path / "message.hmac"
    )

    input_file.write_bytes(
        b"original content"
    )

    assert digest_main([
        "--algorithm",
        "sha256",
        "--hmac",
        "--key",
        KEY_HEX,
        "--input",
        str(input_file),
        "--output",
        str(hmac_file_path),
    ]) == 0

    # Изменяем содержимое файла.
    input_file.write_bytes(
        b"modified content"
    )

    result = digest_main([
        "--algorithm",
        "sha256",
        "--hmac",
        "--key",
        KEY_HEX,
        "--input",
        str(input_file),
        "--verify",
        str(hmac_file_path),
    ])

    captured = (
        capsys.readouterr()
    )

    assert result == 1

    assert (
        "[ERROR] HMAC verification failed"
        in captured.err
    )


def test_hmac_detects_wrong_key(
    tmp_path,
    capsys,
):
    input_file = (
        tmp_path / "message.txt"
    )

    hmac_file_path = (
        tmp_path / "message.hmac"
    )

    input_file.write_bytes(
        b"original content"
    )

    assert digest_main([
        "--algorithm",
        "sha256",
        "--hmac",
        "--key",
        KEY_HEX,
        "--input",
        str(input_file),
        "--output",
        str(hmac_file_path),
    ]) == 0

    wrong_key = (
        "ffeeddccbbaa99887766554433221100"
    )

    result = digest_main([
        "--algorithm",
        "sha256",
        "--hmac",
        "--key",
        wrong_key,
        "--input",
        str(input_file),
        "--verify",
        str(hmac_file_path),
    ])

    captured = (
        capsys.readouterr()
    )

    assert result == 1

    assert (
        "[ERROR] HMAC verification failed"
        in captured.err
    )
def test_hmac_cli_process_exit_codes(
    tmp_path,
):
    import subprocess
    import sys

    input_file = (
        tmp_path / "message.txt"
    )

    hmac_file_path = (
        tmp_path / "message.hmac"
    )

    input_file.write_bytes(
        b"original content"
    )

    key = (
        "00112233445566778899aabbccddeeff"
    )

    # Генерируем HMAC через настоящий CLI.
    generate = subprocess.run(
        [
            sys.executable,
            "-m",
            "cryptocore",
            "dgst",
            "--algorithm",
            "sha256",
            "--hmac",
            "--key",
            key,
            "--input",
            str(input_file),
            "--output",
            str(hmac_file_path),
        ],
        capture_output=True,
        text=True,
    )

    assert generate.returncode == 0
    assert hmac_file_path.exists()

    # Правильный файл + правильный ключ.
    verify_ok = subprocess.run(
        [
            sys.executable,
            "-m",
            "cryptocore",
            "dgst",
            "--algorithm",
            "sha256",
            "--hmac",
            "--key",
            key,
            "--input",
            str(input_file),
            "--verify",
            str(hmac_file_path),
        ],
        capture_output=True,
        text=True,
    )

    assert verify_ok.returncode == 0

    assert (
        "[OK] HMAC verification successful"
        in verify_ok.stdout
    )

    # Изменяем файл.
    input_file.write_bytes(
        b"modified content"
    )

    verify_failed = subprocess.run(
        [
            sys.executable,
            "-m",
            "cryptocore",
            "dgst",
            "--algorithm",
            "sha256",
            "--hmac",
            "--key",
            key,
            "--input",
            str(input_file),
            "--verify",
            str(hmac_file_path),
        ],
        capture_output=True,
        text=True,
    )

    assert verify_failed.returncode != 0

    assert (
        "[ERROR] HMAC verification failed"
        in verify_failed.stderr
    )