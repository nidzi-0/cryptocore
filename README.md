# CryptoCore

CryptoCore — учебное консольное приложение на Python для выполнения криптографических операций с файлами.

Проект последовательно развивается по Sprint и на текущем этапе включает:

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

Клонирование:

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

В Sprint 1 была создана базовая структура проекта.

Реализованы:

- CLI;
- AES-128 ECB;
- PKCS#7 padding;
- работа с файлами;
- автоматические тесты;
- проверка совместимости с OpenSSL.

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

Для ECB применяется PKCS#7 padding.

---

# PKCS#7

Режимы:

```text
ECB
CBC
```

используют PKCS#7 padding.

Если длина данных уже кратна 16 байтам, добавляется полный блок padding.

Режимы:

```text
CFB
OFB
CTR
```

работают без padding.

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
- двусторонняя interoperability-проверка с OpenSSL.

Логика режимов реализована самостоятельно поверх AES-примитива.

---

# AES-128 CBC

CBC использует IV длиной:

```text
16 байт
```

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

используется IV длиной 16 байт.

ECB IV не использует.

При обычном шифровании IV создаётся автоматически.

Формат файла:

```text
<16-byte IV><ciphertext>
```

AES-ключ в ciphertext не записывается.

При расшифровании IV автоматически извлекается из первых 16 байт файла.

Также поддерживается явное указание IV:

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
- проверка потенциально слабых ключей;
- тесты уникальности;
- проверка распределения битов;
- генерация данных NIST;
- статистическая проверка через NIST STS.

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

Для генерации криптографически стойких случайных данных используется:

```python
os.urandom()
```

Стандартный модуль:

```python
random
```

для генерации ключей и IV не используется.

---

# Автоматическая генерация AES-ключа

При шифровании `--key` можно не указывать.

Пример:

```powershell
cryptocore --algorithm aes --mode ctr --encrypt --input plaintext.txt --output ciphertext.bin
```

В этом случае CryptoCore создаёт случайный AES-128 ключ.

Программа выводит:

```text
[INFO] Generated random key: <hex-key>
```

Сгенерированный ключ:

- имеет длину 16 байт;
- создаётся через CSPRNG;
- выводится в hexadecimal-формате;
- не записывается в ciphertext.

Для расшифрования ключ должен быть известен пользователю.

---

# Проверка потенциально слабых AES-ключей

CryptoCore обнаруживает некоторые очевидные слабые пользовательские ключи.

Проверяются:

- одинаковые повторяющиеся байты;
- полностью нулевой ключ;
- последовательность `00–0F`;
- обратная последовательность `0F–00`.

Пример:

```text
00000000000000000000000000000000
```

Вывод:

```text
[WARNING] Обнаружен потенциально слабый AES-ключ: ...
```

Операция при этом не прерывается.

---

# NIST STS

Для статистической проверки CSPRNG использовалась:

```text
NIST Statistical Test Suite 2.1.2
```

Подготовка данных:

```text
scripts/generate_nist_data.py
```

Создаётся файл:

```text
nist_test_data.bin
```

Размер:

```text
10 000 000 байт
```

Параметры проверки:

```text
Размер последовательности: 1 000 000 бит
Количество последовательностей: 80
Общий объём: 80 000 000 бит
```

Были запущены все 15 групп статистических тестов NIST STS.

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

Проверяются:

```text
ECB
CBC
CFB
OFB
CTR
```

Для каждого режима выполняется проверка:

```text
CryptoCore -> OpenSSL
OpenSSL -> CryptoCore
```

Для ECB дополнительно выполняется прямое сравнение ciphertext.

Полученный результат:

```text
Result: 11/11 checks passed
OpenSSL interoperability: PASSED
```

---

# Sprint 4 — криптографические хеш-функции

В Sprint 4 реализованы:

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
- проверка обработки объёма более 1 GiB.

---

# SHA-256

Реализация:

```text
src/cryptocore/hash/sha256.py
```

SHA-256 реализован самостоятельно без использования `hashlib` внутри основной реализации.

