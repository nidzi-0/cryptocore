# CryptoCore

CryptoCore — учебное консольное приложение на Python для выполнения криптографических операций с файлами.

Проект последовательно развивается по Sprint 1–5 и на текущем этапе включает:

- AES-128 ECB;
- AES-128 CBC;
- AES-128 CFB-128;
- AES-128 OFB;
- AES-128 CTR;
- PKCS#7 padding;
- генерацию IV;
- CSPRNG;
- автоматическую генерацию AES-128 ключей;
- SHA-256;
- SHA3-256;
- HMAC-SHA256;
- потоковую обработку файлов;
- проверку целостности и подлинности;
- автоматические тесты;
- официальные NIST test vectors;
- NIST Monte Carlo tests;
- проверку совместимости с OpenSSL и системными утилитами;
- статистическую проверку CSPRNG через NIST STS.

Репозиторий:

```text
https://github.com/nidzi-0/cryptocore
```

---

# Требования

Для запуска проекта требуется:

- Python 3.10 или новее;
- PyCryptodome;
- pytest;
- OpenSSL — для interoperability-проверок;
- WSL/Linux — для некоторых системных проверок;
- NIST Statistical Test Suite 2.1.2 — для статистической проверки CSPRNG.

---

# Установка

Клонирование репозитория:

```powershell
git clone https://github.com/nidzi-0/cryptocore.git
cd cryptocore
```

Создание виртуального окружения:

```powershell
python -m venv .venv
```

Активация:

```powershell
.venv\Scripts\Activate.ps1
```

Установка проекта:

```powershell
pip install -e .
```

Установка зависимостей:

```powershell
pip install -r requirements.txt
```

Проверка запуска:

```powershell
cryptocore --help
```

или:

```powershell
python -m cryptocore --help
```

---

# Sprint 1 — AES-128 ECB

Цель Sprint 1 — создать базовую структуру CryptoCore и реализовать AES-128 в режиме ECB.

Реализованы:

- CLI;
- AES-128 ECB;
- PKCS#7 padding;
- файловый ввод-вывод;
- обработка ошибок;
- автоматические тесты;
- round-trip test;
- OpenSSL interoperability.

---

# AES-128 ECB

AES работает с блоками размером:

```text
16 байт
```

AES-128 использует ключ длиной:

```text
16 байт
```

или:

```text
32 hexadecimal-символа
```

Пример ключа:

```text
000102030405060708090a0b0c0d0e0f
```

Шифрование:

```powershell
cryptocore --algorithm aes --mode ecb --encrypt --key 000102030405060708090a0b0c0d0e0f --input plaintext.txt --output encrypted_ecb.bin
```

Расшифрование:

```powershell
cryptocore --algorithm aes --mode ecb --decrypt --key 000102030405060708090a0b0c0d0e0f --input encrypted_ecb.bin --output decrypted_ecb.txt
```

ECB не использует IV.

Для AES-примитива применяется:

```python
Crypto.Cipher.AES
```

из библиотеки PyCryptodome.

Логика ECB, разбиение данных на блоки и padding реализованы в коде проекта.

---

# PKCS#7

Режимы:

```text
ECB
CBC
```

используют PKCS#7 padding.

Если длина сообщения уже кратна размеру блока AES, добавляется полный блок padding.

Режимы:

```text
CFB
OFB
CTR
```

padding не используют.

---

# Файловый ввод-вывод

CryptoCore работает с файлами в бинарном режиме.

Используются режимы:

```python
rb
wb
```

Это позволяет корректно обрабатывать:

- текстовые файлы;
- бинарные файлы;
- данные, содержащие нулевые байты;
- изображения;
- архивы;
- другие произвольные файлы.

---

# Default output

Параметр:

```text
--output
```

можно не указывать.

В этом случае имя выходного файла формируется автоматически.

При шифровании:

```text
<input>.enc
```

При расшифровании:

```text
<input>.dec
```

---

# Round-trip test Sprint 1

Для проверки используется:

```text
scripts/round_trip_test.py
```

Запуск:

```powershell
python .\scripts\round_trip_test.py
```

Проверяется:

```text
исходный файл
    ↓
AES-128 ECB encryption
    ↓
ciphertext
    ↓
AES-128 ECB decryption
    ↓
восстановленный файл
```

Исходный и восстановленный файлы должны полностью совпасть.

---

# Sprint 2 — дополнительные режимы AES

В Sprint 2 добавлены:

- CBC;
- CFB-128;
- OFB;
- CTR;
- генерация IV;
- параметр `--iv`;
- формат `<IV><ciphertext>`;
- двусторонняя совместимость с OpenSSL.

Логика CBC, CFB, OFB и CTR реализована самостоятельно поверх AES-примитива.

---

# AES-128 CBC

CBC использует IV длиной:

```text
16 байт
```

При шифровании каждый plaintext-блок объединяется через XOR с предыдущим ciphertext-блоком.

