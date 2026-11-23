# CryptoCore

CryptoCore — учебное консольное приложение на Python для выполнения криптографических операций с файлами.

Проект последовательно развивается по Sprint 1–7 и включает:

- AES-128 ECB;
- AES-128 CBC;
- AES-128 CFB-128;
- AES-128 OFB;
- AES-128 CTR;
- AES-128 GCM;
- PKCS#7 padding;
- генерацию IV и nonce;
- CSPRNG;
- автоматическую генерацию AES-128 ключей;
- SHA-256;
- SHA3-256;
- HMAC-SHA256;
- PBKDF2-HMAC-SHA256;
- иерархию производных ключей;
- автоматическую генерацию salt;
- AEAD;
- Associated Authenticated Data (AAD);
- Encrypt-then-MAC;
- streaming AAD;
- потоковую обработку файлов;
- проверку целостности и подлинности;
- официальные NIST test vectors;
- NIST Monte Carlo tests;
- NIST Statistical Test Suite;
- interoperability-проверки;
- автоматические security tests.

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
- OpenSSL — для части interoperability-проверок;
- WSL/Linux — для некоторых memory-limited и interoperability-тестов;
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

Активация в Windows PowerShell:

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

Проверка:

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
- hexadecimal AES-ключи;
- PKCS#7;
- binary file I/O;
- обработка ошибок;
- default output filename;
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

Пример:

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

Логика режимов шифрования реализуется в коде CryptoCore поверх AES-примитива.

---

# PKCS#7

Режимы:

```text
ECB
CBC
```

используют PKCS#7 padding.

Если длина сообщения уже кратна 16 байтам, добавляется полный блок padding.

Режимы:

```text
CFB
OFB
CTR
GCM
```

padding не используют.

---

# Файловый ввод-вывод

CryptoCore работает с файлами в бинарном режиме.

Используются:

```python
rb
wb
```

Программа может обрабатывать:

- текстовые файлы;
- бинарные файлы;
- изображения;
- архивы;
- документы;
- данные с нулевыми байтами.

---

# Default output

Параметр:

```text
--output
```

можно не указывать.

При шифровании автоматически используется:

```text
<input>.enc
```

При расшифровании:

```text
<input>.dec
```

---

# Round-trip Sprint 1

Скрипт:

```text
scripts/round_trip_test.py
```

Запуск:

```powershell
python .\scripts\round_trip_test.py
```

Проверяется:

```text
plaintext
   ↓
encryption
   ↓
ciphertext
   ↓
decryption
   ↓
restored plaintext
```

Исходный и восстановленный файлы должны полностью совпадать.

---

# Sprint 2 — дополнительные режимы AES

Добавлены:

- AES-128 CBC;
- AES-128 CFB-128;
- AES-128 OFB;
- AES-128 CTR;
- генерация IV;
- параметр `--iv`;
- формат `<IV><ciphertext>`;
- двусторонняя interoperability с OpenSSL.

---

# AES-128 CBC

CBC использует IV длиной:

```text
16 байт
```

Для первого блока используется IV.

Каждый plaintext-блок перед AES объединяется через XOR с предыдущим ciphertext-блоком.

CBC использует PKCS#7.

Шифрование:

```powershell
cryptocore --algorithm aes --mode cbc --encrypt --key 000102030405060708090a0b0c0d0e0f --input plaintext.txt --output encrypted_cbc.bin
```

Расшифрование:

```powershell
cryptocore --algorithm aes --mode cbc --decrypt --key 000102030405060708090a0b0c0d0e0f --input encrypted_cbc.bin --output decrypted_cbc.txt
```

---

# AES-128 CFB-128

CFB реализован с размером сегмента:

```text
128 бит
```

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

CTR использует IV как начальное значение 128-битного счётчика.

Для каждого блока:

1. значение счётчика шифруется AES;
2. формируется keystream;
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

Для:

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

При шифровании IV генерируется автоматически.

Формат:

```text
16-byte IV || ciphertext
```

При расшифровании CryptoCore автоматически извлекает первые 16 байт как IV.

Также при расшифровании можно передать IV явно:

```powershell
cryptocore --algorithm aes --mode cbc --decrypt --key 000102030405060708090a0b0c0d0e0f --iv AABBCCDDEEFF00112233445566778899 --input ciphertext.bin --output restored.txt
```

---

# OpenSSL interoperability AES

Скрипт:

```text
scripts/openssl_interop_test.py
```

Запуск:

