import shutil
import subprocess

from cryptocore.kdf.pbkdf2 import (
    pbkdf2_hmac_sha256,
)


def _get_openssl_command():
    windows_openssl = shutil.which(
        "openssl"
    )

    if windows_openssl is not None:
        return [
            windows_openssl,
        ]

    wsl = shutil.which(
        "wsl"
    )

    if wsl is not None:
        check = subprocess.run(
            [
                wsl,
                "openssl",
                "version",
            ],
            capture_output=True,
        )

        if check.returncode == 0:
            return [
                wsl,
                "openssl",
            ]

    raise RuntimeError(
        "OpenSSL не найден ни в Windows, "
        "ни в WSL."
    )


def test_pbkdf2_matches_openssl():
    password = "password"

    salt_hex = "73616c74"

    salt = bytes.fromhex(
        salt_hex
    )

    iterations = 1000
    length = 32

    our_key = pbkdf2_hmac_sha256(
        password=password,
        salt=salt,
        iterations=iterations,
        dklen=length,
    )

    openssl_command = (
        _get_openssl_command()
    )

    result = subprocess.run(
        openssl_command
        + [
            "kdf",
            "-keylen",
            str(length),
            "-binary",
            "-kdfopt",
            "digest:SHA256",
            "-kdfopt",
            f"pass:{password}",
            "-kdfopt",
            f"hexsalt:{salt_hex}",
            "-kdfopt",
            f"iter:{iterations}",
            "PBKDF2",
        ],
        capture_output=True,
        check=True,
    )

    openssl_key = result.stdout

    assert openssl_key == our_key