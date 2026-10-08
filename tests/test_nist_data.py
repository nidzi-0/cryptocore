from pathlib import Path

from cryptocore.nist_data import (
    generate_nist_test_file,
)


def test_generate_nist_test_file(
    tmp_path: Path,
):
    output_file = (
        tmp_path / "nist_test_data.bin"
    )

    size = 100_000

    bytes_written = generate_nist_test_file(
        output_file=output_file,
        total_size=size,
    )

    assert output_file.exists()
    assert bytes_written == size
    assert output_file.stat().st_size == size


def test_nist_file_is_not_constant(
    tmp_path: Path,
):
    output_file = (
        tmp_path / "nist_test_data.bin"
    )

    generate_nist_test_file(
        output_file=output_file,
        total_size=100_000,
    )

    data = output_file.read_bytes()

    assert len(set(data)) > 1