```powershell
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

в направлениях:

```text
CryptoCore -> OpenSSL
OpenSSL -> CryptoCore
```

Для ECB дополнительно выполняется прямое сравнение ciphertext.

Подтверждённый результат:

```text
Result: 11/11 checks passed
OpenSSL interoperability: PASSED
```

---

# Sprint 3 — CSPRNG и управление ключами

Реализованы:

- отдельный CSPRNG;
- `os.urandom()`;
- автоматическая генерация AES-128 ключа;
- генерация IV через общий CSPRNG;
- проверка потенциально слабых ключей;
- 1000-key uniqueness test;
- базовая проверка распределения;
- end-to-end auto-key test;
- генерация данных для NIST STS;
- полный запуск NIST Statistical Test Suite.

---

# CSPRNG

Модуль:

```text
src/cryptocore/csprng.py
```

Функция:

```python
generate_random_bytes(num_bytes: int) -> bytes
```

Для генерации используется:

```python
os.urandom()
```

Модуль:

```python
random
```

для генерации криптографических ключей и IV не используется.

CSPRNG применяется для:

- AES-128 ключей;
- IV;
- GCM nonce;
- PBKDF2 salt;
- данных NIST STS.

---

# Автоматическая генерация AES-ключа

При шифровании `--key` является необязательным.

Пример:

```powershell
cryptocore --algorithm aes --mode ctr --encrypt --input plaintext.txt --output ciphertext.bin
```

CryptoCore генерирует случайный AES-128 ключ:

```text
[INFO] Generated random key: <hex-key>
```

Ключ:

- имеет длину 16 байт;
- создаётся CSPRNG;
- выводится в hexadecimal;
- не записывается в ciphertext.

При расшифровании `--key` обязателен.

---

# End-to-end auto-key test

Файл:

```text
tests/test_sprint3_auto_key_e2e.py
```

Проверяется полный сценарий:

```text
encrypt without --key
        ↓
generated key
        ↓
extract key from stdout
        ↓
decrypt with generated key
        ↓
original == restored
```

---

# Проверка потенциально слабых ключей

Предупреждение выводится для очевидно слабых пользовательских ключей:

- полностью повторяющиеся байты;
- полностью нулевой ключ;
- `00–0F`;
- `0F–00`.

Пример:

```text
00000000000000000000000000000000
```

Сообщение:

```text
[WARNING] Обнаружен потенциально слабый AES-ключ: ...
```

Операция не блокируется.

---

# CSPRNG tests

Файл:

```text
tests/test_csprng.py
```

Проверяются:

- длина результата;
- тип;
- ошибки входных параметров;
- ошибка `os.urandom`;
- генерация 1000 уникальных AES-ключей;
- базовое распределение единичных битов.

Используется диапазон:

```text
0.45 <= one_ratio <= 0.55
```

---

# NIST Statistical Test Suite

Для дополнительной статистической проверки CSPRNG использовался:

```text
NIST Statistical Test Suite 2.1.2
```

Модуль подготовки данных:

```text
src/cryptocore/nist_data.py
```

Скрипт:

```text
scripts/generate_nist_data.py
```

Создаёт:

```text
nist_test_data.bin
```

Размер:

```text
10 000 000 байт
```

или:

```text
80 000 000 бит
```

Параметры выполненного тестирования:

```text
Длина последовательности: 1 000 000 бит
Количество последовательностей: 80
Количество групп тестов: 15
```

Запуск NIST STS:

```bash
./assess 1000000
```

Используется binary input.

Основной статистический порог:

```text
p-value >= 0.01
```

Были выполнены все 15 групп статистических тестов NIST STS.

---

# Sprint 4 — SHA-256 и SHA3-256

Реализованы:

- SHA-256;
- SHA3-256;
- Keccak-f[1600];
- команда `dgst`;
- hexadecimal digest;
- `--output`;
- streaming;
- constant-memory processing;
- NIST vectors;
- NIST Monte Carlo;
- avalanche effect;
- interoperability;
- файл >1 GiB.

Основная реализация SHA не использует `hashlib`.

---

# SHA-256

Реализация:

```text
src/cryptocore/hash/sha256.py
```

Пример:

```powershell
cryptocore dgst --algorithm sha256 --input plaintext.txt
```

---

# SHA3-256

Реализация:

```text
src/cryptocore/hash/sha3_256.py
```

Пример:

```powershell
cryptocore dgst --algorithm sha3-256 --input plaintext.txt
```

---

# Сохранение digest

```powershell
cryptocore dgst --algorithm sha256 --input plaintext.txt --output plaintext.sha256
```

---

# Streaming hash

Файлы обрабатываются блоками:

```text
8192 байт
```

Полный файл не загружается в память.

---

# NIST SHA test vectors

В каталоге:

```text
tests/vectors/nist/
```

находятся:

```text
SHA256ShortMsg.rsp
SHA256LongMsg.rsp
SHA256Monte.rsp

