# CryptoCore

CryptoCore — консольное приложение на Python для шифрования и расшифрования файлов с использованием алгоритма AES-128.

Проект реализован в рамках учебной работы по дисциплине, связанной с методами и средствами криптографической защиты информации.

## Поддерживаемые режимы

CryptoCore поддерживает следующие режимы AES-128:

- ECB
- CBC
- CFB-128
- OFB
- CTR

Для выполнения самого AES используется библиотека PyCryptodome.

Логика режимов CBC, CFB, OFB и CTR реализована самостоятельно поверх AES-примитива.

## Требования

- Python 3.10 или новее
- PyCryptodome
- pytest
- OpenSSL — для проверки совместимости

## Установка

Клонировать репозиторий:

```bash
git clone https://github.com/nidzi-0/cryptocore.git
cd cryptocore
```

Создать виртуальное окружение:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Установить проект и зависимости:

```bash
pip install -e .
pip install -r requirements.txt
```

После установки должна быть доступна команда:

```bash
cryptocore --help
```

## Общий формат команды

```text
cryptocore
    --algorithm aes
    --mode <ecb|cbc|cfb|ofb|ctr>
    <--encrypt|--decrypt>
    --key <hex-key>
    [--iv <hex-iv>]
    --input <input-file>
    [--output <output-file>]
```

AES-128 использует ключ длиной 16 байт, то есть 32 шестнадцатеричных символа.

Пример ключа:

```text
000102030405060708090a0b0c0d0e0f
```

## ECB

ECB не использует IV.

### Шифрование

```powershell
cryptocore --algorithm aes --mode ecb --encrypt --key 000102030405060708090a0b0c0d0e0f --input plaintext.txt --output encrypted_ecb.bin
```

### Расшифрование

```powershell
cryptocore --algorithm aes --mode ecb --decrypt --key 000102030405060708090a0b0c0d0e0f --input encrypted_ecb.bin --output decrypted_ecb.txt
```

Для ECB используется PKCS#7 padding.

## CBC

При шифровании IV создаётся автоматически.

```powershell
cryptocore --algorithm aes --mode cbc --encrypt --key 000102030405060708090a0b0c0d0e0f --input plaintext.txt --output encrypted_cbc.bin
```

В начале выходного файла сохраняется 16-байтовый IV.

При обычном расшифровании указывать IV не требуется:

```powershell
cryptocore --algorithm aes --mode cbc --decrypt --key 000102030405060708090a0b0c0d0e0f --input encrypted_cbc.bin --output decrypted_cbc.txt
```

CryptoCore автоматически считывает первые 16 байт файла как IV.

Для CBC используется PKCS#7 padding.

## CFB-128

```powershell
cryptocore --algorithm aes --mode cfb --encrypt --key 000102030405060708090a0b0c0d0e0f --input plaintext.txt --output encrypted_cfb.bin
```

Расшифрование:

```powershell
cryptocore --algorithm aes --mode cfb --decrypt --key 000102030405060708090a0b0c0d0e0f --input encrypted_cfb.bin --output decrypted_cfb.txt
```

CFB работает с сегментом размером 128 бит.

Padding не используется.

## OFB

```powershell
cryptocore --algorithm aes --mode ofb --encrypt --key 000102030405060708090a0b0c0d0e0f --input plaintext.txt --output encrypted_ofb.bin
```

Расшифрование:

```powershell
cryptocore --algorithm aes --mode ofb --decrypt --key 000102030405060708090a0b0c0d0e0f --input encrypted_ofb.bin --output decrypted_ofb.txt
```

Padding не используется.

## CTR

```powershell
cryptocore --algorithm aes --mode ctr --encrypt --key 000102030405060708090a0b0c0d0e0f --input plaintext.txt --output encrypted_ctr.bin
```

Расшифрование:

```powershell
cryptocore --algorithm aes --mode ctr --decrypt --key 000102030405060708090a0b0c0d0e0f --input encrypted_ctr.bin --output decrypted_ctr.txt
```

Начальным значением 128-битного счётчика является IV.

После обработки каждого блока счётчик увеличивается на единицу.

Padding не используется.

## Работа с IV

Для режимов:

- CBC
- CFB
- OFB
- CTR

используется IV длиной 16 байт.

При шифровании IV генерируется автоматически с помощью:

```python
os.urandom(16)
```

Пользователь не передаёт `--iv` при шифровании.

Формат зашифрованного файла:

```text
<16-byte IV><ciphertext>
```

То есть первые 16 байт выходного файла содержат IV, после чего располагается ciphertext.

При расшифровании файла, созданного CryptoCore, параметр `--iv` не требуется.

Программа сама извлекает IV из первых 16 байт.

## Явное указание IV

Параметр `--iv` используется при расшифровании внешнего ciphertext, например созданного OpenSSL.

Пример:

```powershell
cryptocore --algorithm aes --mode cbc --decrypt --key 000102030405060708090a0b0c0d0e0f --iv AABBCCDDEEFF00112233445566778899 --input openssl_cipher.bin --output decrypted.txt
```

В этом случае весь входной файл считается ciphertext, а IV берётся из параметра `--iv`.

Передавать `--iv` при шифровании запрещено, так как IV создаётся автоматически.

ECB параметр `--iv` не использует.

## Padding

Режимы ECB и CBC используют PKCS#7 padding.

Режимы:

- CFB
- OFB
- CTR

не используют padding.

Поэтому для CFB, OFB и CTR размер ciphertext совпадает с размером исходных данных.

## Работа с бинарными файлами

CryptoCore открывает входные и выходные файлы в бинарном режиме.

Поэтому приложение может обрабатывать:

- текстовые файлы;
- изображения;
- архивы;
- бинарные документы;
- другие типы файлов.

## Проверка тестов

Для запуска всех автоматических тестов:

```powershell
pytest
```

Подробный вывод:

```powershell
pytest -v
```

В проекте проверяются:

- PKCS#7;
- ECB;
- CBC;
- CFB-128;
- OFB;
- CTR;
- генерация и обработка IV;
- корректность CLI;
- обработка бинарных данных;
- неполные блоки;
- известные тестовые векторы;
- round-trip;
- интеграция режимов с файловым форматом.

## Round-trip

Основной принцип проверки:

```text
original
   |
encrypt
   |
ciphertext
   |
decrypt
   |
restored
```

Файлы `original` и `restored` должны полностью совпадать побайтово.

## Совместимость с OpenSSL

Для проверки совместимости требуется установленный OpenSSL.

Проверить его наличие:

```powershell
openssl version
```

Если OpenSSL установлен в:

```text
C:\Program Files\OpenSSL-Win64\bin
```

его можно временно добавить в PATH текущего PowerShell:

```powershell
$env:Path += ";C:\Program Files\OpenSSL-Win64\bin"
```

### Автоматическая проверка

В проекте находится сценарий:

```text
scripts/openssl_interop_test.py
```

Запуск:

```powershell
python scripts/openssl_interop_test.py
```

Он проверяет режимы:

```text
CBC
CFB
OFB
CTR
```

в обоих направлениях:

```text
CryptoCore -> OpenSSL
OpenSSL -> CryptoCore
```

Итого выполняется 8 проверок совместимости.

Ожидаемый итог:

```text
Result: 8/8 checks passed
OpenSSL interoperability: PASSED
```

## CryptoCore -> OpenSSL вручную

CryptoCore записывает файл в формате:

```text
IV + ciphertext
```

OpenSSL необходимо передавать только ciphertext, поэтому сначала требуется отделить первые 16 байт.

Пример для CBC.

Шифрование CryptoCore:

```powershell
cryptocore --algorithm aes --mode cbc --encrypt --key 000102030405060708090a0b0c0d0e0f --input plaintext.txt --output encrypted.bin
```

Извлечь IV и ciphertext можно через Python:

```powershell
python -c "from pathlib import Path; d=Path('encrypted.bin').read_bytes(); print(d[:16].hex()); Path('ciphertext.bin').write_bytes(d[16:])"
```

Команда напечатает IV.

После этого ciphertext можно расшифровать OpenSSL:

```powershell
openssl enc -aes-128-cbc -d -K 000102030405060708090a0b0c0d0e0f -iv <IV_HEX> -in ciphertext.bin -out openssl_decrypted.txt
```

Вместо `<IV_HEX>` необходимо указать IV, полученный предыдущей командой.

Аналогично используются:

```text
-aes-128-cfb
-aes-128-ofb
-aes-128-ctr
```

## OpenSSL -> CryptoCore вручную

Пример CBC.

Шифрование OpenSSL:

```powershell
openssl enc -aes-128-cbc -K 000102030405060708090a0b0c0d0e0f -iv AABBCCDDEEFF00112233445566778899 -in plaintext.txt -out openssl_cipher.bin
```

Расшифрование CryptoCore:

```powershell
cryptocore --algorithm aes --mode cbc --decrypt --key 000102030405060708090a0b0c0d0e0f --iv AABBCCDDEEFF00112233445566778899 --input openssl_cipher.bin --output restored.txt
```

После этого `restored.txt` должен побайтово совпадать с `plaintext.txt`.

## Структура проекта

```text
cryptocore/
|
|-- src/
|   `-- cryptocore/
|       |-- __init__.py
|       |-- __main__.py
|       |-- main.py
|       |-- cli_parser.py
|       |-- file_io.py
|       |-- padding.py
|       |-- iv.py
|       `-- modes/
|           |-- __init__.py
|           |-- ecb.py
|           |-- cbc.py
|           |-- cfb.py
|           |-- ofb.py
|           `-- ctr.py
|
|-- tests/
|   |-- test_padding.py
|   |-- test_ecb.py
|   |-- test_cbc.py
|   |-- test_cfb.py
|   |-- test_ofb.py
|   |-- test_ctr.py
|   |-- test_iv.py
|   |-- test_cli.py
|   `-- test_modes_integration.py
|
|-- scripts/
|   |-- round_trip_test.py
|   `-- openssl_interop_test.py
|
|-- plaintext.txt
|-- pyproject.toml
|-- requirements.txt
|-- README.md
`-- .gitignore
```

## Реализация режимов

Для реализации AES используется:

```python
Crypto.Cipher.AES
```

При этом логика новых режимов написана вручную.

CBC:

```text
plaintext block
      XOR
previous ciphertext / IV
       |
      AES
       |
ciphertext block
```

CFB:

```text
IV / previous ciphertext
          |
         AES
          |
      keystream
          |
         XOR
          |
      ciphertext
```

OFB:

```text
IV
 |
AES
 |
output block
 |
AES
 |
next output block
```

Полученные выходные блоки используются как поток байтов для XOR с данными.

CTR:

```text
counter
   |
  AES
   |
keystream
   |
  XOR
   |
data
```

После каждого блока счётчик увеличивается на единицу.

## Безопасность IV

Для каждого нового шифрования CBC, CFB, OFB или CTR создаётся новый случайный IV:

```python
os.urandom(16)
```

IV не является секретным и поэтому сохраняется непосредственно перед ciphertext.

Ключ AES при этом в файл не записывается.

## Запуск как Python-модуль

Помимо команды `cryptocore`, приложение можно запустить так:

```powershell
python -m cryptocore --algorithm aes --mode cbc --encrypt --key 000102030405060708090a0b0c0d0e0f --input plaintext.txt --output encrypted.bin
```