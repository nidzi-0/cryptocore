import pytest

from cryptocore.csprng import generate_random_bytes


def test_generate_random_bytes_length():
    data = generate_random_bytes(16)

    assert isinstance(data, bytes)
    assert len(data) == 16


def test_generate_different_random_values():
    first = generate_random_bytes(16)
    second = generate_random_bytes(16)

    assert first != second


def test_key_uniqueness():
    keys = [
        generate_random_bytes(16)
        for _ in range(1000)
    ]

    assert len(keys) == 1000
    assert len(set(keys)) == 1000


def test_basic_bit_distribution():
    keys = [
        generate_random_bytes(16)
        for _ in range(1000)
    ]

    total_bits = 0
    one_bits = 0

    for key in keys:
        total_bits += len(key) * 8

        for byte in key:
            one_bits += byte.bit_count()

    one_ratio = one_bits / total_bits

    assert 0.45 <= one_ratio <= 0.55


def test_zero_size_rejected():
    with pytest.raises(ValueError):
        generate_random_bytes(0)


def test_negative_size_rejected():
    with pytest.raises(ValueError):
        generate_random_bytes(-1)


def test_non_integer_size_rejected():
    with pytest.raises(TypeError):
        generate_random_bytes("16")


def test_os_random_error(monkeypatch):

    def failing_urandom(_):
        raise OSError(
            "System random source unavailable"
        )

    monkeypatch.setattr(
        "cryptocore.csprng.os.urandom",
        failing_urandom
    )

    with pytest.raises(
        RuntimeError,
        match="Не удалось получить"
    ):
        generate_random_bytes(16)