SHA3_256ShortMsg.rsp
SHA3_256LongMsg.rsp
SHA3_256Monte.rsp
```

Автоматические проверки:

```text
tests/test_nist_hash_vectors.py
```

и:

```text
scripts/nist_hash_monte_test.py
```

---

# Hash interoperability

Скрипт:

```text
scripts/hash_interop_test.py
```

Проверяет SHA-256 и SHA3-256 против независимых системных реализаций.

Для SHA-256 поддерживается:

```text
sha256sum
```

Для SHA3-256:

```text
sha3sum -a 256
```

и дополнительные fallback-варианты.

---

# Avalanche effect

Тест:

```text
tests/test_hash_avalanche.py
```

Изменяется один бит входного сообщения, после чего сравниваются 256-битные digest.

Проверяются:

```text
SHA-256
SHA3-256
```

---

# Файл больше 1 GiB

Скрипт:

```text
scripts/hash_large_file_test.py
```

создаёт файл:

```text
1 GiB + 1 байт
```

и сравнивает результаты CryptoCore с Python reference implementation.

Автоматический streaming test:

```text
tests/test_large_hash_streaming.py
```

проверяет обработку логического объёма >1 GiB без загрузки всего входа в память.

---

# Sprint 5 — HMAC-SHA256

Добавлен:

```text
HMAC-SHA256
```

Реализация:

```text
src/cryptocore/mac/hmac.py
```

В основной реализации не используются:

```python
hmac
hashlib
```

Внутренней хеш-функцией является собственная SHA-256.

---

# Конструкция HMAC

Используется RFC 2104:

```text
HMAC(K, m) =
H((K XOR opad) || H((K XOR ipad) || m))
```

где:

```text
H = SHA-256
ipad = 0x36
opad = 0x5C
```

Размер блока:

```text
64 байта
```

---

# Обработка HMAC-ключей

Если:

```text
len(key) > 64
```

выполняется:

```text
key = SHA256(key)
```

Если:

```text
len(key) < 64
```

ключ дополняется нулями до 64 байт.

---

# CLI HMAC

Пример:

```powershell
cryptocore dgst --algorithm sha256 --hmac --key 00112233445566778899aabbccddeeff --input plaintext.txt
```

---

# Сохранение HMAC

```powershell
cryptocore dgst --algorithm sha256 --hmac --key 00112233445566778899aabbccddeeff --input plaintext.txt --output plaintext.hmac
```

---

# Проверка HMAC

```powershell
cryptocore dgst --algorithm sha256 --hmac --key 00112233445566778899aabbccddeeff --input plaintext.txt --verify plaintext.hmac
```

Успех:

```text
[OK] HMAC verification successful
```

Exit code:

```text
0
```

Ошибка:

```text
[ERROR] HMAC verification failed
```

Exit code:

```text
1
```

Для безопасного сравнения используется:

```python
secrets.compare_digest()
```

---

# RFC 4231

Файл:

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

Также проверяются ключи:

```text
16 байт
64 байта
100 байт
```

и empty input.

---

# Tamper Detection HMAC

Автоматически проверяется:

- изменение файла;
- неправильный ключ;
- неправильный HMAC.

При несовпадении проверка завершается ошибкой.

---

# HMAC большого файла

Скрипт:

```text
scripts/hmac_large_file_test.py
```

проверяет настоящий HMAC файла размером:

```text
10 MiB
```

CryptoCore сравнивается с:

```python
hmac.new(..., hashlib.sha256)
```

---

# Huge HMAC streaming

Скрипт:

```text
scripts/hmac_huge_streaming_test.py
```

проверяет streaming-архитектуру на виртуальном входе:

```text
>20 GiB
```

Максимальный размер чтения:

```text
8192 байт
```

---

# Memory-limited HMAC

Скрипт:

```text
scripts/hmac_memory_limited_test.py
```

запускается в Linux/WSL.

Используется:

```text
RLIMIT_AS
```

Создаётся sparse-файл, размер которого больше доступной процессу памяти.

CryptoCore выполняет настоящий HMAC-SHA256 потоково.

---

# Sprint 6 — Authenticated Encryption

Цель Sprint 6 — объединить шифрование и проверку подлинности в одной безопасной операции.

Реализованы:

- AES-128 GCM;
- AEAD;
- Associated Authenticated Data;
- GHASH;
- GF(2^128);
- 12-byte nonce;
- 16-byte authentication tag;
- Encrypt-then-MAC;
- key separation;
- streaming AAD;
- catastrophic authentication failure;
- NIST GCM Known-Answer Tests;
- tamper detection;
- GCM interoperability.

---

# AEAD

AEAD:

```text
Authenticated Encryption with Associated Data
```

обеспечивает:

- конфиденциальность;
- целостность;
- аутентификацию;
- защиту дополнительных связанных данных.

AAD не шифруется, но участвует в формировании authentication tag.

Примеры AAD:

- заголовок протокола;
- идентификатор сообщения;
- версия формата;
- метаданные.

Если AAD изменяется, проверка authentication tag завершается ошибкой.

---

# AES-128 GCM

Основная реализация:

```text
src/cryptocore/modes/gcm.py
```

Для базового AES-примитива применяется:

```python
AES.MODE_ECB
```

При этом логика GCM реализована самостоятельно.

Основная реализация CryptoCore не использует:

```python
AES.MODE_GCM
```

Самостоятельно реализованы:

- GCTR;
- GHASH;
- `inc32`;
- J0;
- обработка nonce;
- AAD;
- authentication tag;
- verification.

---

# GHASH и GF(2^128)

GHASH использует конечное поле:

```text
GF(2^128)
```

с неприводимым полиномом:

```text
x^128 + x^7 + x^2 + x + 1
```

Умножение реализовано функциями:

```text
gf_multiply() — эталонная побитовая реализация;
gf_multiply_precomputed() — оптимизированная рабочая реализация.
```

Для рабочего GHASH используется предварительно вычисленная 4-битная lookup table.

Таблица строится для hash subkey H и кэшируется, что уменьшает количество операций при повторных умножениях в GF(2^128).

---

# GCM nonce

При обычном GCM-шифровании генерируется случайный nonce:

```text
12 байт
```

или:

```text
96 бит
```

Nonce генерируется через общий CSPRNG проекта.

Для расшифрования поддерживается:

```text
--nonce
```

Для обратной совместимости также разрешён:

```text
--iv
```

в режиме GCM decrypt.

Одновременно использовать `--nonce` и `--iv` нельзя.

---

# Формат GCM ciphertext

Формат выходного файла:

```text
Nonce || Ciphertext || Tag
```

где:

```text
Nonce = 12 байт
Tag   = 16 байт
```

То есть:

```text
12-byte nonce || ciphertext || 16-byte authentication tag
```

AES-ключ и AAD в ciphertext не записываются.

---

# AAD

Для GCM используется:

```text
--aad
```

AAD передаётся как hexadecimal string.

Пример:

```text
aabbccddeeff
```

Если параметр отсутствует:

```text
AAD = empty
```

AAD:

- не шифруется;
- не записывается в ciphertext;
- участвует в authentication.

Для успешной расшифровки необходимо использовать то же значение AAD.

---

# GCM encryption

Пример:

```powershell
cryptocore --algorithm aes --mode gcm --encrypt --key 00112233445566778899aabbccddeeff --input plaintext.txt --output ciphertext.bin --aad aabbccddeeff
```

CryptoCore:

1. генерирует 12-byte nonce;
2. шифрует plaintext;
3. вычисляет GHASH;
4. формирует authentication tag;
5. сохраняет `nonce || ciphertext || tag`.

---

# GCM decryption

```powershell
cryptocore --algorithm aes --mode gcm --decrypt --key 00112233445566778899aabbccddeeff --input ciphertext.bin --output decrypted.txt --aad aabbccddeeff
```

При расшифровании:

1. первые 12 байт читаются как nonce;
2. последние 16 байт читаются как tag;
3. оставшиеся байты являются ciphertext;
4. tag проверяется;
5. только после успешной проверки выполняется decrypt.

---

# Явный nonce

Если nonce передаётся отдельно:

```powershell
cryptocore --algorithm aes --mode gcm --decrypt --key 00112233445566778899aabbccddeeff --nonce aabbccddeeff001122334455 --input ciphertext_and_tag.bin --output restored.txt --aad aabbccddeeff
```

В этом случае входной файл содержит:

```text
ciphertext || tag
```

---

# Authentication failure

GCM использует fail-closed поведение.

Если:

- AAD неправильный;
- ciphertext изменён;
- tag изменён;
- используется неправильный ключ;

authentication завершается ошибкой.

Пример:

```text
[ERROR] Authentication failed: AAD mismatch or ciphertext/tag tampered.
```

Exit code:

```text
1
```

Критическое правило:

```text
plaintext не выдаётся до успешной authentication
```

Выходной файл с расшифрованными данными не создаётся.

---

# Почему authentication failure критична

Неправильный tag может означать:

- повреждение данных;
- неправильный AAD;
- неправильный ключ;
- изменение ciphertext;
- попытку подделки.

После authentication failure plaintext нельзя считать достоверным.

Поэтому CryptoCore полностью прекращает операцию.

---

# NIST AES-GCM Known-Answer Tests

Файл:

```text
tests/test_gcm.py
```

Проверяются AES-GCM known-answer examples.

Покрываются:

- empty plaintext;
- empty AAD;
- непустой plaintext;
- непустой AAD;
- ciphertext;
- authentication tag;
- decryption;
- nonce нестандартной длины;
- wrong tag;
- wrong AAD.

---

# GCM CLI tests

Файл:

```text
tests/test_gcm_cli.py
```

Проверяется:

- GCM через реальный `python -m cryptocore`;
- round-trip;
- формат файла;
- 12-byte nonce;
- 16-byte tag;
- empty AAD;
- explicit nonce.

---

# GCM Security Tests

Файл:

```text
tests/test_gcm_security.py
```

Проверяются:

- wrong AAD;
- modified ciphertext;
- modified tag;
- отсутствие output-файла;
- non-zero exit code;
- authentication error;
- правильный AAD;
- 1000 уникальных nonce.

Тест nonce:

```text
1000 encryptions
```

ожидает:

```text
1000 unique 12-byte nonces
```

---

# Streaming AAD

Модуль:

```text
src/cryptocore/aead/gcm_stream.py
```

позволяет обрабатывать AAD по частям.

AAD не требуется полностью загружать в оперативную память.

Размер чтения по умолчанию:

```text
8192 байт
```

Тесты:

```text
tests/test_gcm_streaming_aad.py
```

Проверяется:

- совместимость с обычным GCM;
- round-trip;
- wrong streaming AAD;
- ограниченный размер чтения;
- логический AAD размером более 20 GiB.

Большой виртуальный тест проверяет архитектуру constant-memory streaming.

Криптографическая корректность GHASH отдельно проверяется known-answer tests.

---

# GCM interoperability

Скрипт:

```text
scripts/gcm_interop_test.py
```

CryptoCore сравнивается с независимой реализацией AES-GCM из PyCryptodome.

Проверяются:

```text
CryptoCore -> reference
reference -> CryptoCore
```

Сравниваются:

- ciphertext;
- authentication tag;
- plaintext после decrypt.

Успех:

```text
CryptoCore -> reference: PASSED
Reference -> CryptoCore: PASSED
AES-GCM interoperability: PASSED
```

Команда `openssl enc` не используется как основной reference для GCM, поскольку интерфейс `openssl enc` не поддерживает AEAD GCM/CCM.

---

# Encrypt-then-MAC

Дополнительно реализована композиция:

```text
Encrypt-then-MAC
```

Модуль:

```text
src/cryptocore/aead/encrypt_then_mac.py
```

Используются:

```text
AES-128 CTR
+
HMAC-SHA256
```

Схема:

```text
C = E(K_e, P)

