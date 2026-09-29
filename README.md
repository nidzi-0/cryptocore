# CryptoCore

CryptoCore — консольное приложение на Python для шифрования и расшифрования файлов с использованием алгоритма AES-128.

Проект разработан в рамках учебной работы по дисциплине, связанной с методами и средствами криптографической защиты информации.

В рамках проекта реализованы требования Sprint 1 и Sprint 2.

---

## Поддерживаемые режимы

CryptoCore поддерживает следующие режимы AES-128:

- ECB;
- CBC;
- CFB-128;
- OFB;
- CTR.

Для выполнения самого алгоритма AES используется библиотека PyCryptodome.

Логика режимов CBC, CFB, OFB и CTR реализована самостоятельно поверх AES-примитива.

---

## Требования

Для работы проекта требуется:

- Python 3.10 или новее;
- PyCryptodome;
- pytest;
- OpenSSL — для проверки совместимости.

---

## Установка

Клонировать репозиторий:

```powershell
git clone https://github.com/nidzi-0/cryptocore.git
cd cryptocore
```

Создать виртуальное окружение:

```powershell
python -m venv .venv
```

Активировать виртуальное окружение в Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Установить проект и зависимости:

```powershell
pip install -e .
pip install -r requirements.txt
```

После установки должна быть доступна команда:

```powershell
cryptocore --help
```

Также программу можно запускать как Python-модуль:

```powershell
python -m cryptocore --help
```

---

# Использование

Общий формат команды:

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

Для AES-128 используется ключ длиной 16 байт.

В hexadecimal-представлении это 32 символа.

Пример ключа:

```text
000102030405060708090a0b0c0d0e0f
```

---

# AES-128 ECB

ECB реализован в рамках Sprint 1.

Режим ECB не использует IV.

Для ECB используется PKCS#7 padding.

## Шифрование ECB

```powershell
cryptocore --algorithm aes --mode ecb --encrypt --key 000102030405060708090a0b0c0d0e0f --input plaintext.txt --output encrypted_ecb.bin
```

## Расшифрование ECB

```powershell
cryptocore --algorithm aes --mode ecb --decrypt --key 000102030405060708090a0b0c0d0e0f --input encrypted_ecb.bin --output decrypted_ecb.txt
```

---

# AES-128 CBC

CBC реализован в рамках Sprint 2.

При шифровании IV создаётся автоматически.

Для CBC используется PKCS#7 padding.

## Шифрование CBC

```powershell
cryptocore --algorithm aes --mode cbc --encrypt --key 000102030405060708090a0b0c0d0e0f --input plaintext.txt --output encrypted_cbc.bin
```

При шифровании программа:

1. генерирует случайный IV длиной 16 байт;
2. выполняет шифрование CBC;
3. добавляет IV в начало выходного файла.

Формат файла:

```text
<16-byte IV><ciphertext>
```

## Расшифрование CBC

```powershell
cryptocore --algorithm aes --mode cbc --decrypt --key 000102030405060708090a0b0c0d0e0f --input encrypted_cbc.bin --output decrypted_cbc.txt
```

Если параметр `--iv` не указан, CryptoCore автоматически считывает первые 16 байт файла как IV.

---

# AES-128 CFB-128

CFB реализован с размером сегмента 128 бит.

Padding в этом режиме не используется.

Размер ciphertext совпадает с размером исходных данных.

## Шифрование CFB

```powershell
cryptocore --algorithm aes --mode cfb --encrypt --key 000102030405060708090a0b0c0d0e0f --input plaintext.txt --output encrypted_cfb.bin
```

## Расшифрование CFB

```powershell
cryptocore --algorithm aes --mode cfb --decrypt --key 000102030405060708090a0b0c0d0e0f --input encrypted_cfb.bin --output decrypted_cfb.txt
```

---

# AES-128 OFB

OFB работает как потоковый режим.

Padding не используется.

## Шифрование OFB

```powershell
cryptocore --algorithm aes --mode ofb --encrypt --key 000102030405060708090a0b0c0d0e0f --input plaintext.txt --output encrypted_ofb.bin
```

## Расшифрование OFB

```powershell
cryptocore --algorithm aes --mode ofb --decrypt --key 000102030405060708090a0b0c0d0e0f --input encrypted_ofb.bin --output decrypted_ofb.txt
```

