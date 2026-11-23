from cryptocore.derive import parse_salt
import subprocess
import sys


import pytest


def run_cryptocore(
    *args,
):
    return subprocess.run(
        [
            sys.executable,
            "-m",
            "cryptocore.main",
            "derive",
            *args,
        ],
        capture_output=True,
        text=True,
    )


def test_derive_with_fixed_salt():
    result = run_cryptocore(
        "--password",
        "password",
        "--salt",
        "73616c74",
        "--iterations",
        "1",
        "--length",
        "32",
    )

    assert result.returncode == 0

    output = (
        result.stdout
        .strip()
        .split()
    )

    assert len(output) == 2

    key_hex = output[0]
    salt_hex = output[1]

    assert key_hex == (
        "120fb6cffcf8b32c"
        "43e7225256c4f837"
        "a86548c92ccc3548"
        "0805987cb70be17b"
    )

    assert salt_hex == "73616c74"


def test_derive_default_length():
    result = run_cryptocore(
        "--password",
        "password",
        "--salt",
        "73616c74",
        "--iterations",
        "1",
    )

    assert result.returncode == 0

    key_hex, _ = (
        result.stdout
        .strip()
        .split()
    )

    assert len(
        bytes.fromhex(
            key_hex
        )
    ) == 32


def test_derive_generated_salt_is_16_bytes():
    result = run_cryptocore(
        "--password",
        "password",
        "--iterations",
        "1",
    )

    assert result.returncode == 0

    _, salt_hex = (
        result.stdout
        .strip()
        .split()
    )

    salt = bytes.fromhex(
        salt_hex
    )

    assert len(salt) == 16


def test_generated_salts_are_different():
    salts = set()

    for _ in range(20):
        result = run_cryptocore(
            "--password",
            "password",
            "--iterations",
            "1",
        )

        assert result.returncode == 0

        _, salt_hex = (
            result.stdout
            .strip()
            .split()
        )

        salts.add(
            salt_hex
        )

    assert len(salts) == 20


@pytest.mark.parametrize(
    "length",
    [
        1,
        16,
        32,
        64,
        100,
    ],
)
def test_derive_requested_length(
    length,
):
    result = run_cryptocore(
        "--password",
        "password",
        "--salt",
        "73616c74",
        "--iterations",
        "1",
        "--length",
        str(length),
    )

    assert result.returncode == 0

    key_hex, _ = (
        result.stdout
        .strip()
        .split()
    )

    assert len(
        bytes.fromhex(
            key_hex
        )
    ) == length


def test_output_file_contains_raw_key(
    tmp_path,
):
    output_file = (
        tmp_path
        / "derived_key.bin"
    )

    result = run_cryptocore(
        "--password",
        "password",
        "--salt",
        "73616c74",
        "--iterations",
        "1",
        "--length",
        "32",
        "--output",
        str(output_file),
    )

    assert result.returncode == 0

    assert output_file.exists()

    data = output_file.read_bytes()

    assert len(data) == 32

    assert data.hex() == (
        "120fb6cffcf8b32c"
        "43e7225256c4f837"
        "a86548c92ccc3548"
        "0805987cb70be17b"
    )


def test_invalid_salt_rejected():
    result = run_cryptocore(
        "--password",
        "password",
        "--salt",
        "not-hex",
    )

    assert result.returncode != 0

    assert (
        "Salt"
        in result.stderr
    )


def test_zero_iterations_rejected():
    result = run_cryptocore(
        "--password",
        "password",
        "--iterations",
        "0",
    )

    assert result.returncode != 0


def test_zero_length_rejected():
    result = run_cryptocore(
        "--password",
        "password",
        "--length",
        "0",
    )

    assert result.returncode != 0
def test_1000_generated_salts_are_unique():
    salts = set()

    for _ in range(1000):
        salt = parse_salt(
            None
        )

        assert len(salt) == 16

        salts.add(
            salt
        )

    assert len(salts) == 1000