T = MAC(K_m, C || AAD)
```

В реализации также аутентифицируется IV.

Формат:

```text
IV || ciphertext || HMAC-SHA256 tag
```

---

# Key separation

Для AES и HMAC используются разные производные ключи.

Из master key создаются:

```text
K_e — encryption key
K_m — MAC key
```

Используются отдельные domain-separation labels.

Это предотвращает использование одного рабочего ключа одновременно в AES и HMAC.

---

# Encrypt-then-MAC verification

При расшифровании сначала выполняется:

```text
HMAC verification
```

И только после успешного MAC:

```text
AES-CTR decryption
```

Если изменён:

- IV;
- ciphertext;
- AAD;
- tag;
- master key;

возникает authentication error.

---

# Encrypt-then-MAC tests

Файл:

```text
tests/test_encrypt_then_mac.py
```

Проверяются:

- key separation;
- deterministic derivation;
- round-trip;
- wrong AAD;
- IV tamper;
- ciphertext tamper;
- tag tamper;
- wrong master key;
- empty AAD;
- random IV;
- отсутствие decrypt до успешной authentication.

---

# Security properties Sprint 6

AES-GCM и Encrypt-then-MAC обеспечивают:

```text
Confidentiality
+
Integrity
+
Authentication
```

AAD позволяет аутентифицировать метаданные без их шифрования.

Основное правило:

```text
Authenticate before releasing plaintext.
```

При любой ошибке authentication данные считаются недостоверными.

---

# Sprint 7 — Key Derivation Functions

Цель Sprint 7 — реализовать безопасное получение криптографических ключей из паролей и master key.

Реализованы:

- PBKDF2-HMAC-SHA256;
- собственная реализация PBKDF2;
- использование HMAC-SHA256 из Sprint 5;
- произвольная длина password и salt;
- произвольная длина производного ключа;
- автоматическая генерация 16-byte salt;
- команда `derive`;
- key hierarchy;
- context separation;
- OpenSSL interoperability;
- тест 1000 уникальных salt;
- performance tests.

---

# PBKDF2-HMAC-SHA256

Реализация:

```text
src/cryptocore/kdf/pbkdf2.py
```

PBKDF2 реализован самостоятельно.

Используется:

```text
HMAC-SHA256
```

из Sprint 5, который в свою очередь использует собственную реализацию SHA-256 из Sprint 4.

Стандартная библиотечная функция:

```python
hashlib.pbkdf2_hmac()
```

в основной реализации PBKDF2 не используется.

Основная формула:

```text
DK = T1 || T2 || ... || Tn
```

где:

```text
Ti = U1 XOR U2 XOR ... XOR Uc
```

и:

```text
U1 = PRF(P, S || INT_32_BE(i))
Uj = PRF(P, Uj-1)
```

В качестве PRF используется:

```text
HMAC-SHA256
```

---

# Команда derive

Для получения ключа из пароля используется:

```powershell
cryptocore derive --password "password"
```

Поддерживаемые параметры:

```text
--password PASSWORD
--salt SALT
--iterations COUNT
--length LENGTH
--algorithm pbkdf2
--output FILE
```

Количество итераций по умолчанию:

```text
100000
```

Длина производного ключа по умолчанию:

```text
32 байта
```

Если `--salt` не указан, CryptoCore автоматически создаёт случайный salt длиной:

```text
16 байт
```

через общий CSPRNG проекта.

---

# Формат salt

Пользовательский salt передаётся как hexadecimal string.

Пример:

```text
73616c74
```

что соответствует байтам:

```text
salt
```

Пример команды:

```powershell
cryptocore derive --password "password" --salt 73616c74 --iterations 1 --length 32
```

Результат:

```text
120fb6cffcf8b32c43e7225256c4f837a86548c92ccc35480805987cb70be17b 73616c74
```

Формат stdout:

```text
KEY_HEX SALT_HEX
```

---

# Автоматический salt

Если salt не указан:

```powershell
cryptocore derive --password "MyPassword"
```

генерируется новый случайный 16-byte salt.

Повторный запуск с тем же паролем создаёт другой salt и, соответственно, другой производный ключ.

Автоматический тест:

```text
tests/test_derive_cli.py
```

проверяет:

```text
1000 generated salts
=
1000 unique salts
```

---

# Количество итераций

Параметр:

```text
--iterations
```

определяет число последовательных вычислений HMAC-SHA256.

Увеличение количества итераций увеличивает стоимость перебора пароля.

Пример:

```powershell
cryptocore derive --password "MyPassword" --iterations 100000
```

Значение должно быть положительным целым числом.

---

# Длина ключа

Параметр:

```text
--length
```

задаёт длину производного ключа в байтах.

Пример:

```powershell
cryptocore derive --password "MyPassword" --length 16
```

PBKDF2 поддерживает получение ключей требуемой длины посредством формирования нескольких блоков:

```text
T1 || T2 || ...
```

и последующего усечения до указанной длины.

---

# Сохранение производного ключа

Параметр:

```text
--output
```

позволяет сохранить производный ключ в файл.

Пример:

```powershell
cryptocore derive --password "password" --salt 73616c74 --iterations 1 --length 32 --output derived_key.bin
```

В файл записывается:

```text
raw binary key
```

а не hexadecimal-представление.

Salt в файл ключа автоматически не добавляется.

---

# Key hierarchy

Реализация:

```text
src/cryptocore/kdf/hkdf.py
```

Функция:

```python
derive_key(
    master_key: bytes,
    context: str,
    length: int,
) -> bytes
```

используется для получения нескольких независимых ключей из одного master key.

Для каждого блока применяется:

```text
HMAC(master_key, context || counter)
```

Примеры context:

```text
encryption
authentication
```

Разные context создают разные производные ключи:

```text
K_encryption != K_authentication
```

Это обеспечивает domain separation между ключами различного назначения.

---

# PBKDF2 Known-Answer Tests

Файл:

```text
tests/test_pbkdf2.py
```

Проверяются известные PBKDF2-HMAC-SHA256 значения.

Пример:

```text
password = password
salt = salt
iterations = 1
dkLen = 32
```

Ожидаемый результат:

```text
120fb6cffcf8b32c43e7225256c4f837
a86548c92ccc35480805987cb70be17b
```

Также проверяются:

- deterministic derivation;
- разные password;
- разные salt;
- различные длины производного ключа;
- строковые password;
- некорректное количество итераций;
- некорректная длина ключа.

---

# OpenSSL interoperability PBKDF2

Файл:

```text
tests/test_pbkdf2_openssl.py
```

Результат CryptoCore сравнивается с независимой реализацией:

```text
OpenSSL PBKDF2
```

Поддерживается поиск OpenSSL:

```text
Windows OpenSSL
```

и fallback:

```text
WSL OpenSSL
```

CryptoCore и OpenSSL должны формировать одинаковый производный ключ при одинаковых:

```text
password
salt
iteration count
key length
SHA-256
```

Проверка проходит успешно.

---

# PBKDF2 performance

Файл:

```text
tests/test_pbkdf2_performance.py
```

На тестовой системе:

```text
Windows
Python 3.11.9
```

были получены результаты:

```text
10 000 iterations  ≈ 7.2 s
100 000 iterations ≈ 70 s
```

Тест на:

```text
1 000 000 iterations
```

помечен как:

```text
slow
```

и не входит в обычный запуск тестов.

Причина относительно высокой стоимости — PBKDF2 использует собственные Python-реализации HMAC-SHA256 и SHA-256, а не оптимизированные системные реализации.

Обычный запуск:

```powershell
pytest -v -m "not slow"
```

Отдельный запуск slow-теста:

```powershell
pytest .\tests\test_pbkdf2_performance.py -v -s -m slow
```

---

# Security considerations KDF

Для реального использования необходимо:

- использовать уникальный случайный salt;
- не использовать salt как секрет;
- использовать достаточно большое количество PBKDF2-итераций;
- увеличивать iteration count по мере роста производительности оборудования;
- использовать разные context для ключей разного назначения;
- не использовать производный encryption key как authentication key;
- использовать стойкие пользовательские пароли.

Salt предотвращает получение одинаковых производных ключей для одинаковых паролей при использовании разных salt.

Iteration count увеличивает стоимость brute-force и dictionary attacks.

PBKDF2 не заменяет необходимость использования сильных паролей.

---

# Автоматические тесты

Основные тестовые файлы:

```text
tests/test_cbc.py
tests/test_cfb.py
tests/test_cli.py
tests/test_csprng.py
tests/test_ctr.py

