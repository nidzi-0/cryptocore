from pathlib import Path

from cryptocore.hash.sha256 import SHA256
from cryptocore.hash.sha3_256 import SHA3_256


VECTOR_DIR = (
    Path(__file__).parent
    / "vectors"
    / "nist"
)


def sha256_hex(data: bytes) -> str:
    hasher = SHA256()
    hasher.update(data)
    return hasher.hexdigest()


def sha3_256_hex(data: bytes) -> str:
    hasher = SHA3_256()
    hasher.update(data)
    return hasher.hexdigest()


def load_message_vectors(
    file_path: Path,
):
    """
    Читает NIST .rsp файлы формата:

    Len = ...
    Msg = ...
    MD = ...
    """

    current = {}

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

            if name == "Len":
                current["len"] = int(
                    value
                )

            elif name == "Msg":
                current["msg"] = value

            elif name == "MD":
                current["md"] = (
                    value.lower()
                )

                if {
                    "len",
                    "msg",
                    "md",
                }.issubset(current):
                    yield current

                    current = {}


def message_from_vector(
    vector,
) -> bytes:
    length_bits = vector["len"]

    if length_bits == 0:
        return b""

    if length_bits % 8 != 0:
        raise ValueError(
            "Byte-oriented NIST vector "
            f"имеет Len={length_bits}, "
            "который не кратен 8."
        )

    message = bytes.fromhex(
        vector["msg"]
    )

    expected_length = (
        length_bits // 8
    )

    if len(message) != expected_length:
        raise ValueError(
            "Размер Msg не совпадает "
            f"с Len={length_bits}."
        )

    return message


def check_vector_file(
    filename: str,
    hash_function,
) -> None:
    file_path = (
        VECTOR_DIR / filename
    )

    assert file_path.exists(), (
        f"NIST vector file not found: "
        f"{file_path}"
    )

    count = 0

    for vector in load_message_vectors(
        file_path
    ):
        message = message_from_vector(
            vector
        )

        result = hash_function(
            message
        )

        assert result == vector["md"], (
            f"NIST vector failed\n"
            f"File: {filename}\n"
            f"Len: {vector['len']}\n"
            f"Expected: {vector['md']}\n"
            f"Actual:   {result}"
        )

        count += 1

    assert count > 0, (
        f"No NIST vectors found "
        f"in {filename}"
    )

    print(
        f"{filename}: "
        f"{count} vectors PASSED"
    )


def test_nist_sha256_short_messages():
    check_vector_file(
        "SHA256ShortMsg.rsp",
        sha256_hex,
    )


def test_nist_sha256_long_messages():
    check_vector_file(
        "SHA256LongMsg.rsp",
        sha256_hex,
    )


def test_nist_sha3_256_short_messages():
    check_vector_file(
        "SHA3_256ShortMsg.rsp",
        sha3_256_hex,
    )


def test_nist_sha3_256_long_messages():
    check_vector_file(
        "SHA3_256LongMsg.rsp",
        sha3_256_hex,
    )