Для первого блока используется IV.

CBC использует PKCS#7 padding.

Шифрование:

```powershell
cryptocore --algorithm aes --mode cbc --encrypt --key 000102030405060708090a0b0c0d0e0f --input plaintext.txt --output encrypted_cbc.bin
```

Расшифрование:

```powershell
cryptocore --algorithm aes --mode cbc --decrypt --key 000102030405060708090a0b0c0d0e0f --input encrypted_cbc.bin --output decrypted_cbc.txt
```

Формат зашифрованного файла:

```text
<16-byte IV><ciphertext>
```

---

# AES-128 CFB-128

CFB реализован с размером сегмента:

```text
128 бит
```

CFB работает как потоковый режим.

Padding не используется.

Шифрование:

```powershell
cryptocore --algorithm aes --mode cfb --encrypt --key 000102030405060708090a0b0c0d0e0f --input plaintext.txt --output encrypted_cfb.bin
```

Расшифрование:

```powershell
cryptocore --algorithm aes --mode cfb --decrypt --key 000102030405060708090a0b0c0d0e0f --input encrypted_cfb.bin --output decrypted_cfb.txt
```

Неполный последний блок обрабатывается без изменения его размера.

---

# AES-128 OFB

OFB работает как потоковый режим.

Keystream формируется независимо от plaintext.

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

1. значение счётчика шифруется AES;
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

используется IV длиной:

```text
16 байт
```

ECB IV не использует.

При обычном шифровании IV генерируется автоматически.

Пользователь не должен передавать `--iv` при шифровании.

Если `--iv` указан вместе с `--encrypt`, CLI завершает выполнение с ошибкой.

Формат выходного файла:

```text
<16-byte IV><ciphertext>
```

При расшифровании без `--iv` CryptoCore:

1. читает первые 16 байт файла;
2. использует их как IV;
3. оставшиеся данные рассматривает как ciphertext.

Если входной файл короче 16 байт, программа выводит ошибку.

Также при расшифровании можно передать IV явно:

```powershell
cryptocore --algorithm aes --mode cbc --decrypt --key 000102030405060708090a0b0c0d0e0f --iv AABBCCDDEEFF00112233445566778899 --input openssl_cipher.bin --output restored.txt
```

---

# OpenSSL interoperability AES

Для проверки используется:

```text
scripts/openssl_interop_test.py
```

Запуск:

```powershell
$env:Path += ";C:\Program Files\OpenSSL-Win64\bin"
python .\scripts\openssl_interop_test.py
```

Проверяются режимы:

```text
ECB
CBC
CFB
OFB
CTR
```

Для каждого выполняются два направления:

```text
CryptoCore -> OpenSSL
OpenSSL -> CryptoCore
```

Для ECB дополнительно выполняется прямое побайтовое сравнение ciphertext.

Полученный результат:

```text
Result: 11/11 checks passed
OpenSSL interoperability: PASSED
```

---

# Sprint 3 — CSPRNG и управление ключами

Цель Sprint 3 — использовать криптографически стойкий источник случайности для AES-ключей и IV.

Реализованы:

- отдельный CSPRNG-модуль;
- `os.urandom()`;
- автоматическая генерация AES-ключей;
- генерация IV через общий CSPRNG;
- проверка потенциально слабых ключей;
- проверка 1000 случайных ключей на уникальность;
- базовая проверка распределения единичных битов;
- подготовка данных для NIST STS;
- полный запуск NIST Statistical Test Suite.

---

# CSPRNG

Реализация:

```text
src/cryptocore/csprng.py
```

Основная функция:

```python
generate_random_bytes(num_bytes: int) -> bytes
```

Для генерации используется:

```python
os.urandom()
```

Обычный Python-модуль:

```python
random
```

для криптографических ключей и IV не используется.

При ошибке системного источника случайности CryptoCore выбрасывает понятное исключение.

---

# Security properties CSPRNG

`os.urandom()` использует источник случайности операционной системы, предназначенный для криптографических задач.

В проекте полученные случайные байты используются для:

- AES-128 ключей;
- IV режимов CBC, CFB, OFB и CTR;
- подготовки данных для статистических тестов NIST STS.

Генератор не использует предсказуемый псевдослучайный модуль `random`.

Статистические тесты не доказывают абсолютную криптографическую безопасность генератора, но позволяют обнаруживать заметные статистические отклонения.

---

# Автоматическая генерация AES-ключа

При шифровании параметр:

```text
--key
```

является необязательным.

Пример:

```powershell
cryptocore --algorithm aes --mode ctr --encrypt --input plaintext.txt --output ciphertext.bin
```

CryptoCore создаёт случайный ключ длиной:

```text
16 байт
```

и выводит его в stdout:

```text
[INFO] Generated random key: <hex-key>
```

Ключ:

- имеет длину 128 бит;
- создаётся через CSPRNG;
- выводится hexadecimal-строкой;
- выводится один раз;
- не записывается в ciphertext.

