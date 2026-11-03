from pathlib import Path

from cryptocore.hash.sha256 import SHA256
from cryptocore.hash.sha3_256 import SHA3_256


VECTOR_DIR = (
    Path(__file__).resolve().parent.parent
    / "tests"
    / "vectors"
    / "nist"
)


def sha256_digest(
    data: bytes,
) -> bytes:
    hasher = SHA256()
    hasher.update(data)
    return hasher.digest()


def sha3_256_digest(
    data: bytes,
) -> bytes:
    hasher = SHA3_256()
    hasher.update(data)
    return hasher.digest()


def load_monte_file(
    file_path: Path,
):
    seed = None
    checkpoints = []

    current_count = None

    with file_path.open(
        "r",
        encoding="utf-8",
    ) as file:
        for raw_line in file:
            line = raw_line.strip()

            if (
                not line
                or line.startswith("#")
                or line.startswith("[")
            ):
                continue

            if "=" not in line:
                continue

            name, value = (
                part.strip()
                for part in line.split(
                    "=",
                    1,
                )
            )

            if name == "Seed":
                seed = bytes.fromhex(
                    value
                )

            elif name == "COUNT":
                current_count = int(
                    value
                )

            elif name == "MD":
                if current_count is None:
                    continue

                checkpoints.append(
                    (
                        current_count,
                        value.lower(),
                    )
                )

                current_count = None

    if seed is None:
        raise ValueError(
            f"Seed not found in "
            f"{file_path.name}"
        )

    if not checkpoints:
        raise ValueError(
            f"No checkpoints found in "
            f"{file_path.name}"
        )

    return seed, checkpoints


def run_sha256_monte() -> None:
    file_path = (
        VECTOR_DIR
        / "SHA256Monte.rsp"
    )

    seed, checkpoints = (
        load_monte_file(
            file_path
        )
    )

    print(
        "NIST SHA-256 Monte Carlo"
    )

    for expected_count, expected_md in checkpoints:
        md0 = seed
        md1 = seed
        md2 = seed

        for _ in range(
            3,
            1003,
        ):
            message = (
                md0
                + md1
                + md2
            )

            digest = sha256_digest(
                message
            )

            md0 = md1
            md1 = md2
            md2 = digest

        seed = md2

        actual = seed.hex()

        if actual != expected_md:
            raise AssertionError(
                "\nSHA-256 Monte Carlo FAILED\n"
                f"COUNT:    {expected_count}\n"
                f"Expected: {expected_md}\n"
                f"Actual:   {actual}"
            )

        print(
            f"SHA-256 COUNT "
            f"{expected_count}: PASSED"
        )

    print(
        "NIST SHA-256 Monte Carlo: "
        "PASSED"
    )


def run_sha3_256_monte() -> None:
    file_path = (
        VECTOR_DIR
        / "SHA3_256Monte.rsp"
    )

    seed, checkpoints = (
        load_monte_file(
            file_path
        )
    )

    print()
    print(
        "NIST SHA3-256 Monte Carlo"
    )

    md = seed

    for expected_count, expected_md in checkpoints:
        for _ in range(
            1000
        ):
            md = sha3_256_digest(
                md
            )

        actual = md.hex()

        if actual != expected_md:
            raise AssertionError(
                "\nSHA3-256 Monte Carlo FAILED\n"
                f"COUNT:    {expected_count}\n"
                f"Expected: {expected_md}\n"
                f"Actual:   {actual}"
            )

        print(
            f"SHA3-256 COUNT "
            f"{expected_count}: PASSED"
        )

    print(
        "NIST SHA3-256 Monte Carlo: "
        "PASSED"
    )


def main() -> int:
    run_sha256_monte()
    run_sha3_256_monte()

    print()
    print(
        "All NIST Monte Carlo "
        "hash tests: PASSED"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )