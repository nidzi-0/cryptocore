# CryptoCore

CryptoCore — консольное приложение на Python для шифрования, расшифрования и вычисления криптографических хешей файлов.

Проект разработан в рамках учебной работы по дисциплине, связанной с методами и средствами криптографической защиты информации.

В проекте реализованы требования Sprint 1, Sprint 2, Sprint 3 и Sprint 4.

---

# Возможности проекта

CryptoCore поддерживает:

- AES-128 ECB;
- AES-128 CBC;
- AES-128 CFB-128;
- AES-128 OFB;
- AES-128 CTR;
- SHA-256;
- SHA3-256;
- автоматическую генерацию AES-ключей;
- генерацию IV;
- CSPRNG;
- потоковое хеширование файлов;
- проверку совместимости с OpenSSL и системными утилитами;
- статистическую проверку CSPRNG через NIST STS.

---

# Требования

Для работы проекта требуется:

- Python 3.10 или новее;
- PyCryptodome;
- pytest;
- OpenSSL — для проверки совместимости;
- NIST Statistical Test Suite 2.1.2 — для статистической проверки CSPRNG.

---

# Установка

Клонировать репозиторий:

```powershell
git clone https://github.com/nidzi-0/cryptocore.git
cd cryptocore
```

Создать виртуальное окружение:

```powershell
python -m venv .venv
```

Активировать виртуальное окружение:

```powershell
.venv\Scripts\Activate.ps1
```

Установить зависимости:

```powershell
pip install -e .
pip install -r requirements.txt
```

Проверить запуск:

```powershell
cryptocore --help
```

или:

```powershell
python -m cryptocore --help
```

---

# Шифрование AES-128

Поддерживаются режимы:

```text
ECB
CBC
CFB
OFB
CTR
```

Общий формат команды:

```text
cryptocore
    --algorithm aes
    --mode <ecb|cbc|cfb|ofb|ctr>
    <--encrypt|--decrypt>
    [--key <hex-key>]
    [--iv <hex-iv>]
    --input <input-file>
    [--output <output-file>]
```

Для AES-128 используется ключ длиной:

```text
16 байт
```

или:

```text
32 hexadecimal-символа
```

Пример:

```text
000102030405060708090a0b0c0d0e0f
```

---

# Автоматическая генерация AES-ключа

При шифровании параметр:

```text
--key
```

является необязательным.

Если ключ не передан, CryptoCore автоматически создаёт криптографически стойкий случайный ключ AES-128 длиной 16 байт.

Пример:

```powershell
cryptocore --algorithm aes --mode ctr --encrypt --input plaintext.txt --output ciphertext.bin
```

Пример вывода:

```text
[INFO] Generated random key: 1a2b3c4d5e6f7890fedcba9876543210
Шифрование успешно завершено.
Результат сохранён в: ciphertext.bin
IV: ...
```

Сгенерированный ключ:

- имеет длину 16 байт;
- предназначен для AES-128;
- выводится в stdout;
- выводится в hexadecimal-формате;
- не записывается в ciphertext.

Пользователь должен сохранить ключ самостоятельно.

Для расшифрования `--key` является обязательным.

---

# Пользовательский AES-ключ

Пользователь может передать собственный ключ:

```powershell
cryptocore --algorithm aes --mode cbc --encrypt --key 000102030405060708090a0b0c0d0e0f --input plaintext.txt --output ciphertext.bin
```

Ключ должен содержать ровно 16 байт.

---

# Предупреждение о слабых ключах

CryptoCore выполняет базовую проверку пользовательского AES-ключа.

Потенциально слабыми считаются:

- полностью повторяющиеся байты;
- полностью нулевой ключ;
- последовательность `00–0F`;
- обратная последовательность `0F–00`.

Пример:

```text
00000000000000000000000000000000
```

В этом случае выводится предупреждение:

```text
[WARNING] Обнаружен потенциально слабый AES-ключ: ...
```

Операция при этом не прерывается.

---

# CSPRNG

В проекте реализован отдельный модуль:

```text
src/cryptocore/csprng.py
```

Основная функция:

```python
generate_random_bytes(num_bytes: int) -> bytes
```

Для генерации случайных данных используется:

```python
os.urandom()
```

Стандартный модуль:

```python
random
```

для криптографических ключей и IV не используется.

CSPRNG применяется для:

- AES-128 ключей;
- IV;
- подготовки данных NIST STS.

---

# AES-128 ECB

ECB обрабатывает каждый блок независимо.

IV не используется.

Применяется PKCS#7 padding.

Шифрование:

```powershell
cryptocore --algorithm aes --mode ecb --encrypt --key 000102030405060708090a0b0c0d0e0f --input plaintext.txt --output encrypted_ecb.bin
```

Расшифрование:

```powershell
cryptocore --algorithm aes --mode ecb --decrypt --key 000102030405060708090a0b0c0d0e0f --input encrypted_ecb.bin --output decrypted_ecb.txt
```

---

# AES-128 CBC

CBC использует 16-байтовый IV.

Для CBC применяется PKCS#7 padding.

Каждый plaintext-блок объединяется через XOR с предыдущим ciphertext-блоком.

Для первого блока используется IV.

Шифрование:

```powershell
cryptocore --algorithm aes --mode cbc --encrypt --key 000102030405060708090a0b0c0d0e0f --input plaintext.txt --output encrypted_cbc.bin
```

Расшифрование:

```powershell
cryptocore --algorithm aes --mode cbc --decrypt --key 000102030405060708090a0b0c0d0e0f --input encrypted_cbc.bin --output decrypted_cbc.txt
```

Формат файла:

```text
<16-byte IV><ciphertext>
```

---

# AES-128 CFB-128

CFB реализован с размером сегмента 128 бит.

Padding не используется.

Шифрование:

```powershell
cryptocore --algorithm aes --mode cfb --encrypt --key 000102030405060708090a0b0c0d0e0f --input plaintext.txt --output encrypted_cfb.bin
```

Расшифрование:

```powershell
cryptocore --algorithm aes --mode cfb --decrypt --key 000102030405060708090a0b0c0d0e0f --input encrypted_cfb.bin --output decrypted_cfb.txt
```

---

# AES-128 OFB

OFB работает как потоковый режим.

Padding не используется.

Шифрование:

```powershell
cryptocore --algorithm aes --mode ofb --encrypt --key 000102030405060708090a0b0c0d0e0f --input plaintext.txt --output encrypted_ofb.bin
```

Расшифрование:

```powershell
cryptocore --algorithm aes --mode ofb --decrypt --key 000102030405060708090a0b0c0d0e0f --input encrypted_ofb.bin --output decrypted_ofb.txt
```

---

# AES-128 CTR

В CTR IV используется как начальное значение 128-битного счётчика.

Для каждого блока:

1. счётчик шифруется AES;
2. результат используется как keystream;
3. keystream объединяется с данными через XOR;
4. счётчик увеличивается.

Padding не используется.

Шифрование:

```powershell
cryptocore --algorithm aes --mode ctr --encrypt --key 000102030405060708090a0b0c0d0e0f --input plaintext.txt --output encrypted_ctr.bin
```

Расшифрование:

```powershell
cryptocore --algorithm aes --mode ctr --decrypt --key 000102030405060708090a0b0c0d0e0f --input encrypted_ctr.bin --output decrypted_ctr.txt
```

---

# Работа с IV

Для режимов:

```text
CBC
CFB
OFB
CTR
```

используется IV длиной 16 байт.

ECB IV не использует.

IV создаётся автоматически через общий CSPRNG.

Формат файла:

```text
<16-byte IV><ciphertext>
```

AES-ключ в файл не записывается.

При расшифровании файла CryptoCore может автоматически извлечь IV из первых 16 байт.

Также поддерживается явное указание IV:

```powershell
cryptocore --algorithm aes --mode cbc --decrypt --key 000102030405060708090a0b0c0d0e0f --iv AABBCCDDEEFF00112233445566778899 --input openssl_cipher.bin --output restored.txt
```

---

# Padding

Режимы:

```text
ECB
CBC
```

используют PKCS#7 padding.

Режимы:

```text
CFB
OFB
CTR
```

работают без padding.

---

# Работа с файлами

CryptoCore работает с файлами в бинарном режиме.

Чтение:

```python
rb
```

Запись:

```python
wb
```

Поэтому программа поддерживает:

- текст;
- изображения;
- архивы;
- документы;
- произвольные бинарные данные.

---

# OpenSSL interoperability для AES

Проверка выполняется скриптом:

```text
scripts/openssl_interop_test.py
```

Запуск:

```powershell
$env:Path += ";C:\Program Files\OpenSSL-Win64\bin"
python .\scripts\openssl_interop_test.py
```

Проверяются:

```text
ECB
CBC
CFB
OFB
CTR
```

Для каждого режима выполняются проверки:

```text
CryptoCore -> OpenSSL
OpenSSL -> CryptoCore
```

Дополнительно для ECB выполняется побайтовое сравнение ciphertext.

Итог:

```text
Result: 11/11 checks passed
OpenSSL interoperability: PASSED
```

---

# NIST STS

Для статистической проверки CSPRNG использовалась:

```text
NIST Statistical Test Suite 2.1.2
```

Подготовка данных выполняется через:

```text
scripts/generate_nist_data.py
```

Создаётся:

```text
nist_test_data.bin
```

размером:

```text
10 000 000 байт
```

Данные формируются через:

```python
generate_random_bytes(...)
```

---

# Параметры NIST STS

Размер одной последовательности:

```text
1 000 000 бит
```

Количество последовательностей:

```text
80
```

Общий объём:

```text
80 000 000 бит
```

Формат:

```text
Binary
```

Команда запуска:

```bash
./assess 1000000
```

Были выбраны все 15 статистических тестов.

---

# Выполненные тесты NIST STS

Выполнены:

1. Frequency;
2. Block Frequency;
3. Cumulative Sums;
4. Runs;
5. Longest Run of Ones;
6. Binary Matrix Rank;
7. Discrete Fourier Transform;
8. Non-overlapping Template Matching;
9. Overlapping Template Matching;
10. Maurer's Universal Statistical;
11. Approximate Entropy;
12. Random Excursions;
13. Random Excursions Variant;
14. Serial;
15. Linear Complexity.

Основные результаты:

```text
Frequency               80/80
BlockFrequency          79/80
CumulativeSums          80/80
Runs                    79/80
LongestRun              79/80
Rank                    79/80
FFT                     80/80
OverlappingTemplate     78/80
Universal               79/80
ApproximateEntropy      79/80
Serial                  80/80 и 79/80
LinearComplexity        80/80
```

Для Random Excursions и Random Excursions Variant результаты находились в диапазоне:

```text
51/53 – 53/53
```

Итог:

```text
NIST STS: PASSED
```

---

# Sprint 4 — криптографические хеш-функции

В Sprint 4 добавлены криптографические хеш-функции для проверки целостности данных.

Реализованы:

```text
SHA-256
SHA3-256
```

Оба алгоритма реализованы самостоятельно.

---

# SHA-256

Файл:

```text
src/cryptocore/hash/sha256.py
```

SHA-256 реализован без использования `hashlib` внутри основной реализации.

Реализованы:

- обработка 512-битных блоков;
- 8 начальных значений состояния;
- 64 константы;
- функция Ch;
- функция Maj;
- функции Σ0 и Σ1;
- функции σ0 и σ1;
- message schedule;
- 64 раунда compression function;
- SHA-256 padding;
- 64-битное представление длины сообщения;
- incremental update;
- digest;
- hexadecimal digest.

Поддерживаются методы:

```python
update()
digest()
hexdigest()
```

---

# SHA3-256

Файл:

```text
src/cryptocore/hash/sha3_256.py
```

SHA3-256 также реализован самостоятельно.

Реализованы:

- Keccak sponge construction;
- Keccak-f[1600];
- состояние 1600 бит;
- rate 1088 бит;
- capacity 512 бит;
- 24 раунда;
- Theta;
- Rho;
- Pi;
- Chi;
- Iota;
- domain separation SHA-3;
- padding;
- получение 256-битного результата.

`hashlib.sha3_256()` внутри основной реализации не используется.

---

# Команда dgst

Для вычисления хешей добавлена отдельная команда:

```text
cryptocore dgst
```

Поддерживаются:

```text
--algorithm
--input
--output
```

Поддерживаемые алгоритмы:

```text
sha256
sha3-256
```

Параметры шифрования:

```text
--key
--mode
--encrypt
--decrypt
--iv
```

команда `dgst` не принимает.

---

# SHA-256 файла

Пример:

```powershell
cryptocore dgst --algorithm sha256 --input plaintext.txt
```

Результат:

```text
85cacb699d2c90431881e2b94d5f99a7ba4263252d0a86cb7f6baaee40c53466  plaintext.txt
```

Формат:

```text
HASH_VALUE  INPUT_FILE_PATH
```

Хеш выводится строчными hexadecimal-символами.

---

# SHA3-256 файла

Пример:

```powershell
cryptocore dgst --algorithm sha3-256 --input plaintext.txt
```

Результат:

```text
5ceabced06ecc36f0f0f53b6b67fc89920a7430eb7a20fb23c8fdaf62b3fa6b3  plaintext.txt
```

---

# Сохранение хеша в файл

Пример:

```powershell
cryptocore dgst --algorithm sha256 --input plaintext.txt --output plaintext.sha256
```

В файл записывается строка:

```text
HASH_VALUE  INPUT_FILE_PATH
```

То есть формат совпадает с форматом stdout.

---

# Потоковая обработка файлов

При хешировании файлы не загружаются полностью в оперативную память.

Они открываются в бинарном режиме:

```python
rb
```

и обрабатываются частями:

```text
8192 байт
```

Схема:

```text
input file
    |
    v
8192-byte chunk
    |
    v
update()
    |
    v
next chunk
    |
    v
final digest
```

Это позволяет обрабатывать большие файлы при постоянном объёме используемой памяти.

---

# Known-Answer Tests SHA-256

Проверен хеш пустого сообщения:

```text
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

Для:

```text
abc
```

получено:

```text
ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad
```

Также проверен вектор:

```text
abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq
```

Ожидаемый результат:

```text
248d6a61d20638b8e5c026930c3e6039a33ce45964ff2167f6ecedd419db06c1
```

---

# Known-Answer Tests SHA3-256

Пустое сообщение:

```text
a7ffc6f8bf1ed76651c14756a061d662f580ff4de43b49fa82d80a4b80f8434a
```

Для:

```text
abc
```

получено:

```text
3a985da74fe225b2045c172d6bd390bd855f086e3e9d525b46bfe24511431532
```

---

# Interoperability SHA-256

SHA-256 CryptoCore проверен через системную Linux-утилиту:

```bash
sha256sum plaintext.txt
```

CryptoCore:

```text
85cacb699d2c90431881e2b94d5f99a7ba4263252d0a86cb7f6baaee40c53466
```

`sha256sum`:

```text
85cacb699d2c90431881e2b94d5f99a7ba4263252d0a86cb7f6baaee40c53466
```

Результат:

```text
SHA-256 interoperability: PASSED
```

---

# Interoperability SHA3-256

SHA3-256 проверен через OpenSSL 3.5.5:

```bash
openssl dgst -sha3-256 plaintext.txt
```

CryptoCore:

```text
5ceabced06ecc36f0f0f53b6b67fc89920a7430eb7a20fb23c8fdaf62b3fa6b3
```

OpenSSL:

```text
5ceabced06ecc36f0f0f53b6b67fc89920a7430eb7a20fb23c8fdaf62b3fa6b3
```

Результат:

```text
SHA3-256 OpenSSL interoperability: PASSED
```

В использованной WSL-системе команда `/usr/bin/sha3sum` оказалась другой утилитой `sum` и не поддерживала параметр `-a 256`.

Попытка установки требуемой версии через:

```bash
sudo apt install libdigest-sha3-perl
```

не завершилась из-за недоступности Ubuntu-репозитория.

Поэтому независимая проверка SHA3-256 была выполнена через OpenSSL.

---

# Avalanche Effect

Добавлен тест:

```text
tests/test_hash_avalanche.py
```

В исходных данных изменяется один бит.

После этого сравниваются 256-битные результаты.

Подсчитывается количество различающихся битов.

Допустимый диапазон:

```text
100 < changed_bits < 156
```

Проверяются:

```text
SHA-256
SHA3-256
```

---

# Проверка файла больше 1 GB

Добавлен скрипт:

```text
scripts/hash_large_file_test.py
```

Создаётся временный файл размером:

```text
1 073 741 825 байт
```

Это на один байт больше 1 GiB.

CryptoCore хеширует его по частям.

Проверяются:

```text
SHA-256
SHA3-256
```

Результаты сравниваются с эталонными реализациями.

Итог:

```text
Large file test: PASSED
```

После проверки временный файл автоматически удаляется.

---

# Автоматические тесты Sprint 4

Добавлены:

```text
tests/test_sha256.py
tests/test_sha3_256.py
tests/test_digest.py
tests/test_digest_cli.py
tests/test_hash_avalanche.py
```

Проверяются:

- SHA-256;
- SHA3-256;
- пустое сообщение;
- известные тестовые векторы;
- сообщения различной длины;
- incremental update;
- повторный вызов digest;
- продолжение update после digest;
- обработка ошибок;
- chunked hashing;
- CLI `dgst`;
- `--output`;
- запрет AES-параметров для `dgst`;
- stdout;
- avalanche effect.

---

# Проверка всех автоматических тестов

Запуск:

```powershell
pytest -v
```

Все тесты должны завершаться без:

```text
FAILED
ERROR
```

---

# Проверка сохранения Sprint 1–3

После реализации Sprint 4 повторно выполнена полная проверка AES через OpenSSL:

```powershell
python .\scripts\openssl_interop_test.py
```

Итог:

```text
Result: 11/11 checks passed
OpenSSL interoperability: PASSED
```

Проверены:

```text
ECB
CBC
CFB
OFB
CTR
```

Следовательно, добавление hash-функциональности не нарушило работу предыдущих Sprint.

---

# Структура проекта

```text
cryptocore/
|
|-- src/
|   `-- cryptocore/
|       |-- __init__.py
|       |-- __main__.py
|       |-- main.py
|       |-- cli_parser.py
|       |-- digest.py
|       |-- digest_cli.py
|       |-- file_io.py
|       |-- padding.py
|       |-- iv.py
|       |-- csprng.py
|       |-- nist_data.py
|       |
|       |-- hash/
|       |   |-- __init__.py
|       |   |-- sha256.py
|       |   `-- sha3_256.py
|       |
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
|   |-- test_modes_integration.py
|   |-- test_csprng.py
|   |-- test_nist_data.py
|   |-- test_sha256.py
|   |-- test_sha3_256.py
|   |-- test_digest.py
|   |-- test_digest_cli.py
|   `-- test_hash_avalanche.py
|
|-- scripts/
|   |-- round_trip_test.py
|   |-- openssl_interop_test.py
|   |-- generate_nist_data.py
|   |-- hash_interop_test.py
|   `-- hash_large_file_test.py
|
|-- plaintext.txt
|-- pyproject.toml
|-- requirements.txt
|-- README.md
`-- .gitignore
```