Для расшифрования `--key` остаётся обязательным.

---

# End-to-end test автоматического ключа

Для Sprint 3 предусмотрен отдельный acceptance test:

```text
tests/test_sprint3_auto_key_e2e.py
```

Он проверяет полный сценарий:

```text
исходный файл
    ↓
encrypt без --key
    ↓
CryptoCore генерирует и печатает ключ
    ↓
полученный ключ извлекается из stdout
    ↓
decrypt с этим ключом
    ↓
восстановленный файл
```

В конце проверяется точное совпадение восстановленного файла с исходным.

Запуск:

```powershell
pytest .\tests\test_sprint3_auto_key_e2e.py -v
```

---

# Проверка потенциально слабых AES-ключей

CryptoCore выполняет базовую проверку пользовательского AES-ключа.

Предупреждение создаётся для:

- полностью нулевого ключа;
- одинаковых повторяющихся байтов;
- последовательности `00–0F`;
- обратной последовательности `0F–00`.

Пример:

```text
00000000000000000000000000000000
```

Вывод:

```text
[WARNING] Обнаружен потенциально слабый AES-ключ: ...
```

Предупреждение выводится в:

```text
stderr
```

Операция при этом не блокируется.

---

# Проверка уникальности CSPRNG

Автоматический тест:

```text
tests/test_csprng.py
```

генерирует:

```text
1000
```

ключей по:

```text
16 байт
```

и проверяет отсутствие повторов.

Также выполняется базовая проверка доли единичных битов.

Допустимый диапазон:

```text
0.45 <= one_ratio <= 0.55
```

---

# NIST STS

Для статистической проверки CSPRNG использовалась:

```text
NIST Statistical Test Suite 2.1.2
```

## Подготовка данных

Модуль:

```text
src/cryptocore/nist_data.py
```

использует основной CSPRNG проекта:

```python
generate_random_bytes()
```

Скрипт:

```text
scripts/generate_nist_data.py
```

создаёт:

```text
nist_test_data.bin
```

размером:

```text
10 000 000 байт
```

то есть:

```text
80 000 000 бит
```

Запуск:

```powershell
python .\scripts\generate_nist_data.py
```

---

# Параметры NIST STS

В выполненном прогоне использовались:

```text
Длина одной последовательности: 1 000 000 бит
Количество последовательностей: 80
Общий объём: 80 000 000 бит
Количество групп тестов: 15
```

---

# Запуск NIST STS

NIST STS запускался в WSL/Linux.

После сборки NIST STS необходимо перейти в его каталог:

```bash
cd <path-to-nist-sts>
```

Запуск:

```bash
./assess 1000000
```

Значение:

```text
1000000
```

задаёт длину одной последовательности в битах.

В интерактивном меню необходимо:

1. выбрать выполнение всех 15 статистических тестов;
2. указать путь к `nist_test_data.bin`;
3. выбрать Binary input mode;
4. указать 80 последовательностей;
5. запустить анализ.

Файл `nist_test_data.bin` содержит бинарные случайные данные и поэтому должен анализироваться как binary input.

---

# Критерий NIST STS

Для статистических тестов анализируется:

```text
p-value
```

Основной порог:

```text
p-value >= 0.01
```

Также рассматривается доля последовательностей, прошедших каждый тест.

Единичное статистическое отклонение само по себе не обязательно означает неисправность CSPRNG.

Систематические или массовые отказы тестов могли бы указывать на проблему.

---

# Результат NIST STS

Были проанализированы:

```text
80 последовательностей
по 1 000 000 бит
```

Общий объём:

```text
80 000 000 бит
```

Были выполнены все 15 групп статистических тестов NIST STS.

Полученный набор результатов соответствовал статистическим критериям для проверяемой последовательности данных.

Это дополняет автоматические тесты:

```text
tests/test_csprng.py
tests/test_nist_data.py
```

---

# Sprint 4 — криптографические хеш-функции

Цель Sprint 4 — добавить криптографические хеш-функции для проверки целостности данных.

Реализованы:

- SHA-256;
- SHA3-256;
- команда `dgst`;
- `--algorithm`;
- `--input`;
- `--output`;
- binary file I/O;
- chunked processing;
- Known-Answer Tests;
- официальные NIST test vectors;
- NIST Monte Carlo tests;
- interoperability;
- avalanche effect;
- проверка больших файлов.

---

# SHA-256

Реализация:

```text
src/cryptocore/hash/sha256.py
```

SHA-256 реализован самостоятельно без использования `hashlib` внутри основной реализации.

Реализованы:

- 512-битные блоки;
- восемь начальных значений состояния;
- 64 round constants;
- Ch;
- Maj;
- Σ0;
- Σ1;
- σ0;
- σ1;
- message schedule;
- 64 раунда compression function;
- padding;
- добавление 64-битной длины сообщения;
- incremental update.

Поддерживаются:

```python
update()
digest()
hexdigest()
```

