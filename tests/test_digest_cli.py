import pytest

from cryptocore.digest import digest_main
from cryptocore.digest_cli import (
    get_digest_arguments,
)


def test_digest_cli_sha256():
    args = get_digest_arguments([
        "--algorithm",
        "sha256",
        "--input",
        "document.pdf",
    ])

    assert args.algorithm == "sha256"
    assert args.input_file == "document.pdf"


def test_digest_cli_sha3_256():
    args = get_digest_arguments([
        "--algorithm",
        "sha3-256",
        "--input",
        "document.pdf",
    ])

    assert args.algorithm == "sha3-256"


@pytest.mark.parametrize(
    "forbidden_argument",
    [
        "--key",
        "--mode",
        "--encrypt",
        "--decrypt",
        "--iv",
    ],
)
def test_digest_rejects_encryption_arguments(
    forbidden_argument,
):
    argv = [
        "--algorithm",
        "sha256",
        "--input",
        "file.bin",
        forbidden_argument,
    ]

    if forbidden_argument in {
        "--key",
        "--mode",
        "--iv",
    }:
        argv.append("value")

    with pytest.raises(SystemExit):
        get_digest_arguments(argv)


def test_digest_stdout(
    tmp_path,
    capsys,
):
    input_file = (
        tmp_path / "abc.txt"
    )

    input_file.write_bytes(b"abc")

    result = digest_main([
        "--algorithm",
        "sha256",
        "--input",
        str(input_file),
    ])

    captured = capsys.readouterr()

    assert result == 0

    assert (
        "ba7816bf8f01cfea414140de5dae2223"
        "b00361a396177a9cb410ff61f20015ad"
    ) in captured.out

    assert str(input_file) in captured.out


def test_digest_output_file(
    tmp_path,
    capsys,
):
    input_file = (
        tmp_path / "abc.txt"
    )

    output_file = (
        tmp_path / "abc.sha256"
    )

    input_file.write_bytes(b"abc")

    result = digest_main([
        "--algorithm",
        "sha256",
        "--input",
        str(input_file),
        "--output",
        str(output_file),
    ])

    captured = capsys.readouterr()

    assert result == 0
    assert captured.out == ""

    content = output_file.read_text(
        encoding="utf-8"
    )

    assert (
        "ba7816bf8f01cfea414140de5dae2223"
        "b00361a396177a9cb410ff61f20015ad"
    ) in content

    assert str(input_file) in content