Реализованы:

- обработка 512-битных блоков;
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
- 64-битное представление длины сообщения;
- incremental update.

Поддерживаются методы:

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

Используется Keccak sponge construction.

Реализованы:

- состояние 1600 бит;
- rate 1088 бит;
- capacity 512 бит;
- Keccak-f[1600];
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

SHA-256 и SHA3-256 формируют результат длиной:

```text
256 бит
```

Для идеализированной 256-битной криптографической хеш-функции ожидаемый уровень стойкости составляет:

```text
Preimage resistance:          около 2^256
Second-preimage resistance:   около 2^256
Collision resistance:         около 2^128
```

Коллизионная стойкость ограничена birthday bound.

SHA-256 относится к семейству SHA-2 и использует конструкцию Merkle-Damgård.

SHA3-256 основан на Keccak sponge construction и принципиально отличается внутренним устройством от SHA-256.

Для SHA3-256 используются:

```text
state    = 1600 бит
rate     = 1088 бит
capacity = 512 бит
digest   = 256 бит
```

Криптографический хеш предназначен для контроля целостности данных.

Сам по себе обычный SHA-256 или SHA3-256 не подтверждает, кто сформировал данные, поскольку для вычисления обычного хеша не требуется секрет.

Для проверки одновременно целостности и подлинности в Sprint 5 используется HMAC-SHA256.

---

# Команда dgst

Для вычисления хешей используется:

```text
cryptocore dgst
```

Поддерживаются алгоритмы:

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

Формат файла:

```text
HASH_VALUE  INPUT_FILE_PATH
```

---

# Потоковая обработка хешей

Файл открывается в бинарном режиме:

```python
rb
```

и читается блоками:

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

Полный файл не загружается в оперативную память.

---

# Known-Answer Tests SHA-256

Пустое сообщение:

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

Пустое сообщение:

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

Файлы SHA-256:

```text
SHA256ShortMsg.rsp
SHA256LongMsg.rsp
SHA256Monte.rsp
```

Файлы SHA3-256:

```text
SHA3_256ShortMsg.rsp
SHA3_256LongMsg.rsp
SHA3_256Monte.rsp
```

Short и Long vectors проверяются автоматически через:

```text
tests/test_nist_hash_vectors.py
```

Запуск:

```powershell
pytest .\tests\test_nist_hash_vectors.py -v -s
```

Проверяются:

```text
SHA-256 Short Message
SHA-256 Long Message
SHA3-256 Short Message
SHA3-256 Long Message
```

---

# NIST Monte Carlo

Для Monte Carlo используется отдельный скрипт:

```text
scripts/nist_hash_monte_test.py
```

Запуск:

```powershell
python .\scripts\nist_hash_monte_test.py
```

Проверяются официальные checkpoint-значения из:

```text
SHA256Monte.rsp
SHA3_256Monte.rsp
```

Monte Carlo запускается отдельно от обычного `pytest`, поскольку содержит значительно больше вычислений.

---

# Interoperability SHA-256

Проверка выполнялась с системной Linux-утилитой:

```bash
sha256sum plaintext.txt
```

Полученный SHA-256 CryptoCore совпадает с системным значением.

---

# Interoperability SHA3-256

SHA3-256 независимо проверялся через OpenSSL:

```bash
openssl dgst -sha3-256 plaintext.txt
```

Значение CryptoCore совпадает с OpenSSL.

Для среды, где доступна нужная SHA3-утилита, также может использоваться:

```bash
sha3sum -a 256 plaintext.txt
```

---

# Avalanche Effect

Тест:

```text
tests/test_hash_avalanche.py
```

В исходных данных изменяется один бит.

После этого сравниваются два 256-битных digest.

Проверяется количество отличающихся битов:

```text
100 < changed_bits < 156
```

Тестируется:

```text
SHA-256
SHA3-256
```

---

# Проверка больших данных Sprint 4

В проекте предусмотрены два уровня проверки.

## Реальный файл больше 1 GiB

