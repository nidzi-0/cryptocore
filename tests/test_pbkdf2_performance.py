import time

import pytest

from cryptocore.kdf.pbkdf2 import (
    pbkdf2_hmac_sha256,
)


@pytest.mark.parametrize(
    "iterations",
    [
        10_000,
        100_000,
    ],
)
def test_pbkdf2_performance(
    iterations,
):
    start = time.perf_counter()

    result = pbkdf2_hmac_sha256(
        password=b"performance-test",
        salt=b"cryptocore-salt",
        iterations=iterations,
        dklen=32,
    )

    elapsed = (
        time.perf_counter()
        - start
    )

    assert len(result) == 32

    print(
        f"\nPBKDF2-SHA256 "
        f"{iterations:,} iterations: "
        f"{elapsed:.3f} s"
    )


@pytest.mark.slow
def test_pbkdf2_one_million_iterations():
    start = time.perf_counter()

    result = pbkdf2_hmac_sha256(
        password=b"performance-test",
        salt=b"cryptocore-salt",
        iterations=1_000_000,
        dklen=32,
    )

    elapsed = (
        time.perf_counter()
        - start
    )

    assert len(result) == 32

    print(
        "\nPBKDF2-SHA256 "
        "1,000,000 iterations: "
        f"{elapsed:.3f} s"
    )