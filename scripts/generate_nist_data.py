from cryptocore.nist_data import (
    DEFAULT_OUTPUT_FILE,
    DEFAULT_TOTAL_SIZE,
    generate_nist_test_file,
)


def main() -> int:
    print(
        "Подготовка случайных данных "
        "для NIST STS..."
    )

    bytes_written = generate_nist_test_file()

    print(
        f"Создан файл: {DEFAULT_OUTPUT_FILE}"
    )

    print(
        f"Размер: {bytes_written} байт"
    )

    print(
        f"Размер: "
        f"{bytes_written / 1_000_000:.2f} MB"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())