---

# AES-128 CTR

CTR использует 128-битное значение IV в качестве начального значения счётчика.

После обработки каждого блока счётчик увеличивается на единицу.

Padding не используется.

## Шифрование CTR

```powershell
cryptocore --algorithm aes --mode ctr --encrypt --key 000102030405060708090a0b0c0d0e0f --input plaintext.txt --output encrypted_ctr.bin
```

## Расшифрование CTR

```powershell
cryptocore --algorithm aes --mode ctr --decrypt --key 000102030405060708090a0b0c0d0e0f --input encrypted_ctr.bin --output decrypted_ctr.txt
```

---

# Работа с IV

Для режимов:

- CBC;
- CFB;
- OFB;
- CTR

используется IV длиной 16 байт.

При шифровании IV создаётся автоматически с помощью:

```python
os.urandom(16)
```

Пользователь не должен передавать `--iv` при шифровании.

Формат зашифрованного файла:

```text
<16-byte IV><ciphertext>
```

Первые 16 байт содержат IV.

Оставшиеся байты содержат ciphertext.

---

## Расшифрование без параметра --iv

Если файл был создан CryptoCore, параметр `--iv` указывать не требуется.

Например:

```powershell
cryptocore --algorithm aes --mode cbc --decrypt --key 000102030405060708090a0b0c0d0e0f --input encrypted_cbc.bin --output restored.txt
```

Программа сама извлекает IV из первых 16 байт.

---

## Явное указание IV

Параметр `--iv` используется при расшифровании ciphertext, созданного внешней программой, например OpenSSL.

Пример:

```powershell
cryptocore --algorithm aes --mode cbc --decrypt --key 000102030405060708090a0b0c0d0e0f --iv AABBCCDDEEFF00112233445566778899 --input openssl_cipher.bin --output restored.txt
```

В этом случае весь входной файл считается ciphertext.

IV берётся из параметра `--iv`.

---

## Ограничения параметра --iv

Параметр `--iv` не используется для ECB.

Передавать `--iv` при шифровании нельзя.

При шифровании CBC, CFB, OFB и CTR IV создаётся автоматически.

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

Это позволяет CFB, OFB и CTR корректно обрабатывать последний неполный блок без увеличения размера ciphertext.

---

# Работа с бинарными файлами

CryptoCore работает с файлами в бинарном режиме.

Программа может обрабатывать:

- текстовые файлы;
- изображения;
- архивы;
- исполняемые файлы;
- документы;
- произвольные бинарные данные.

Чтение выполняется в режиме:

```python
rb
```

Запись выполняется в режиме:

```python
wb
```

---

# Автоматические тесты

Для запуска всех тестов:

```powershell
pytest
```

Для подробного вывода:

```powershell
pytest -v
```

Тестами проверяются:

- PKCS#7 padding;
- AES-128 ECB;
- AES-128 CBC;
- AES-128 CFB-128;
- AES-128 OFB;
- AES-128 CTR;
- обработка IV;
- CLI;
- неправильные ключи;
- неправильные IV;
- бинарные данные;
- неполные блоки;
- известные тестовые векторы;
- round-trip;
- файловый формат;
- совместимость между режимами и основной программой.

---

# Round-trip

Round-trip проверяет следующий сценарий:

```text
original file
      |
      v
   encrypt
      |
      v
 ciphertext
      |
      v
   decrypt
      |
      v
 restored file
```

После расшифрования исходный и восстановленный файлы должны полностью совпадать побайтово.

Сценарий находится в:

```text
scripts/round_trip_test.py
```

Запуск:

```powershell
python scripts/round_trip_test.py
```

---

# Совместимость с OpenSSL

Для проверки совместимости CryptoCore с OpenSSL используется общий сценарий:

```text
scripts/openssl_interop_test.py
```

Он используется для проверки Sprint 1 и Sprint 2.

---

## Установка и запуск OpenSSL

Проверить наличие OpenSSL:

```powershell
openssl version
```

Если OpenSSL установлен по пути:

```text
C:\Program Files\OpenSSL-Win64\bin
```

его можно добавить в PATH текущего PowerShell:

```powershell
$env:Path += ";C:\Program Files\OpenSSL-Win64\bin"
```

После этого:

```powershell
openssl version
```