tests/test_derive_cli.py

tests/test_digest.py
tests/test_digest_cli.py
tests/test_ecb.py

tests/test_encrypt_then_mac.py

tests/test_gcm.py
tests/test_gcm_cli.py
tests/test_gcm_security.py
tests/test_gcm_streaming_aad.py

tests/test_hash_avalanche.py

tests/test_hmac_cli.py
tests/test_hmac_vectors.py

tests/test_iv.py

tests/test_kdf_hierarchy.py

tests/test_large_hash_streaming.py
tests/test_modes_integration.py
tests/test_nist_data.py
tests/test_nist_hash_vectors.py

tests/test_ofb.py
tests/test_padding.py

tests/test_pbkdf2.py
tests/test_pbkdf2_openssl.py
tests/test_pbkdf2_performance.py

tests/test_sha256.py
tests/test_sha3_256.py
tests/test_sprint3_auto_key_e2e.py
```

Обычный запуск без долгих тестов:

```powershell
pytest -v -m "not slow"
```

Текущий результат:

```text
272 passed
1 deselected
0 failed
```

Slow-тест запускается отдельно:

```powershell
pytest -v -m slow
```

В `pyproject.toml`:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]

markers = [
    "slow: долгие тесты производительности",
]
```

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
|       |-- derive.py
|       |-- digest.py
|       |-- digest_cli.py
|       |-- file_io.py
|       |-- iv.py
|       |-- nist_data.py
|       |-- padding.py
|       |
|       |-- aead/
|       |   |-- __init__.py
|       |   |-- encrypt_then_mac.py
|       |   `-- gcm_stream.py
|       |
|       |-- hash/
|       |   |-- __init__.py
|       |   |-- sha256.py
|       |   `-- sha3_256.py
|       |
|       |-- kdf/
|       |   |-- __init__.py
|       |   |-- hkdf.py
|       |   `-- pbkdf2.py
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
|           |-- gcm.py
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
|   |-- test_derive_cli.py
|   |-- test_digest.py
|   |-- test_digest_cli.py
|   |-- test_ecb.py
|   |-- test_encrypt_then_mac.py
|   |-- test_gcm.py
|   |-- test_gcm_cli.py
|   |-- test_gcm_security.py
|   |-- test_gcm_streaming_aad.py
|   |-- test_hash_avalanche.py
|   |-- test_hmac_cli.py
|   |-- test_hmac_vectors.py
|   |-- test_iv.py
|   |-- test_kdf_hierarchy.py
|   |-- test_large_hash_streaming.py
|   |-- test_modes_integration.py
|   |-- test_nist_data.py
|   |-- test_nist_hash_vectors.py
|   |-- test_ofb.py
|   |-- test_padding.py
|   |-- test_pbkdf2.py
|   |-- test_pbkdf2_openssl.py
|   |-- test_pbkdf2_performance.py
|   |-- test_sha256.py
|   |-- test_sha3_256.py
|   `-- test_sprint3_auto_key_e2e.py
|
|-- scripts/
|   |-- gcm_interop_test.py
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