Скрипт:

```text
scripts/hash_large_file_test.py
```

создаёт sparse-файл размером:

```text
1 073 741 825 байт
```

то есть больше 1 GiB.

Для файла вычисляются:

```text
SHA-256
SHA3-256
```

Результаты сравниваются с:

```python
hashlib.sha256()
hashlib.sha3_256()
```

Скрипт запускается отдельно:

```powershell
python .\scripts\hash_large_file_test.py
```

Он не включён в обычный `pytest`, поскольку самописные SHA-256 и особенно SHA3-256 существенно медленнее оптимизированных библиотечных реализаций.

## Проверка streaming >1 GiB

Автоматический тест:

```text
tests/test_large_hash_streaming.py
```

создаёт виртуальный поток размером:

```text
1 GiB + 1 байт
```

и проверяет, что `hash_stream()`:

- обрабатывает весь логический объём;
- не загружает данные целиком;
- вызывает `read()` блоками;
- использует `CHUNK_SIZE = 8192`.

Криптографическая корректность самих SHA-функций при этом независимо проверяется NIST vectors.

---

# Sprint 5 — HMAC-SHA256

Цель Sprint 5 — реализовать механизм проверки целостности и подлинности данных.

Добавлен:

```text
HMAC-SHA256
```

Основная реализация:

```text
src/cryptocore/mac/hmac.py
```

HMAC реализован самостоятельно.

В основной реализации стандартные:

```python
hmac
hashlib
```

не используются.

В качестве внутренней хеш-функции применяется собственная реализация SHA-256 из Sprint 4.

---

# Конструкция HMAC

Используется классическая конструкция:

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

HMAC-SHA256 предназначен для проверки одновременно:

- целостности данных;
- подлинности данных.

В отличие от обычного SHA-256, HMAC использует секретный ключ.

Если получатель владеет тем же секретным ключом, он может проверить:

- что содержимое сообщения не было изменено;
- что корректный MAC был создан стороной, обладающей секретным ключом.

HMAC:

- не шифрует данные;
- не обеспечивает конфиденциальность;
- не скрывает содержимое сообщения.

Безопасность HMAC зависит от:

- сохранения ключа в тайне;
- качества ключевого материала;
- стойкости используемой хеш-функции.

В CryptoCore используется:

```text
HMAC-SHA256
```

с собственной реализацией SHA-256.

Для проверки вычисленного и ожидаемого значения применяется:

```python
secrets.compare_digest()
```

Это предпочтительнее обычного посимвольного сравнения MAC-значений.

Секретный ключ не должен передаваться или храниться вместе с защищаемым сообщением и его HMAC.

---

# Обработка HMAC-ключа

HMAC поддерживает ключ произвольной длины.

Если ключ длиннее блока SHA-256:

```text
len(key) > 64
```

то сначала выполняется:

```text
key = SHA256(key)
```

Если ключ короче 64 байт, он дополняется нулевыми байтами:

```text
key = key || zero padding
```

до:

```text
64 байт
```

Если ключ имеет длину ровно 64 байта, дополнительное хеширование не выполняется.

---

# CLI HMAC

HMAC интегрирован в существующую команду:

```text
cryptocore dgst
```

Используется флаг:

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

Ключ передаётся как hexadecimal-строка.

---

# Генерация HMAC

Пример:

```powershell
cryptocore dgst --algorithm sha256 --hmac --key 00112233445566778899aabbccddeeff --input plaintext.txt
```

Формат вывода:

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

Формат файла:

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

Если значение совпадает:

```text
[OK] HMAC verification successful
```

Код возврата:

```text
0
```

Если значение не совпадает:

```text
[ERROR] HMAC verification failed
```

Код возврата:

```text
1
```

---

# Формат expected HMAC

Файл проверки может иметь стандартный формат:

```text
HMAC_VALUE  INPUT_FILE_PATH
```

При чтении CryptoCore использует первый whitespace-separated элемент как HMAC.

Имя файла после значения может игнорироваться.