---

# SHA3-256

Реализация:

```text
src/cryptocore/hash/sha3_256.py
```

SHA3-256 также реализован самостоятельно.

Реализованы:

- sponge construction;
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
- SHA-3 domain separation;
- padding;
- 256-битный digest.

---

# Security properties SHA-256 и SHA3-256

Обе функции формируют результат длиной:

```text
256 бит
```

Для идеализированной 256-битной криптографической хеш-функции ожидаемый уровень стойкости составляет:

```text
Preimage resistance:         около 2^256
Second-preimage resistance:  около 2^256
Collision resistance:        около 2^128
```

Коллизионная стойкость ограничена birthday bound.

SHA-256 использует Merkle-Damgård construction.

SHA3-256 использует Keccak sponge construction.

Для SHA3-256:

```text
state    = 1600 бит
rate     = 1088 бит
capacity = 512 бит
digest   = 256 бит
```

Обычный криптографический хеш позволяет обнаруживать изменение данных, но не обеспечивает аутентификацию отправителя, поскольку для вычисления хеша не используется секретный ключ.

Для проверки одновременно целостности и подлинности в Sprint 5 используется HMAC-SHA256.

---

# Команда dgst

Для вычисления хешей используется отдельная команда:

```text
cryptocore dgst
```

Поддерживаются:

```text
sha256
sha3-256
```

SHA-256:

```powershell
cryptocore dgst --algorithm sha256 --input plaintext.txt
```

SHA3-256:

```powershell
cryptocore dgst --algorithm sha3-256 --input plaintext.txt
```

Формат результата:

```text
HASH_VALUE  INPUT_FILE_PATH
```

Хеш выводится lowercase hexadecimal.

---

# Сохранение хеша

Поддерживается:

```text
--output
```

Пример:

```powershell
cryptocore dgst --algorithm sha256 --input plaintext.txt --output plaintext.sha256
```

Содержимое файла:

```text
HASH_VALUE  INPUT_FILE_PATH
```

---

# Потоковое хеширование

Файлы открываются в бинарном режиме:

```python
rb
```

и читаются блоками:

```text
8192 байт
```

Схема:

```text
input
  ↓
8192-byte chunk
  ↓
update()
  ↓
next chunk
  ↓
digest
```

Полный файл не загружается в оперативную память.

---

# Known-Answer Tests SHA-256

Для пустого сообщения:

```text
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

Для:

```text
abc
```

результат:

```text
ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad
```

Для:

```text
abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq
```

результат:

```text
248d6a61d20638b8e5c026930c3e6039a33ce45964ff2167f6ecedd419db06c1
```

---

# Known-Answer Tests SHA3-256

Для пустого сообщения:

```text
a7ffc6f8bf1ed76651c14756a061d662f580ff4de43b49fa82d80a4b80f8434a
```

Для:

```text
abc
```

результат:

```text
3a985da74fe225b2045c172d6bd390bd855f086e3e9d525b46bfe24511431532
```

---

# Официальные NIST test vectors

В проект добавлены официальные NIST `.rsp` test vectors.

Каталог:

```text
tests/vectors/nist/
```

SHA-256:

```text
SHA256ShortMsg.rsp
SHA256LongMsg.rsp
SHA256Monte.rsp
```

SHA3-256:

```text
SHA3_256ShortMsg.rsp
SHA3_256LongMsg.rsp
SHA3_256Monte.rsp
```

Автоматические Short/Long проверки:

```text
tests/test_nist_hash_vectors.py
```

Запуск:

```powershell
pytest .\tests\test_nist_hash_vectors.py -v
```

---

# NIST Monte Carlo Hash Tests

Отдельный скрипт:

```text
scripts/nist_hash_monte_test.py
```

проверяет официальные Monte Carlo vectors:

```text
SHA256Monte.rsp
SHA3_256Monte.rsp
```

Запуск:

```powershell
python .\scripts\nist_hash_monte_test.py
```

Ожидаемый финальный результат:

```text
NIST SHA-256 Monte Carlo: PASSED
NIST SHA3-256 Monte Carlo: PASSED

All NIST Monte Carlo hash tests: PASSED
```

---

# Interoperability SHA-256

Для SHA-256 используется:

```bash
sha256sum plaintext.txt
```

Также скрипт:

```text
scripts/hash_interop_test.py
```

умеет автоматически выбрать доступную системную реализацию.

---

# Interoperability SHA3-256

SHA3-256 проверяется независимой системной реализацией.

OpenSSL:

```bash
openssl dgst -sha3-256 plaintext.txt
```

Также Sprint 4 предусматривает проверку через:

```bash
sha3sum -a 256 plaintext.txt
```

При наличии `libdigest-sha3-perl` в WSL:

```bash
sudo apt update
sudo apt install -y libdigest-sha3-perl
```

Проверка:

```bash
sha3sum -a 256 plaintext.txt
```

CryptoCore:

```powershell
cryptocore dgst --algorithm sha3-256 --input plaintext.txt
```

Первые 64 hexadecimal-символа результатов должны полностью совпасть.

Автоматический interoperability-скрипт:

```powershell
python .\scripts\hash_interop_test.py
```

использует:

```text
sha256sum
sha3sum -a 256
```

если соответствующие утилиты доступны, и имеет fallback на OpenSSL.

---

# Avalanche Effect

Тест:

```text
tests/test_hash_avalanche.py
```

В исходном сообщении изменяется один бит.

После этого сравниваются два 256-битных хеша.

Количество изменившихся битов проверяется в диапазоне:

```text
100 < changed_bits < 156
```

Тестируются:

```text
SHA-256
SHA3-256
```

---

# Проверка файла больше 1 GiB

Скрипт:

```text
scripts/hash_large_file_test.py
```

создаёт sparse-файл размером:

```text
1 073 741 825 байт
```

то есть:

```text
1 GiB + 1 байт
```

Для него вычисляются:

```text
SHA-256
SHA3-256
```

Результаты сравниваются с:

```python
hashlib.sha256()
hashlib.sha3_256()
```

Запуск:

```powershell
python .\scripts\hash_large_file_test.py
```

---

# Проверка streaming больше 1 GiB

Автоматический тест:

```text
tests/test_large_hash_streaming.py
```

создаёт виртуальный поток размером:

```text
1 GiB + 1 байт
```

и проверяет:

- обработку всего логического объёма;
- чтение ограниченными блоками;
- отсутствие загрузки полного входа в память;
- `CHUNK_SIZE = 8192`.

Криптографическая корректность SHA независимо проверяется официальными NIST vectors.

---

# Sprint 5 — HMAC-SHA256

Цель Sprint 5 — реализовать механизм проверки подлинности и целостности данных.

Добавлен:

```text
HMAC-SHA256
```

Основная реализация:

```text
src/cryptocore/mac/hmac.py
```

HMAC реализован самостоятельно.

Основная реализация не использует:

```python
hmac
hashlib
```

Внутренней хеш-функцией является собственная SHA-256 из Sprint 4.

---

# Конструкция HMAC

Используется конструкция RFC 2104:

```text
HMAC(K, m) =
H((K XOR opad) || H((K XOR ipad) || m))
```

где:

```text
H     = SHA-256
K     = секретный ключ
m     = сообщение
ipad  = 0x36 repeated 64 times
opad  = 0x5C repeated 64 times
```

Размер блока SHA-256:

```text
64 байта
```

---

# Security properties HMAC-SHA256

HMAC-SHA256 обеспечивает проверку:

- целостности;
- подлинности.

В отличие от обычного SHA-256, HMAC использует секретный ключ.

Сторона, которая знает правильный секретный ключ, может проверить, что:

- сообщение не было изменено;
- MAC был сформирован стороной, обладающей тем же ключом.

HMAC:

- не шифрует данные;
- не скрывает содержимое;
- не обеспечивает конфиденциальность.

Безопасность зависит от:

- сохранения ключа в тайне;
- качества ключевого материала;
- стойкости SHA-256.

Для сравнения HMAC используется:

```python
secrets.compare_digest()
```

что предпочтительнее обычного посимвольного сравнения.

---

# Обработка HMAC-ключа

HMAC поддерживает ключи произвольной длины.

Если:

```text
len(key) > 64
```

сначала выполняется:

```text
key = SHA256(key)
```

Если:

```text
len(key) < 64
```

ключ дополняется нулевыми байтами:

```text
key = key || zero padding
```

до 64 байт.

Если ключ имеет длину ровно 64 байта, он используется без предварительного хеширования.

---

# CLI HMAC

HMAC используется через:

```text
cryptocore dgst
```

Флаг:

```text
--hmac
```

При HMAC обязательны:

```text
--algorithm sha256
--hmac
--key
--input
```

Ключ передаётся в hexadecimal-формате.

---

# Генерация HMAC

Пример:

```powershell
cryptocore dgst --algorithm sha256 --hmac --key 00112233445566778899aabbccddeeff --input plaintext.txt
```

Формат:

```text
HMAC_VALUE  INPUT_FILE_PATH
```

HMAC выводится lowercase hexadecimal.

---

# Сохранение HMAC

Поддерживается:

```text
--output
```

Пример:

```powershell
cryptocore dgst --algorithm sha256 --hmac --key 00112233445566778899aabbccddeeff --input plaintext.txt --output plaintext.hmac
```

Содержимое файла:

```text
HMAC_VALUE  INPUT_FILE_PATH
```

---

# Проверка HMAC

Используется:

```text
--verify
```

Пример:

```powershell
cryptocore dgst --algorithm sha256 --hmac --key 00112233445566778899aabbccddeeff --input plaintext.txt --verify plaintext.hmac
```

Успешная проверка:

```text
[OK] HMAC verification successful
```

Код завершения:

```text
0
```

Ошибка:

```text
[ERROR] HMAC verification failed
```

Код завершения:

```text
1
```

---

# Expected HMAC format

Файл проверки может содержать:

```text
HMAC_VALUE  INPUT_FILE_PATH
```

CryptoCore использует первый whitespace-separated элемент как ожидаемое значение HMAC.

Имя файла после HMAC и дополнительные пробелы не влияют на сравнение.

---

# Потоковый HMAC

Файлы открываются:

```python
rb
```

и обрабатываются блоками:

```text
8192 байт
```

Схема:

```text
input
  ↓
