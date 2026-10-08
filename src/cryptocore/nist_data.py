from pathlib import Path

from .csprng import generate_random_bytes


DEFAULT_OUTPUT_FILE = Path("nist_test_data.bin")
DEFAULT_TOTAL_SIZE = 10_000_000
CHUNK_SIZE = 4096


def generate_nist_test_file(
    output_file: Path = DEFAULT_OUTPUT_FILE,
    total_size: int = DEFAULT_TOTAL_SIZE,
) -> int:
    if total_size <= 0:
        raise ValueError(
            "Размер тестового файла должен "
            "быть больше нуля."
        )

    bytes_written = 0

    with output_file.open("wb") as file:
        while bytes_written < total_size:
            current_chunk_size = min(
                CHUNK_SIZE,
                total_size - bytes_written
            )

            random_data = generate_random_bytes(
                current_chunk_size
            )

            file.write(random_data)

            bytes_written += len(random_data)

    return bytes_written