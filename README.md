# CryptoCore

CryptoCore — учебное консольное приложение на Python для выполнения криптографических операций с файлами.

В проекте последовательно реализованы требования Sprint 1–5:

- AES-128 ECB;
- AES-128 CBC;
- AES-128 CFB-128;
- AES-128 OFB;
- AES-128 CTR;
- PKCS#7;
- генерация IV;
- CSPRNG;
- автоматическая генерация AES-ключей;
- SHA-256;
- SHA3-256;
- HMAC-SHA256;
- потоковая обработка файлов;
- проверка HMAC;
- автоматические тесты;
- проверка совместимости с OpenSSL;
- статистическая проверка CSPRNG через NIST STS.

---

# Требования

Для запуска проекта требуется:

- Python 3.10 или новее;
- PyCryptodome;
- pytest;
- OpenSSL — для проверки совместимости;
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

В Sprint 1 была реализована базовая структура CryptoCore.

Основные возможности:

- AES-128;
- режим ECB;
- PKCS#7 padding;
- командная строка;
- работа с файлами;
- автоматические тесты;
- проверка совместимости с OpenSSL.

---

# AES-128 ECB

ECB обрабатывает каждый 16-байтовый блок независимо.

Для ECB IV не используется.

Используется PKCS#7 padding.

Пример шифрования:

```powershell
cryptocore --algorithm aes --mode ecb --encrypt --key 000102030405060708090a0b0c0d0e0f --input plaintext.txt --output encrypted_ecb.bin
```

Расшифрование:

```powershell
cryptocore --algorithm aes --mode ecb --decrypt --key 000102030405060708090a0b0c0d0e0f --input encrypted_ecb.bin --output decrypted_ecb.txt
```

AES-128 использует ключ длиной:

```text
16 байт
```

или:

```text
32 hexadecimal-символа
```

Например:

```text
000102030405060708090a0b0c0d0e0f
```

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

работают без padding.

---

# Sprint 2 — дополнительные режимы AES

В Sprint 2 были добавлены:

- CBC;
- CFB-128;
- OFB;
- CTR;
- генерация IV;
- параметр `--iv`;
- формат хранения `<IV><ciphertext>`;
- двусторонняя совместимость с OpenSSL.

Логика режимов реализована самостоятельно поверх AES-примитива.

---

# AES-128 CBC

CBC использует IV длиной 16 байт.

Каждый блок plaintext объединяется через XOR с предыдущим ciphertext-блоком.

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

используется 16-байтовый IV.

ECB IV не использует.

При обычном шифровании IV создаётся автоматически.

Формат файла:

```text
<16-byte IV><ciphertext>
```

AES-ключ в ciphertext не записывается.

При расшифровании CryptoCore может автоматически получить IV из первых 16 байт файла.

Также можно указать IV вручную:

```powershell
cryptocore --algorithm aes --mode cbc --decrypt --key 000102030405060708090a0b0c0d0e0f --iv AABBCCDDEEFF00112233445566778899 --input openssl_cipher.bin --output restored.txt
```

---

# Sprint 3 — CSPRNG и управление ключами

В Sprint 3 реализованы:

- отдельный CSPRNG;
- `os.urandom()`;
- автоматическая генерация AES-ключей;
- генерация IV через общий CSPRNG;
- проверка потенциально слабых пользовательских ключей;
- тесты случайности;
- подготовка данных для NIST STS;
- проверка CSPRNG через NIST STS.

---

# CSPRNG

Модуль:

```text
src/cryptocore/csprng.py
```

Основная функция:

```python
generate_random_bytes(num_bytes: int) -> bytes
```

Для генерации используются криптографически стойкие случайные данные:

```python
os.urandom()
```

Обычный модуль:

```python
random
```

для криптографических ключей и IV не используется.

---

# Автоматическая генерация AES-ключа

При шифровании параметр:

```text
--key
```

можно не указывать.

В этом случае CryptoCore создаёт случайный 16-байтовый AES-128 ключ.

Пример:

```powershell
cryptocore --algorithm aes --mode ctr --encrypt --input plaintext.txt --output ciphertext.bin
```

Программа выводит созданный ключ:

```text
[INFO] Generated random key: <hex-key>
```

Ключ:

- состоит из 16 случайных байт;
- выводится в hexadecimal-формате;
- не записывается в ciphertext.

Для расшифрования ключ должен быть известен пользователю.

---

# Проверка слабых AES-ключей

CryptoCore выполняет базовую проверку пользовательского AES-ключа.

Предупреждение создаётся, например, для:

- одинаковых повторяющихся байтов;
- полностью нулевого ключа;
- последовательности от `00` до `0F`;
- обратной последовательности.

Пример:

```text
00000000000000000000000000000000
```