8192-byte chunk
  ↓
HMACSHA256.update()
  ↓
next chunk
  ↓
HMAC digest
```

Полный файл не загружается в оперативную память.

---

# RFC 4231 Known-Answer Tests

Тесты:

```text
tests/test_hmac_vectors.py
```

Проверяются:

```text
RFC 4231 Test Case 1
RFC 4231 Test Case 2
RFC 4231 Test Case 3
RFC 4231 Test Case 4
```

---

# RFC 4231 Test Case 1

Ключ:

```text
0b repeated 20 times
```

Сообщение:

```text
Hi There
```

Ожидаемый HMAC-SHA256:

```text
b0344c61d8db38535ca8afceaf0bf12b881dc200c9833da726e9376c2e32cff7
```

---

# RFC 4231 Test Case 2

Ключ:

```text
Jefe
```

Сообщение:

```text
what do ya want for nothing?
```

Ожидаемый HMAC-SHA256:

```text
5bdcc146bf60754e6a042426089575c75a003f089d2739839dec58b964ec3843
```

---

# RFC 4231 Test Case 3

Ключ:

```text
aa repeated 20 times
```

Сообщение:

```text
dd repeated 50 times
```

Ожидаемый HMAC-SHA256:

```text
773ea91e36800e46854db8ebd09181a72959098b3ef8c122d9635514ced565fe
```

---

# RFC 4231 Test Case 4

Ключ:

```text
0102030405060708090a0b0c0d0e0f10111213141516171819
```

Данные:

```text
cd repeated 50 times
```

Ожидаемый HMAC-SHA256:

```text
82558a389a443c0ea4cc819899f2083a85f0faa3e578f8077a2e3ff46729665b
```

---

# Проверка размеров HMAC-ключей

Автоматически проверяются:

```text
16 байт
64 байта
100 байт
```

Это покрывает:

- короткий ключ;
- ключ размером блока;
- ключ длиннее блока.

Для длинного ключа есть отдельная явная проверка:

```text
test_long_key_is_hashed_before_hmac
```

Эталоном в тестах служат:

```python
hmac
hashlib.sha256
```

Эти модули используются только в тестах, а не в основной реализации CryptoCore.

---

# Empty File HMAC

Проверяется HMAC для:

```python
b""
```

Результат сравнивается с эталонной реализацией Python.

---

# Tamper Detection — файл

Тест:

1. создаёт HMAC исходного файла;
2. изменяет содержимое;
3. выполняет `--verify`;
4. ожидает ошибку.

Результат:

```text
[ERROR] HMAC verification failed
```

---

# Tamper Detection — ключ

Тест:

1. создаёт HMAC правильным ключом;
2. выполняет проверку другим ключом;
3. ожидает ошибку.

Результат:

```text
[ERROR] HMAC verification failed
```

---

# Реальные CLI exit codes

В:

```text
tests/test_hmac_cli.py
```

используется настоящий subprocess:

```text
python -m cryptocore
```

Проверяется:

```text
valid HMAC  -> exit code 0
invalid HMAC -> non-zero exit code
```

---

# Реальный HMAC большого файла

Скрипт:

```text
scripts/hmac_large_file_test.py
```

создаёт файл:

```text
10 485 760 байт
```

то есть:

```text
10 MiB
```

Настоящий HMAC CryptoCore сравнивается с:

```python
hmac.new(..., hashlib.sha256)
```

Подтверждённый результат:

```text
CryptoCore: d20bad94a922f94d99165e579e66f710efc20dc7429bf47cf0985e6303d69ea0
Reference:  d20bad94a922f94d99165e579e66f710efc20dc7429bf47cf0985e6303d69ea0

Large HMAC test: PASSED
```

---

# Huge HMAC streaming test

Скрипт:

```text
scripts/hmac_huge_streaming_test.py
```

проверяет функцию:

```python
hmac_stream()
```

на виртуальном входе размером:

```text
21 474 836 603 байта
```

то есть более:

```text
20 GiB
```

Максимальный размер одного чтения:

```text
8192 байт
```

Подтверждённый результат:

```text
Logical input size: 21,474,836,603 bytes
Processed: 21,474,836,603 bytes
Maximum read: 8192 bytes