---

# Потоковая обработка HMAC

Входной файл открывается в бинарном режиме:

```python
rb
```

и читается блоками:

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
HMACSHA256.update()
    |
    v
next chunk
    |
    v
HMAC digest
```

Весь файл не загружается в память.

---

# RFC 4231 Known-Answer Tests

Файл:

```text
tests/test_hmac_vectors.py
```

Реализованы обязательные:

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

В Test Case 4 используется бинарный ключ:

```text
0102030405060708090a0b0c0d0e0f10111213141516171819
```

и сообщение из 50 байтов:

```text
cd
```

Ожидаемый HMAC-SHA256:

```text
82558a389a443c0ea4cc819899f2083a85f0faa3e578f8077a2e3ff46729665b
```

---

# Проверка ключей разных размеров

Автоматически проверяются HMAC-ключи:

```text
16 байт
64 байта
100 байт
```

Это покрывает:

- ключ короче блока;
- ключ, равный размеру блока;
- ключ длиннее блока.

Для сравнения в тестах используется стандартная библиотека Python:

```python
hmac
hashlib.sha256
```

Она применяется только как эталон в тестах, а не в основной реализации CryptoCore.

---

# Empty Input HMAC

Проверяется вычисление HMAC для:

```python
b""
```

Результат сравнивается с эталонной реализацией Python.

---

# Tamper Detection — изменение файла

Тест:

1. создаёт HMAC исходного файла;
2. изменяет содержимое;
3. выполняет `--verify`;
4. ожидает ошибку.

Результат:

```text
[ERROR] HMAC verification failed
```

Код возврата:

```text
1
```

---

# Tamper Detection — неверный ключ

Тест:

1. создаёт HMAC одним ключом;
2. выполняет проверку другим ключом;
3. ожидает несовпадение.

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

есть отдельный тест, который запускает настоящий процесс:

```text
python -m cryptocore
```

через `subprocess`.

Проверяется:

```text
успех проверки -> return code 0
ошибка проверки -> return code != 0
```

То есть тестируется не только возврат `digest_main()`, но и фактический код завершения CLI-процесса.

---

# Проверка HMAC на реальном большом файле

Скрипт:

```text
scripts/hmac_large_file_test.py
```

создаёт бинарный файл размером:

```text
10 485 760 байт
```

или:

```text
10 MiB
```

Настоящий `HMACSHA256` CryptoCore вычисляет MAC для всего файла.

Полученное значение сравнивается с:

```python
hmac.new(
    key,
    data,
    hashlib.sha256
)
```

Для проверенного тестового файла были получены одинаковые значения:

```text
CryptoCore: d20bad94a922f94d99165e579e66f710efc20dc7429bf47cf0985e6303d69ea0
Reference:  d20bad94a922f94d99165e579e66f710efc20dc7429bf47cf0985e6303d69ea0
```

Результат:

```text
Large HMAC test: PASSED
```

---

# Проверка constant-memory HMAC

Дополнительно используется:

```text
scripts/hmac_huge_streaming_test.py
```

Тест передаёт через реальную функцию:

```python
hmac_stream()
```

виртуальный вход размером:

```text
21 474 836 603 байта
```

то есть более 20 GiB.

При этом максимальный размер одного чтения:

```text
8192 байт
```

Проверенный результат:

```text
Logical input size: 21,474,836,603 bytes
Processed: 21,474,836,603 bytes
Maximum read: 8192 bytes