Вывод:

```text
[WARNING] Обнаружен потенциально слабый AES-ключ: ...
```

Операция не блокируется.

---

# NIST STS

Для статистической проверки CSPRNG использовалась:

```text
NIST Statistical Test Suite 2.1.2
```

Подготовка данных выполняется скриптом:

```text
scripts/generate_nist_data.py
```

Создаётся файл:

```text
nist_test_data.bin
```

размером:

```text
10 000 000 байт
```

Параметры проверки:

```text
Размер последовательности: 1 000 000 бит
Количество последовательностей: 80
Общий объём: 80 000 000 бит
```

Были выполнены все 15 групп статистических тестов NIST STS.

Итоговая проверка показала соответствие статистическим критериям.

---

# OpenSSL interoperability AES

Для проверки AES используется:

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

Для них выполняются направления:

```text
CryptoCore -> OpenSSL
OpenSSL -> CryptoCore
```

Также выполняется прямое сравнение ciphertext для ECB.

Полученный результат:

```text
Result: 11/11 checks passed
OpenSSL interoperability: PASSED
```

---

# Sprint 4 — криптографические хеш-функции

В Sprint 4 добавлены:

- SHA-256;
- SHA3-256;
- отдельная команда `dgst`;
- потоковое чтение файлов;
- `--output`;
- Known-Answer Tests;
- interoperability;
- avalanche effect;
- проверки больших данных.

---

# SHA-256

Реализация находится в:

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
- добавление длины сообщения;
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
- padding.

---

# Команда dgst

Для хеширования используется:

```text
cryptocore dgst
```

Поддерживаемые алгоритмы:

```text
sha256
sha3-256
```

Пример SHA-256:

```powershell
cryptocore dgst --algorithm sha256 --input plaintext.txt
```

Пример SHA3-256:

```powershell
cryptocore dgst --algorithm sha3-256 --input plaintext.txt
```

Формат результата:

```text
HASH_VALUE  INPUT_FILE_PATH
```

Результат выводится lowercase hexadecimal.

---

# Сохранение хеша

Можно использовать:

```powershell
cryptocore dgst --algorithm sha256 --input plaintext.txt --output plaintext.sha256
```

Файл содержит:

```text
HASH_VALUE  INPUT_FILE_PATH
```

---

# Потоковое хеширование

Файлы открываются в бинарном режиме:

```python
rb
```

и обрабатываются блоками:

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
digest
```

Весь файл целиком в оперативную память не загружается.

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

# Interoperability SHA-256

Проверка выполнялась через:

```bash
sha256sum plaintext.txt
```

Результат CryptoCore совпал с результатом `sha256sum`.

```text
SHA-256 interoperability: PASSED
```

---

# Interoperability SHA3-256

SHA3-256 был независимо проверен через OpenSSL:

```bash
openssl dgst -sha3-256 plaintext.txt
```

Результаты совпали:

```text
SHA3-256 OpenSSL interoperability: PASSED
```

---

# Avalanche Effect

Добавлен тест:

```text
tests/test_hash_avalanche.py
```

В исходном сообщении изменяется один бит.

После этого сравниваются два 256-битных хеша.

В тесте используется диапазон:

```text
100 < changed_bits < 156
```

Проверяются:

```text
SHA-256
SHA3-256
```

---

# Sprint 5 — HMAC

Цель Sprint 5 — добавить механизм проверки подлинности и целостности данных.

В проект добавлен:

```text
HMAC-SHA256
```

Основная реализация:

```text
src/cryptocore/mac/hmac.py
```

HMAC реализован самостоятельно и использует SHA-256, созданный в Sprint 4.

Стандартный Python-модуль `hmac` в основной реализации HMAC не используется.

---

# Принцип работы HMAC

Используется конструкция:

```text
HMAC(K, m) =
H((K XOR opad) || H((K XOR ipad) || m))
```

где:

```text
H     = SHA-256
ipad  = байт 0x36, повторённый 64 раза
opad  = байт 0x5C, повторённый 64 раза
K     = ключ
m     = сообщение
```

Размер блока SHA-256:

```text
64 байта
```

---

# Обработка HMAC-ключа

HMAC поддерживает ключи произвольной длины.

Если ключ длиннее 64 байт:

```text
key = SHA256(key)
```

Если ключ короче 64 байт:

```text
key = key || zero padding
```

до размера:

```text
64 байта
```

Если ключ имеет длину ровно 64 байта, он используется без дополнительного хеширования.

---

# Команда HMAC

HMAC вызывается через существующую команду:

```text
cryptocore dgst
```

с параметром:

```text
--hmac
```

Для HMAC необходимо указать:

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

Формат результата:

```text
HMAC_VALUE  INPUT_FILE_PATH
```

Например:

```text
0123456789abcdef...  plaintext.txt
```

HMAC выводится lowercase hexadecimal.

---

# Сохранение HMAC в файл

Поддерживается параметр:

```text
--output
```

Пример:

```powershell
cryptocore dgst --algorithm sha256 --hmac --key 00112233445566778899aabbccddeeff --input plaintext.txt --output plaintext.hmac
```

Файл содержит:

```text
HMAC_VALUE  INPUT_FILE_PATH
```

---

# Проверка HMAC

Для проверки используется:

```text
--verify
```

Пример:

```powershell
cryptocore dgst --algorithm sha256 --hmac --key 00112233445566778899aabbccddeeff --input plaintext.txt --verify plaintext.hmac
```

При успешной проверке:

```text
[OK] HMAC verification successful
```

Код возврата:

```text
0
```

При несовпадении:

```text
[ERROR] HMAC verification failed
```

Код возврата:

```text
1
```

---

# Формат файла проверки

Файл HMAC может содержать:

```text
HMAC_VALUE  INPUT_FILE_PATH
```

При чтении ожидаемого значения CryptoCore использует HMAC в начале строки.

Имя файла и дополнительные пробельные символы не влияют на сравнение.

---

# Безопасное сравнение HMAC

Для сравнения вычисленного и ожидаемого HMAC используется:

```python
secrets.compare_digest()
```

Это позволяет избежать обычного посимвольного сравнения значений MAC.

---

# Потоковая обработка HMAC

HMAC не загружает весь файл в оперативную память.

Файл читается блоками:

```text
8192 байт
```

Для каждого блока вызывается:

```python
HMACSHA256.update()
```

Схема:

```text
input file
    |
    v
8192-byte chunk
    |
    v
HMACSHA256.update()
    |
    v
next chunk
    |
    v
HMAC digest
```

Потребление памяти при этом не зависит от полного размера входного файла.

---

# RFC 4231

Для проверки HMAC-SHA256 используются Known-Answer Tests из RFC 4231.

Реализованы обязательные тестовые случаи:

```text
Test Case 1
Test Case 2
Test Case 3
Test Case 4
```

Тесты находятся в:

```text
tests/test_hmac_vectors.py
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

Данные:

```text
dd repeated 50 times
```

Ожидаемый HMAC-SHA256:

```text
773ea91e36800e46854db8ebd09181a72959098b3ef8c122d9635514ced565fe
```

---

# RFC 4231 Test Case 4

Проверяется ещё один официальный тестовый вектор RFC 4231 с бинарным ключом и сообщением.

Результат CryptoCore совпадает с ожидаемым HMAC-SHA256.

---

# Проверка размеров ключей

Тестами проверяются ключи:

```text
16 байт
64 байта
100 байт
```

Таким образом проверены:

- ключ короче блока SHA-256;
- ключ, равный размеру блока;
- ключ длиннее блока.

---

# Пустое сообщение

HMAC корректно вычисляется для пустого сообщения:

```text
b""
```

Результат дополнительно сравнивается с эталонной реализацией Python в автоматическом тесте.

---

# Tamper Detection — изменение файла

Проверяется следующий сценарий:

1. создаётся HMAC исходного файла;
2. содержимое файла изменяется;
3. выполняется `--verify`;
4. проверка должна завершиться ошибкой.

Результат:

```text
[ERROR] HMAC verification failed
```

Это показывает, что изменение содержимого файла обнаруживается.

---

# Tamper Detection — неверный ключ

Также выполняется проверка с другим ключом.

Алгоритм:

1. HMAC создаётся с первым ключом;
2. выполняется проверка с другим ключом;
3. значения HMAC не совпадают.

Результат:

```text
[ERROR] HMAC verification failed
```

---

# Проверка потокового HMAC

Добавлен специальный автоматический тест, который контролирует вызовы:

```python
stream.read(size)
```

и проверяет, что HMAC читает данные блоками:

```text
8192 байт
```

а не загружает весь поток сразу.

Это отдельно подтверждает работу chunked processing.

---

# Проверка большого файла HMAC

Добавлен:

```text
scripts/hmac_large_file_test.py
```

Скрипт создаёт бинарный файл размером:

```text
10 485 760 байт
```

то есть:

```text
10 MiB
```

Затем HMAC вычисляется двумя способами:

1. собственной реализацией CryptoCore;
2. эталонной реализацией `hmac` + `hashlib.sha256`.

Полученные значения совпали:

```text
CryptoCore: d20bad94a922f94d99165e579e66f710efc20dc7429bf47cf0985e6303d69ea0
Reference:  d20bad94a922f94d99165e579e66f710efc20dc7429bf47cf0985e6303d69ea0
```

