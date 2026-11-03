from cryptocore.hash.sha256 import SHA256
from cryptocore.hash.sha3_256 import SHA3_256


def count_different_bits(
    first_digest: str,
    second_digest: str,
) -> int:
    first = bytes.fromhex(first_digest)
    second = bytes.fromhex(second_digest)

    return sum(
        (first_byte ^ second_byte).bit_count()
        for first_byte, second_byte
        in zip(first, second)
    )


def test_sha256_avalanche_effect():
    original = b"Hello, world!"

    modified = bytearray(original)

    # Меняем ровно один бит.
    modified[0] ^= 0x01

    hash_original = SHA256.hash(
        original
    )

    hash_modified = SHA256.hash(
        bytes(modified)
    )

    different_bits = count_different_bits(
        hash_original,
        hash_modified,
    )

    print(
        "SHA-256 changed bits: "
        f"{different_bits}/256"
    )

    assert 100 < different_bits < 156


def test_sha3_256_avalanche_effect():
    original = b"Hello, world!"

    modified = bytearray(original)

    # Меняем ровно один бит.
    modified[0] ^= 0x01

    hash_original = SHA3_256.hash(
        original
    )

    hash_modified = SHA3_256.hash(
        bytes(modified)
    )

    different_bits = count_different_bits(
        hash_original,
        hash_modified,
    )

    print(
        "SHA3-256 changed bits: "
        f"{different_bits}/256"
    )

    assert 100 < different_bits < 156