Переустановка editable package:

```powershell
pip install -e .
```

Все обычные автоматические тесты:

```powershell
pytest -v -m "not slow"
```

Slow performance test:

```powershell
pytest -v -m slow
```

Sprint 1 round-trip:

```powershell
python .\scripts\round_trip_test.py
```

AES/OpenSSL:

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

Hash >1 GiB:

```powershell
python .\scripts\hash_large_file_test.py
```

HMAC 10 MiB:

```powershell
python .\scripts\hmac_large_file_test.py
```

Huge HMAC streaming:

```powershell
python .\scripts\hmac_huge_streaming_test.py
```

Memory-limited HMAC в WSL:

```bash
PYTHONPATH=src python3 scripts/hmac_memory_limited_test.py
```

GCM interoperability:

```powershell
python .\scripts\gcm_interop_test.py
```

PBKDF2/OpenSSL:

```powershell
pytest .\tests\test_pbkdf2_openssl.py -v
```

PBKDF2 performance без slow-теста:

```powershell
pytest .\tests\test_pbkdf2_performance.py -v -s -m "not slow"
```

---

# Итоги Sprint 1

Реализованы:

- Git repository;
- build system;
- CLI;
- AES-128 ECB;
- PKCS#7;
- binary I/O;
- errors;
- default output;
- round-trip;
- OpenSSL interoperability.