Результат:

```text
Large HMAC test: PASSED
```

Тестовый файл после проверки автоматически удаляется.

---

# HMAC interoperability с OpenSSL

HMAC-SHA256 можно дополнительно сравнить с OpenSSL.

CryptoCore:

```powershell
cryptocore dgst --algorithm sha256 --hmac --key 00112233445566778899aabbccddeeff --input plaintext.txt
```

OpenSSL:

```powershell
openssl dgst -sha256 -mac HMAC -macopt hexkey:00112233445566778899aabbccddeeff plaintext.txt
```

При одинаковом ключе и одинаковом входном файле полученные HMAC должны совпадать.

---

# Автоматические тесты Sprint 5

Основные новые файлы:

```text
tests/test_hmac_vectors.py
tests/test_hmac_cli.py
```

Проверяются:

- RFC 4231 Test Case 1;
- RFC 4231 Test Case 2;
- RFC 4231 Test Case 3;
- RFC 4231 Test Case 4;
- ключ 16 байт;
- ключ 64 байта;
- ключ 100 байт;
- пустое сообщение;
- incremental update;
- повторный вызов `hexdigest()`;
- ошибочный тип ключа;
- ошибочный тип сообщения;
- обязательный `--key`;
- hexadecimal key;
- HMAC файла;
- `--output`;
- успешный `--verify`;
- изменение файла;
- неправильный ключ;
- chunked processing.

---

# Запуск всех тестов

В `pyproject.toml` указано:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
```

Поэтому pytest запускает только автоматические тесты из:

```text
tests/
```

а служебные скрипты из:

```text
scripts/
```

не воспринимаются как pytest-тесты.

Запуск:

```powershell
pytest -v
```

Полный набор тестов Sprint 1–5 проходит без `FAILED` и `ERROR`.

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
|       |-- mac/
|       |   |-- __init__.py
|       |   `-- hmac.py
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
|   |-- test_hash_avalanche.py
|   |-- test_hmac_vectors.py
|   `-- test_hmac_cli.py
|
|-- scripts/
|   |-- round_trip_test.py
|   |-- openssl_interop_test.py
|   |-- generate_nist_data.py
|   |-- hash_interop_test.py
|   |-- hash_large_file_test.py
|   `-- hmac_large_file_test.py
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

- структура CryptoCore;
- CLI;
- AES-128 ECB;
- PKCS#7;
- файловый ввод-вывод;
- автоматические тесты;
- OpenSSL interoperability.

---

# Итоги Sprint 2

Реализованы:

- AES-128 CBC;
- AES-128 CFB-128;
- AES-128 OFB;
- AES-128 CTR;
- собственная логика режимов;
- генерация IV;
- параметр `--iv`;
- формат `<IV><ciphertext>`;
- двусторонняя совместимость с OpenSSL.

---

# Итоги Sprint 3

Реализованы:

- CSPRNG;
- `os.urandom()`;
- автоматическая генерация AES-ключа;
- генерация IV через CSPRNG;
- предупреждение о потенциально слабых ключах;
- автоматические тесты CSPRNG;
- подготовка данных NIST;
- полный NIST STS.

---

# Итоги Sprint 4

Реализованы:

- SHA-256 с нуля;
- SHA3-256 с нуля;
- Keccak-f[1600];
- команда `dgst`;
- `--algorithm`;
- `--input`;
- `--output`;
- binary file I/O;
- chunked processing;
- Known-Answer Tests;
- empty-message tests;
- interoperability;
- avalanche effect.

---

# Итоги Sprint 5

Реализованы:

- HMAC-SHA256 с нуля;
- использование собственной SHA-256 из Sprint 4;
- обработка HMAC-ключей произвольной длины;
- обработка ключей больше 64 байт;
- zero padding коротких ключей;
- `--hmac`;
- `--key`;
- `--verify`;
- `--output` для HMAC;
- формат `HMAC_VALUE INPUT_FILE_PATH`;
- потоковая обработка;
- безопасное сравнение HMAC;
- RFC 4231 Test Cases 1–4;
- проверка короткого ключа;
- проверка 64-байтового ключа;
- проверка 100-байтового ключа;
- проверка пустого сообщения;
- tamper detection для файла;
- tamper detection для ключа;
- проверка chunked processing;
- проверка большого файла;
- сохранение работоспособности предыдущих Sprint.

AES-CMAC в Sprint 5 не реализован, поскольку относится к дополнительному Bonus/Could требованию.

---

# Текущий результат

CryptoCore поддерживает:

```text
AES-128 ECB
AES-128 CBC
AES-128 CFB-128
AES-128 OFB
AES-128 CTR

SHA-256
SHA3-256

HMAC-SHA256
```