---

# Итоги Sprint 1

Реализованы:

- структура проекта;
- CLI;
- AES-128 ECB;
- PKCS#7;
- файловый ввод-вывод;
- round-trip;
- проверка AES-128 ECB через OpenSSL.

---

# Итоги Sprint 2

Реализованы:

- AES-128 CBC;
- AES-128 CFB-128;
- AES-128 OFB;
- AES-128 CTR;
- самостоятельная логика режимов поверх AES-примитива;
- генерация IV;
- формат `<IV><ciphertext>`;
- явный `--iv`;
- двусторонняя совместимость с OpenSSL.

---

# Итоги Sprint 3

Реализованы:

- отдельный CSPRNG;
- `generate_random_bytes()`;
- использование `os.urandom()`;
- автоматическая генерация AES-128 ключа;
- вывод ключа в stdout;
- отсутствие ключа в ciphertext;
- обязательный ключ при расшифровании;
- предупреждение о потенциально слабых ключах;
- единый CSPRNG для IV;
- тест 1000 уникальных случайных значений;
- базовая проверка распределения битов;
- генерация данных NIST STS;
- полный NIST STS;
- все 15 статистических тестов.

Итог:

```text
NIST STS: PASSED
```

---

# Итоги Sprint 4

Реализованы:

- SHA-256 с нуля;
- SHA3-256 с нуля;
- Keccak-f[1600];
- отдельный CLI `dgst`;
- `--algorithm sha256`;
- `--algorithm sha3-256`;
- `--input`;
- `--output`;
- lowercase hexadecimal output;
- бинарное чтение;
- chunked processing;
- Known-Answer Tests;
- тест пустого сообщения;
- interoperability;
- avalanche effect;
- тест файла больше 1 GB;
- сохранена совместимость Sprint 1–3.

Проверка AES после Sprint 4:

```text
Result: 11/11 checks passed
OpenSSL interoperability: PASSED
```

Проверка SHA-256:

```text
SHA-256 interoperability: PASSED
```

Проверка SHA3-256:

```text
SHA3-256 OpenSSL interoperability: PASSED
```

Проверка большого файла:

```text
Large file test: PASSED
```