---

# Итоги Sprint 2

Реализованы:

- CBC;
- CFB-128;
- OFB;
- CTR;
- IV generation;
- `--iv`;
- `IV || ciphertext`;
- automatic IV extraction;
- OpenSSL interoperability.

---

# Итоги Sprint 3

Реализованы:

- CSPRNG;
- `os.urandom`;
- automatic AES-128 key generation;
- common CSPRNG for keys and IV;
- weak-key warning;
- 1000 unique keys;
- distribution test;
- end-to-end auto-key test;
- NIST data;
- NIST STS.

---

# Итоги Sprint 4

Реализованы:

- SHA-256;
- SHA3-256;
- Keccak-f[1600];
- `dgst`;
- streaming;
- constant-memory hashing;
- NIST Short Message;
- NIST Long Message;
- NIST Monte Carlo;
- interoperability;
- avalanche effect;
- >1 GiB tests.

---

# Итоги Sprint 5

Реализованы:

- HMAC-SHA256;
- собственная SHA-256;
- RFC 2104;
- keys arbitrary length;
- `--hmac`;
- `--key`;
- `--verify`;
- RFC 4231 cases 1–4;
- 16/64/100-byte keys;
- empty file;
- tamper detection;
- CLI exit codes;
- 10 MiB real HMAC;
- >20 GiB streaming;
- memory-limited HMAC.