Huge HMAC streaming test: PASSED
```

В этом тесте криптографическое ядро заменяется счётчиком.

Поэтому тест предназначен именно для доказательства constant-memory streaming.

Криптографическая корректность независимо подтверждается RFC 4231 и сравнением с Python HMAC.

---

# Memory-limited HMAC test

Дополнительный тест:

```text
scripts/hmac_memory_limited_test.py
```

предназначен для прямой проверки требования:

```text
размер входного файла > доступная процессу память
```

Тест запускается в Linux/WSL.

Он:

1. определяет текущий размер виртуальной памяти Python-процесса;
2. создаёт sparse-файл больше будущего memory limit;
3. вычисляет эталонный HMAC;
4. устанавливает Linux `RLIMIT_AS`;
5. запускает настоящий `cryptocore.digest.hmac_file()`;
6. использует настоящий `HMACSHA256`;
7. сравнивает результат с `hmac + hashlib.sha256`.

Запуск:

```bash
cd "/mnt/c/Users/Елизавета/PycharmProjects/cryptocore"
PYTHONPATH=src python3 scripts/hmac_memory_limited_test.py
```

Успешный тест должен завершиться:

```text
Memory-limited HMAC test: PASSED
```

Это дополнительно подтверждает, что HMAC не требует загрузки полного файла в оперативную память.

---

# HMAC interoperability с OpenSSL

CryptoCore:

```powershell
cryptocore dgst --algorithm sha256 --hmac --key 00112233445566778899aabbccddeeff --input plaintext.txt
```

OpenSSL:

```powershell
openssl dgst -sha256 -mac HMAC -macopt hexkey:00112233445566778899aabbccddeeff plaintext.txt
```

Для одинаковых данных и одинакового ключа HMAC должны совпасть.

---

# AES-CMAC

AES-CMAC в Sprint 5 не реализован.

В техническом задании AES-CMAC относится к:

```text
Bonus / Could
```

и не является обязательным требованием Sprint 5.

---

# Автоматические тесты

Основные файлы:

```text
tests/test_cbc.py
tests/test_cfb.py
tests/test_cli.py
tests/test_csprng.py
tests/test_ctr.py
tests/test_digest.py
tests/test_digest_cli.py
tests/test_ecb.py
tests/test_hash_avalanche.py
tests/test_hmac_cli.py
tests/test_hmac_vectors.py
tests/test_iv.py
tests/test_large_hash_streaming.py
tests/test_modes_integration.py
tests/test_nist_data.py
tests/test_nist_hash_vectors.py
tests/test_ofb.py
tests/test_padding.py
tests/test_sha256.py
tests/test_sha3_256.py
tests/test_sprint3_auto_key_e2e.py
```

---

# pytest

В:

```text
pyproject.toml
```

указано:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
```

Поэтому:

```powershell
pytest -v
```

запускает автоматические тесты только из каталога:

```text
tests/
```

Служебные и тяжёлые тесты из:

```text
scripts/
```

запускаются отдельно.

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
|       |-- csprng.py
|       |-- digest.py
|       |-- digest_cli.py
|       |-- file_io.py
|       |-- iv.py
|       |-- nist_data.py
|       |-- padding.py
|       |
|       |-- hash/
|       |   |-- __init__.py
|       |   |-- sha256.py
|       |   `-- sha3_256.py
|       |
|       |-- mac/
|       |   |-- __init__.py
|       |   `-- hmac.py
|       |
|       `-- modes/
|           |-- __init__.py
|           |-- cbc.py
|           |-- cfb.py
|           |-- ctr.py
|           |-- ecb.py
|           `-- ofb.py
|
|-- tests/
|   |
|   |-- vectors/
|   |   `-- nist/
|   |       |-- SHA256ShortMsg.rsp
|   |       |-- SHA256LongMsg.rsp
|   |       |-- SHA256Monte.rsp
|   |       |-- SHA3_256ShortMsg.rsp
|   |       |-- SHA3_256LongMsg.rsp
|   |       `-- SHA3_256Monte.rsp
|   |
|   |-- test_cbc.py
|   |-- test_cfb.py
|   |-- test_cli.py
|   |-- test_csprng.py
|   |-- test_ctr.py
|   |-- test_digest.py
|   |-- test_digest_cli.py
|   |-- test_ecb.py
|   |-- test_hash_avalanche.py
|   |-- test_hmac_cli.py
|   |-- test_hmac_vectors.py
|   |-- test_iv.py
|   |-- test_large_hash_streaming.py
|   |-- test_modes_integration.py
|   |-- test_nist_data.py
|   |-- test_nist_hash_vectors.py
|   |-- test_ofb.py
|   |-- test_padding.py
|   |-- test_sha256.py
|   |-- test_sha3_256.py
|   `-- test_sprint3_auto_key_e2e.py
|
|-- scripts/
|   |-- generate_nist_data.py
|   |-- hash_interop_test.py
|   |-- hash_large_file_test.py
|   |-- hmac_huge_streaming_test.py
|   |-- hmac_large_file_test.py
|   |-- hmac_memory_limited_test.py
|   |-- nist_hash_monte_test.py
|   |-- openssl_interop_test.py
|   `-- round_trip_test.py
|
|-- .gitignore
|-- plaintext.txt
|-- pyproject.toml
|-- README.md
`-- requirements.txt
```