Пример корректного результата:

```text
OpenSSL 4.0.2
```

---

# Общая проверка OpenSSL

Запуск:

```powershell
python scripts/openssl_interop_test.py
```

Сценарий проверяет следующие режимы AES-128:

- ECB;
- CBC;
- CFB-128;
- OFB;
- CTR.

Для каждого режима выполняются проверки в обоих направлениях:

```text
CryptoCore -> OpenSSL
OpenSSL -> CryptoCore
```

Для CBC, CFB, OFB и CTR используется IV длиной 16 байт.

ECB не использует IV.

---

# TEST-3 Sprint 1 — OpenSSL ECB interop

Требование TEST-3 Sprint 1 проверяет совместимость ciphertext CryptoCore с OpenSSL для AES-128-ECB.

Проверка выполняется внутри общего сценария:

```powershell
python scripts/openssl_interop_test.py
```

Отдельный сценарий для ECB не используется.

---

## Как выполняется TEST-3 Sprint 1

Одни и те же входные данные шифруются двумя способами:

1. CryptoCore с использованием AES-128-ECB;
2. OpenSSL с использованием `openssl enc -aes-128-ecb`.

После этого два ciphertext сравниваются побайтово.

Схема проверки:

```text
                    plaintext
                    /       \
                   /         \
                  v           v
           CryptoCore      OpenSSL
               ECB            ECB
                  \           /
                   \         /
                    v       v
                 ciphertext
                     |
                     v
              byte-by-byte
                comparison
```

ECB не использует IV.

---

## Padding при проверке ECB

CryptoCore использует PKCS#7 padding.

При вызове OpenSSL параметр:

```text
-nopad
```

не используется.

Поэтому OpenSSL применяет стандартное дополнение, совместимое с PKCS#7.

Это позволяет непосредственно сравнивать ciphertext CryptoCore и OpenSSL.

---

# Пример OpenSSL ECB

## Шифрование через CryptoCore

```powershell
cryptocore --algorithm aes --mode ecb --encrypt --key 000102030405060708090a0b0c0d0e0f --input plaintext.txt --output cryptocore_ecb.bin
```

## Шифрование тех же данных через OpenSSL

```powershell
openssl enc -aes-128-ecb -e -K 000102030405060708090a0b0c0d0e0f -nosalt -in plaintext.txt -out openssl_ecb.bin
```

Обратите внимание:

- `-aes-128-ecb` — режим AES-128 ECB;
- `-e` — операция шифрования;
- `-K` — ключ AES в hex;
- `-nosalt` — отключает добавление служебного salt-заголовка;
- IV не передаётся, поскольку ECB его не использует;
- `-nopad` не указывается, поэтому используется padding.

После выполнения команд файлы:

```text
cryptocore_ecb.bin
openssl_ecb.bin
```

должны полностью совпадать побайтово.

---

## Автоматическая проверка ciphertext ECB

В `openssl_interop_test.py` отдельно выполняется сравнение:

```text
CryptoCore ciphertext
        ==
OpenSSL ciphertext
```

При успешной проверке вывод содержит:

```text
[SPRINT 1 TEST-3 / ECB CIPHERTEXT]

CryptoCore ciphertext: ...
OpenSSL ciphertext:   ...

PASS: ciphertext CryptoCore ECB совпадает с ciphertext OpenSSL ECB
```

Таким образом выполняется требование TEST-3 Sprint 1.

---

# Проверка ECB: CryptoCore -> OpenSSL

Кроме прямого сравнения ciphertext, общий interop-тест проверяет возможность расшифровать результат CryptoCore средствами OpenSSL.

Схема:

```text
plaintext
    |
    v
CryptoCore ECB encrypt
    |
    v
ciphertext
    |
    v
OpenSSL ECB decrypt
    |
    v
restored plaintext
```

Результат должен полностью совпадать с исходными данными.

---

# Проверка ECB: OpenSSL -> CryptoCore

Проверяется и обратное направление:

```text
plaintext
    |
    v
OpenSSL ECB encrypt
    |
    v
ciphertext
    |
    v
CryptoCore ECB decrypt
    |
    v
restored plaintext
```

ECB при этом не требует IV.

---

# Проверка CBC, CFB, OFB и CTR через OpenSSL

Для режимов:

```text
CBC
CFB
OFB
CTR
```

