from pathlib import Path

from cryptocore.file_io import read_file, write_file
from cryptocore.modes.ecb import encrypt_ecb, decrypt_ecb


KEY = bytes.fromhex(
    "000102030405060708090a0b0c0d0e0f"
)

def main():
    project_root = Path(__file__).resolve().parent.parent

    original_file = project_root / "roundtrip_original.txt"
    encrypted_file = project_root / "roundtrip_encrypted.bin"
    decrypted_file = project_root / "roundtrip_decrypted.txt"

    original_data = (
        b"CryptoCore round-trip test.\n"
        b"AES-128 ECB mode with PKCS#7 padding.\n"
    )

    print("1. Создание исходного файла...")

    write_file(
        str(original_file),
        original_data
    )

    print(f"Исходный файл: {original_file}")

    print("\n2. Чтение исходного файла...")

    data = read_file(
        str(original_file)
    )

    print(
        f"Прочитано байт: {len(data)}"
    )

    print("\n3. Шифрование...")

    encrypted_data = encrypt_ecb(
        data=data,
        key=KEY
    )

    write_file(
        str(encrypted_file),
        encrypted_data
    )

    print(
        f"Зашифрованный файл: {encrypted_file}"
    )

    print(
        f"Размер ciphertext: {len(encrypted_data)} байт"
    )

    print("\n4. Расшифрование...")

    encrypted_data_from_file = read_file(
        str(encrypted_file)
    )

    decrypted_data = decrypt_ecb(
        data=encrypted_data_from_file,
        key=KEY
    )

    write_file(
        str(decrypted_file),
        decrypted_data
    )

    print(
        f"Расшифрованный файл: {decrypted_file}"
    )

    print("\n5. Сравнение файлов...")

    original = read_file(
        str(original_file)
    )

    decrypted = read_file(
        str(decrypted_file)
    )

    if original == decrypted:
        print(
            "PASS: расшифрованный файл полностью "
            "совпадает с исходным."
        )
        return 0

    print(
        "FAIL: расшифрованный файл отличается "
        "от исходного."
    )

    return 1


if __name__ == "__main__":
    raise SystemExit(main())