AES-CMAC не реализован, поскольку относится к дополнительному Bonus/Could требованию.

---

# Итоги Sprint 6

Реализованы:

- AES-128 GCM;
- собственная логика GCM поверх AES;
- GCTR;
- GHASH;
- GF(2^128);
- polynomial `x^128 + x^7 + x^2 + x + 1`;
- 12-byte random nonce;
- support non-96-bit nonce through GHASH;
- 16-byte authentication tag;
- `nonce || ciphertext || tag`;
- `--aad`;
- empty AAD;
- `--nonce`;
- backward-compatible `--iv` for GCM decrypt;
- catastrophic authentication failure;
- отсутствие plaintext до проверки tag;
- NIST GCM Known-Answer Tests;
- wrong-AAD test;
- ciphertext tamper test;
- tag tamper test;
- 1000 unique nonce test;
- streaming AAD;
- virtual AAD >20 GiB;
- GCM interoperability;
- Encrypt-then-MAC;
- AES-CTR + HMAC-SHA256;
- key separation;
- Encrypt-then-MAC tamper detection.

---

# Итоги Sprint 7

Реализованы:

- PBKDF2-HMAC-SHA256;
- PBKDF2 поверх собственного HMAC-SHA256;
- собственный SHA-256 используется через HMAC;
- `cryptocore derive`;
- `--password`;
- `--salt`;
- автоматический 16-byte salt;
- `--iterations`;
- `--length`;
- `--algorithm pbkdf2`;
- `--output`;
- binary key output;
- key hierarchy;
- context separation;
- known-answer tests;
- OpenSSL interoperability;
- 1000 unique salt test;
- performance tests;
- отдельный slow performance test для 1 000 000 итераций.

---

# Текущий результат

CryptoCore поддерживает:

```text
AES-128 ECB
AES-128 CBC
AES-128 CFB-128
AES-128 OFB
AES-128 CTR
AES-128 GCM

CSPRNG

SHA-256
SHA3-256

HMAC-SHA256

PBKDF2-HMAC-SHA256
Key Derivation
Key Hierarchy

AEAD
Associated Authenticated Data
Encrypt-then-MAC
Streaming AAD
```

Текущий результат полного обычного набора тестов:

```text
272 passed
1 deselected
0 failed
```

Долгий PBKDF2-тест на 1 000 000 итераций вынесен в отдельный `slow` marker.