используется IV длиной 16 байт.

---

## CryptoCore -> OpenSSL

CryptoCore сохраняет файл в формате:

```text
<16-byte IV><ciphertext>
```

Перед передачей данных OpenSSL общий тест:

1. извлекает первые 16 байт;
2. использует их как IV;
3. передаёт OpenSSL только ciphertext.

Пример команды для CBC:

```powershell
openssl enc -aes-128-cbc -d -K 000102030405060708090a0b0c0d0e0f -iv AABBCCDDEEFF00112233445566778899 -in ciphertext.bin -out restored.txt
```

---

## OpenSSL -> CryptoCore

OpenSSL создаёт ciphertext без заголовка CryptoCore.

Поэтому при расшифровании IV передаётся явно через параметр:

```text
--iv
```

Пример:

```powershell
cryptocore --algorithm aes --mode cbc --decrypt --key 000102030405060708090a0b0c0d0e0f --iv AABBCCDDEEFF00112233445566778899 --input openssl_cipher.bin --output restored.txt
```

---

# Результат OpenSSL interoperability test

В общем сценарии выполняются:

```text
ECB:
    CryptoCore -> OpenSSL
    OpenSSL -> CryptoCore

CBC:
    CryptoCore -> OpenSSL
    OpenSSL -> CryptoCore

CFB:
    CryptoCore -> OpenSSL
    OpenSSL -> CryptoCore

OFB:
    CryptoCore -> OpenSSL
    OpenSSL -> CryptoCore

CTR:
    CryptoCore -> OpenSSL
    OpenSSL -> CryptoCore

Sprint 1 TEST-3:
    CryptoCore ECB ciphertext
        ==
    OpenSSL ECB ciphertext
```

Всего выполняется 11 проверок.

При успешной работе:

```text
Result: 11/11 checks passed
OpenSSL interoperability: PASSED
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
|       |-- file_io.py
|       |-- padding.py
|       |-- iv.py
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

Отдельного файла:

```text
openssl_ecb_verify.py
```

в проекте нет.

Проверка ECB выполняется внутри:

```text
scripts/openssl_interop_test.py
```

---

# Реализация режимов

## ECB

ECB обрабатывает каждый блок независимо.

Используется PKCS#7 padding.

IV не используется.

---

## CBC

Для первого блока используется IV.

Перед шифрованием каждый блок открытого текста объединяется XOR с предыдущим ciphertext-блоком.

Для первого блока вместо предыдущего ciphertext используется IV.

Используется PKCS#7 padding.

---

## CFB-128

Для формирования потока AES шифрует IV или предыдущий ciphertext-блок.

Полученный результат объединяется с исходными данными операцией XOR.

Padding не используется.

---

## OFB

Поток формируется последовательным шифрованием предыдущего выходного блока AES.

Первым значением является IV.

Полученный поток объединяется с данными операцией XOR.

Padding не используется.

---

## CTR

IV используется как начальное значение 128-битного счётчика.

Для каждого блока:

1. текущее значение счётчика шифруется AES;
2. результат объединяется с данными через XOR;
3. счётчик увеличивается на единицу.

Padding не используется.

---

# Безопасность IV

Для каждого нового шифрования в режимах:

- CBC;
- CFB;
- OFB;
- CTR

генерируется новый случайный IV:

```python
os.urandom(16)
```

IV не является секретным.

Поэтому он сохраняется непосредственно перед ciphertext.

Формат:

```text
IV + ciphertext
```

AES-ключ в зашифрованный файл не записывается.

---

# Проверка проекта перед сдачей

Запустить все pytest-тесты:

```powershell
pytest
```

Запустить round-trip:

```powershell
python scripts/round_trip_test.py
```

Добавить OpenSSL в PATH при необходимости:

```powershell
$env:Path += ";C:\Program Files\OpenSSL-Win64\bin"
```

Проверить OpenSSL:

```powershell
openssl version
```

Запустить полную проверку совместимости:

```powershell
python scripts/openssl_interop_test.py
```

Ожидаемый итог:

```text
Result: 11/11 checks passed
OpenSSL interoperability: PASSED
```

После этого можно проверить состояние Git:

```powershell
git status
```

Для полностью сохранённого проекта ожидается:

```text
nothing to commit, working tree clean
```