---

# Полная проверка проекта

Автоматические тесты:

```powershell
pytest -v
```

Round-trip Sprint 1:

```powershell
python .\scripts\round_trip_test.py
```

AES/OpenSSL interoperability:

```powershell
python .\scripts\openssl_interop_test.py
```

Hash interoperability:

```powershell
python .\scripts\hash_interop_test.py
```

NIST hash Monte Carlo:

```powershell
python .\scripts\nist_hash_monte_test.py
```

Реальный файл >1 GiB:

```powershell
python .\scripts\hash_large_file_test.py
```

Реальный HMAC 10 MiB:

```powershell
python .\scripts\hmac_large_file_test.py
```

Huge constant-memory HMAC:

```powershell
python .\scripts\hmac_huge_streaming_test.py
```

Memory-limited HMAC в WSL:

```bash
PYTHONPATH=src python3 scripts/hmac_memory_limited_test.py
```

SHA3-256 через `sha3sum`:

```bash
sha3sum -a 256 plaintext.txt
```

CryptoCore SHA3-256:

```powershell
cryptocore dgst --algorithm sha3-256 --input plaintext.txt
```

---

# Итоги Sprint 1

Реализованы:

- Git-репозиторий;
- README;
- build system через `pyproject.toml`;
- CLI;
- AES-128 ECB;
- hexadecimal AES-ключи;
- PKCS#7;
- binary file I/O;
- обработка ошибок;
- default output filename;
- round-trip test;
- OpenSSL interoperability.

---

# Итоги Sprint 2

Реализованы:

- AES-128 CBC;
- AES-128 CFB-128;
- AES-128 OFB;
- AES-128 CTR;
- самостоятельная логика режимов;
- secure IV generation;
- IV длиной 16 байт;
- `--iv` для расшифрования;
- запрет `--iv` при шифровании;
- формат `<IV><ciphertext>`;
- автоматическое извлечение IV;
- обработка слишком короткого ciphertext;
- двусторонняя interoperability с OpenSSL.

---

# Итоги Sprint 3

Реализованы:

- отдельный CSPRNG-модуль;
- `generate_random_bytes()`;
- `os.urandom()`;
- обработка ошибок CSPRNG;
- автоматическая генерация AES-128 ключа;
- вывод ключа в stdout;
- обязательный ключ при расшифровании;
- общий CSPRNG для ключей и IV;
- предупреждение о слабых пользовательских ключах;
- 1000-key uniqueness test;
- базовый distribution test;
- end-to-end auto-key round-trip test;
- генерация NIST test data;
- полный NIST STS;
- документация NIST STS.

---

# Итоги Sprint 4

Реализованы:

- SHA-256 с нуля;
- SHA3-256 с нуля;
- Keccak-f[1600];
- команда `dgst`;
- два алгоритма хеширования;
- binary file I/O;
- lowercase hexadecimal output;
- `--output`;
- chunked processing;
- constant-memory processing;
- empty input;
- Known-Answer Tests;
- официальные NIST Short Message vectors;
- официальные NIST Long Message vectors;
- NIST Monte Carlo;
- SHA-256 interoperability;
- SHA3-256 interoperability;
- поддержка `sha3sum -a 256`;
- avalanche effect;
- реальный файл >1 GiB;
- автоматический streaming test >1 GiB;
- документация security properties.

---

# Итоги Sprint 5

Реализованы:

- HMAC-SHA256 с нуля;
- использование собственной SHA-256;
- RFC 2104 construction;
- произвольная длина ключа;
- hashing ключей >64 байт;
- zero padding ключей <64 байт;
- `--hmac`;
- обязательный hexadecimal `--key`;
- `--verify`;
- `--output`;
- формат `HMAC_VALUE INPUT_FILE_PATH`;
- flexible expected-HMAC parsing;
- binary file I/O;
- chunked processing;
- `secrets.compare_digest`;
- RFC 4231 Test Cases 1–4;
- ключи 16/64/100 байт;
- отдельная проверка длинного ключа;
- empty file;
- verify generated HMAC;
- tamper detection файла;
- tamper detection ключа;
- реальные CLI exit codes;
- настоящий HMAC файла 10 MiB;
- huge logical streaming >20 GiB;
- отдельный memory-limited test с настоящим HMAC;
- документация конструкции и security properties.

AES-CMAC не реализован, поскольку относится к дополнительному Bonus/Could требованию.

---

# Текущий результат

CryptoCore поддерживает:

```text
AES-128 ECB
AES-128 CBC
AES-128 CFB-128
AES-128 OFB
AES-128 CTR

CSPRNG

SHA-256
SHA3-256

HMAC-SHA256
```