Huge HMAC streaming test: PASSED
```

В этом тесте криптографическое ядро заменяется счётчиком, поскольку его задача — отдельно проверить свойство constant-memory streaming.

Правильность самого HMAC независимо подтверждается:

- RFC 4231;
- тестами разных ключей;
- пустым сообщением;
- сравнением с Python `hmac`;
- настоящим 10 MiB файлом.

---

# HMAC interoperability с OpenSSL

Для дополнительной независимой проверки можно сравнить CryptoCore с OpenSSL.

CryptoCore:

```powershell
cryptocore dgst --algorithm sha256 --hmac --key 00112233445566778899aabbccddeeff --input plaintext.txt
```

OpenSSL:

```powershell
openssl dgst -sha256 -mac HMAC -macopt hexkey:00112233445566778899aabbccddeeff plaintext.txt
```

Для одинакового ключа и одинаковых данных HMAC должны совпадать.

---

# AES-CMAC

AES-CMAC в Sprint 5 не реализован.

В техническом задании он относится к:

```text
Bonus / Could
```

и не является обязательной частью Sprint 5.

---

# Автоматические тесты

Основные тестовые файлы:

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
```

---

# Настройка pytest

В:

```text
pyproject.toml
```

указано:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
```

Поэтому команда:

```powershell
pytest -v
```

запускает только автоматические тесты из:

```text
tests/
```

Служебные скрипты:

```text
scripts/
```

не запускаются автоматически через pytest.

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
|   `-- test_sha3_256.py
|
|-- scripts/
|   |-- generate_nist_data.py
|   |-- hash_interop_test.py
|   |-- hash_large_file_test.py
|   |-- hmac_huge_streaming_test.py
|   |-- hmac_large_file_test.py
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

# Проверка проекта

Обычный набор автоматических тестов:

```powershell
pytest -v
```

Проверка AES/OpenSSL:

```powershell
python .\scripts\openssl_interop_test.py
```

NIST Monte Carlo:

```powershell
python .\scripts\nist_hash_monte_test.py
```

Реальный файл >1 GiB для SHA:

```powershell
python .\scripts\hash_large_file_test.py
```

Реальный HMAC на 10 MiB:

```powershell
python .\scripts\hmac_large_file_test.py
```

Constant-memory HMAC на логическом объёме >20 GiB:

```powershell
python .\scripts\hmac_huge_streaming_test.py
```

---

# Итоги Sprint 1

Реализованы:

- структура проекта;
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
- самостоятельная логика режимов;
- генерация IV;
- `--iv`;
- формат `<IV><ciphertext>`;
- двусторонняя interoperability с OpenSSL.

---

# Итоги Sprint 3

Реализованы:

- CSPRNG;
- `os.urandom()`;
- автоматическая генерация AES-ключа;
- генерация IV через CSPRNG;
- предупреждение о потенциально слабых ключах;
- тесты CSPRNG;
- подготовка NIST data;
- NIST STS.

---

# Итоги Sprint 4

Реализованы:

- SHA-256 с нуля;
- SHA3-256 с нуля;
- Keccak-f[1600];
- `dgst`;
- `--algorithm`;
- `--input`;
- `--output`;
- binary file I/O;
- lowercase hexadecimal output;
- chunked processing;
- Known-Answer Tests;
- empty input tests;
- официальные NIST Short Message vectors;
- официальные NIST Long Message vectors;
- NIST Monte Carlo;
- interoperability;
- avalanche effect;
- проверка реального файла >1 GiB;
- отдельная автоматическая проверка streaming >1 GiB;
- документация security properties.

---

# Итоги Sprint 5

Реализованы:

- HMAC-SHA256 с нуля;
- использование собственной SHA-256;
- RFC 2104 construction;
- обработка ключей произвольной длины;
- хеширование ключей больше 64 байт;
- zero padding коротких ключей;
- `--hmac`;
- обязательный hexadecimal `--key`;
- `--verify`;
- `--output`;
- формат `HMAC_VALUE INPUT_FILE_PATH`;
- безопасное сравнение через `compare_digest`;
- binary file I/O;
- chunked processing;
- RFC 4231 Test Cases 1–4;
- ключи 16, 64 и 100 байт;
- empty input;
- verify generated HMAC;
- tamper detection файла;
- tamper detection ключа;
- реальные CLI exit codes;
- HMAC настоящего 10 MiB файла;
- constant-memory streaming для логического входа более 20 GiB;
- документация конструкции и security properties.

AES-CMAC не реализован, поскольку является дополнительным Bonus/Could требованием.

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

