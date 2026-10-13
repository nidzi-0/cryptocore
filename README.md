# CryptoCore

CryptoCore — консольное приложение на Python для шифрования и расшифрования файлов с использованием алгоритма AES-128.

Проект разработан в рамках учебной работы по дисциплине, связанной с методами и средствами криптографической защиты информации.

В проекте реализованы требования Sprint 1, Sprint 2 и Sprint 3.

---

# Поддерживаемые режимы

CryptoCore поддерживает следующие режимы AES-128:

- ECB;
- CBC;
- CFB-128;
- OFB;
- CTR.

Для выполнения самого алгоритма AES используется библиотека PyCryptodome.

Логика режимов ECB, CBC, CFB, OFB и CTR реализована на уровне проекта поверх AES-примитива.

---

# Требования

Для работы проекта требуется:

- Python 3.10 или новее;
- PyCryptodome;
- pytest;
- OpenSSL — для проверки совместимости;
- NIST Statistical Test Suite — для отдельной статистической проверки CSPRNG.

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

Программу также можно запускать как Python-модуль:

```powershell
python -m cryptocore --help
```

---

# Общий формат команды

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

Для AES-128 используется ключ длиной 16 байт.

В шестнадцатеричном представлении это 32 символа.

Пример ключа:

```text
000102030405060708090a0b0c0d0e0f
```

Начиная со Sprint 3 параметр `--key` является необязательным при шифровании.

При расшифровании `--key` остаётся обязательным.

---

# Автоматическая генерация AES-ключа

Если при шифровании параметр `--key` не указан, CryptoCore автоматически создаёт криптографически стойкий случайный ключ длиной 16 байт.

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
- выводится в stdout в hexadecimal-формате;
- выводится сразу после генерации;
- не записывается в зашифрованный файл.

Пользователь должен сохранить этот ключ самостоятельно.

Для последующего расшифрования необходимо передать его через `--key`.

Пример:

```powershell
cryptocore --algorithm aes --mode ctr --decrypt --key 1a2b3c4d5e6f7890fedcba9876543210 --input ciphertext.bin --output decrypted.txt
```

---

# Пользовательский AES-ключ

Если пользователь явно указывает `--key`, CryptoCore использует переданный ключ.

Пример:

```powershell
cryptocore --algorithm aes --mode cbc --encrypt --key 000102030405060708090a0b0c0d0e0f --input plaintext.txt --output ciphertext.bin
```

Ключ должен:

- быть представлен hexadecimal-строкой;
- содержать ровно 16 байт;
- состоять из 32 hexadecimal-символов.

---

# Предупреждение о слабых ключах

CryptoCore выполняет базовую проверку пользовательского AES-ключа.

Потенциально слабыми считаются, например:

- полностью нулевой ключ;
- ключ из одного повторяющегося байта;
- последовательность байтов от `00` до `0F`;
- обратная последовательность байтов.

Пример слабого ключа:

```text
00000000000000000000000000000000
```

При обнаружении такого значения программа выводит предупреждение в `stderr`.

Пример:

```text
[WARNING] Обнаружен потенциально слабый AES-ключ: ключ состоит из одного повторяющегося байта.
```

Операция при этом не блокируется.

---

# CSPRNG

Начиная со Sprint 3 в проекте используется отдельный модуль криптографически стойкой генерации случайных данных:

```text
src/cryptocore/csprng.py
```

Основная функция:

```python
generate_random_bytes(num_bytes: int) -> bytes
```

Для получения случайных данных используется:

```python
os.urandom()
```

Стандартный модуль Python:

```python
random
```

для генерации криптографических ключей и IV не используется.

CSPRNG применяется для:

- автоматической генерации AES-128 ключей;
- генерации IV для CBC;
- генерации IV для CFB;
- генерации IV для OFB;
- генерации IV для CTR;
- подготовки случайных данных для NIST STS.

Модуль также проверяет корректность запрашиваемого размера и обрабатывает ошибки системного источника случайности.

---

# AES-128 ECB

ECB не использует IV.

Для ECB применяется PKCS#7 padding.

## Шифрование с пользовательским ключом

```powershell
cryptocore --algorithm aes --mode ecb --encrypt --key 000102030405060708090a0b0c0d0e0f --input plaintext.txt --output encrypted_ecb.bin
```

## Шифрование с автоматически созданным ключом

```powershell
cryptocore --algorithm aes --mode ecb --encrypt --input plaintext.txt --output encrypted_ecb.bin
```

## Расшифрование

```powershell
cryptocore --algorithm aes --mode ecb --decrypt --key 000102030405060708090a0b0c0d0e0f --input encrypted_ecb.bin --output decrypted_ecb.txt
```

---

# AES-128 CBC

CBC использует IV длиной 16 байт.

При шифровании IV создаётся автоматически через общий CSPRNG.

Для CBC используется PKCS#7 padding.

## Шифрование

```powershell
cryptocore --algorithm aes --mode cbc --encrypt --key 000102030405060708090a0b0c0d0e0f --input plaintext.txt --output encrypted_cbc.bin
```

Либо без пользовательского ключа:

```powershell
cryptocore --algorithm aes --mode cbc --encrypt --input plaintext.txt --output encrypted_cbc.bin
```

Формат выходного файла:

```text
<16-byte IV><ciphertext>
```

## Расшифрование

```powershell
cryptocore --algorithm aes --mode cbc --decrypt --key 000102030405060708090a0b0c0d0e0f --input encrypted_cbc.bin --output decrypted_cbc.txt
```

Если `--iv` не указан, CryptoCore автоматически считывает первые 16 байт входного файла как IV.

---

# AES-128 CFB-128

CFB реализован с размером сегмента 128 бит.

Padding не используется.

Размер ciphertext совпадает с размером исходных данных.

## Шифрование

```powershell
cryptocore --algorithm aes --mode cfb --encrypt --key 000102030405060708090a0b0c0d0e0f --input plaintext.txt --output encrypted_cfb.bin
```

## Расшифрование

```powershell
cryptocore --algorithm aes --mode cfb --decrypt --key 000102030405060708090a0b0c0d0e0f --input encrypted_cfb.bin --output decrypted_cfb.txt
```

---

# AES-128 OFB

OFB работает как потоковый режим.

Padding не используется.

## Шифрование

```powershell
cryptocore --algorithm aes --mode ofb --encrypt --key 000102030405060708090a0b0c0d0e0f --input plaintext.txt --output encrypted_ofb.bin
```

## Расшифрование

```powershell
cryptocore --algorithm aes --mode ofb --decrypt --key 000102030405060708090a0b0c0d0e0f --input encrypted_ofb.bin --output decrypted_ofb.txt
```

---

# AES-128 CTR

В CTR IV используется как начальное значение 128-битного счётчика.

После обработки каждого блока счётчик увеличивается на единицу.

Padding не используется.

## Шифрование

```powershell
cryptocore --algorithm aes --mode ctr --encrypt --key 000102030405060708090a0b0c0d0e0f --input plaintext.txt --output encrypted_ctr.bin
```

## Расшифрование

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

ECB IV не использует.

Начиная со Sprint 3 генерация IV выполняется через общий CSPRNG:

```python
generate_random_bytes(16)
```

который внутри использует:

```python
os.urandom()
```

При шифровании пользователь не должен передавать `--iv`.

IV создаётся автоматически.

Формат зашифрованного файла:

```text
<16-byte IV><ciphertext>
```

Первые 16 байт содержат IV.

Все оставшиеся байты содержат ciphertext.

---

# Расшифрование без --iv

Если файл был создан CryptoCore, параметр `--iv` указывать не требуется.

Например:

```powershell
cryptocore --algorithm aes --mode cbc --decrypt --key 000102030405060708090a0b0c0d0e0f --input encrypted_cbc.bin --output restored.txt
```

CryptoCore автоматически:

1. читает первые 16 байт;
2. использует их как IV;
3. оставшуюся часть файла считает ciphertext;
4. выполняет расшифрование.

---

# Явное указание IV

Параметр `--iv` используется при расшифровании ciphertext, полученного из внешней программы, например OpenSSL.

Пример:

```powershell
cryptocore --algorithm aes --mode cbc --decrypt --key 000102030405060708090a0b0c0d0e0f --iv AABBCCDDEEFF00112233445566778899 --input openssl_cipher.bin --output restored.txt
```

В этом случае весь входной файл считается ciphertext.

IV берётся из параметра `--iv`.

Передавать `--iv` при шифровании запрещено.

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

CFB, OFB и CTR корректно обрабатывают последний неполный блок без изменения размера исходных данных.

---

# Работа с бинарными файлами

CryptoCore работает с файлами в бинарном режиме.

Чтение выполняется через:

```python
rb
```

Запись выполняется через:

```python
wb
```

Поэтому CryptoCore может обрабатывать:

- текстовые файлы;
- изображения;
- архивы;
- документы;
- исполняемые файлы;
- произвольные бинарные данные.

---

# Автоматические тесты

Для запуска всех тестов:

```powershell
pytest
```

Подробный вывод:

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
- CLI;
- ключи AES;
- автоматическая генерация ключа;
- обязательность ключа при расшифровании;
- CSPRNG;
- генерация IV;
- формат IV + ciphertext;
- обработка бинарных файлов;
- неполные блоки;
- round-trip;
- известные тестовые векторы;
- обнаружение слабых ключей;
- уникальность случайных значений;
- базовое распределение случайных битов;
- подготовка данных для NIST STS.

---

# Тест CSPRNG

Основные тесты находятся в:

```text
tests/test_csprng.py
```

Проверяется:

- тип результата;
- требуемая длина результата;
- генерация разных значений;
- обработка неправильного размера;
- обработка ошибки `os.urandom`;
- уникальность 1000 случайных 16-байтовых значений;
- базовое распределение единичных битов.

---

# Тест 1000 случайных ключей

Для проверки уникальности вызывается:

```python
generate_random_bytes(16)
```

1000 раз.

Все полученные значения помещаются в множество.

Ожидается:

```text
1000 generated keys
1000 unique keys
```

Появление повторяющегося 128-битного значения в таком тесте рассматривается как критическая ошибка.

---

# Базовая статистическая проверка

В проекте также выполняется простая проверка Hamming weight.

Для набора случайных данных подсчитывается количество единичных битов.

Для качественного случайного распределения доля единичных битов должна находиться около 50%.

В автоматическом тесте используется допустимый диапазон:

```text
45% - 55%
```

Данная проверка не является заменой полноценного статистического набора NIST STS.

---

# Round-trip

Основной принцип проверки:

```text
original
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
restored
```

Файлы `original` и `restored` должны полностью совпадать побайтово.

Дополнительный сценарий находится в:

```text
scripts/round_trip_test.py
```

Запуск:

```powershell
python scripts/round_trip_test.py
```

---

# Round-trip с автоматически созданным ключом

Sprint 3 позволяет выполнить шифрование без `--key`.

Пример:

```powershell
cryptocore --algorithm aes --mode ctr --encrypt --input plaintext.txt --output sprint3_test.bin
```

Программа выведет:

```text
[INFO] Generated random key: ...
```

Выведенный ключ необходимо использовать для расшифрования:

```powershell
cryptocore --algorithm aes --mode ctr --decrypt --key <GENERATED_KEY> --input sprint3_test.bin --output restored.txt
```

Файл `restored.txt` должен побайтово совпадать с `plaintext.txt`.

---

# Совместимость с OpenSSL

Для проверки совместимости CryptoCore с OpenSSL используется общий сценарий:

```text
scripts/openssl_interop_test.py
```

Проверка охватывает:

- ECB;
- CBC;
- CFB-128;
- OFB;
- CTR.

---

# Установка и запуск OpenSSL

Проверить наличие OpenSSL:

```powershell
openssl version
```

Если OpenSSL установлен по пути:

```text
C:\Program Files\OpenSSL-Win64\bin
```

его можно временно добавить в PATH текущего PowerShell:

```powershell
$env:Path += ";C:\Program Files\OpenSSL-Win64\bin"
```

Проверить:

```powershell
openssl version
```

---

# Общая проверка OpenSSL

Запуск:

```powershell
python scripts/openssl_interop_test.py
```

Для каждого режима выполняются проверки в обоих направлениях:

```text
CryptoCore -> OpenSSL
OpenSSL -> CryptoCore
```

Для CBC, CFB, OFB и CTR используется IV.

ECB IV не использует.

Кроме того, отдельно выполняется побайтовое сравнение ciphertext ECB для выполнения TEST-3 Sprint 1.

Всего:

```text
5 режимов × 2 направления = 10 проверок
```

и дополнительная проверка:

```text
CryptoCore ECB ciphertext == OpenSSL ECB ciphertext
```

Итого:

```text
11 проверок
```

Ожидаемый успешный результат:

```text
Result: 11/11 checks passed
OpenSSL interoperability: PASSED
```

---

# TEST-3 Sprint 1 — OpenSSL ECB

Для ECB выполняется отдельное сравнение ciphertext.

Одни и те же данные шифруются:

1. средствами CryptoCore;
2. средствами OpenSSL.

Команда OpenSSL:

```powershell
openssl enc -aes-128-ecb -e -K 000102030405060708090a0b0c0d0e0f -nosalt -in plaintext.txt -out openssl_ecb.bin
```

ECB не использует IV.

Параметр:

```text
-nopad
```

не используется, поскольку CryptoCore применяет PKCS#7 padding, а стандартное дополнение OpenSSL совместимо с ним.

Результаты CryptoCore и OpenSSL сравниваются побайтово.

---

# CryptoCore -> OpenSSL

Для CBC, CFB, OFB и CTR CryptoCore формирует файл:

```text
<16-byte IV><ciphertext>
```

Перед передачей в OpenSSL необходимо:

1. извлечь первые 16 байт;
2. использовать их как IV;
3. передать OpenSSL только ciphertext.

Пример для CBC:

```powershell
openssl enc -aes-128-cbc -d -K 000102030405060708090a0b0c0d0e0f -iv AABBCCDDEEFF00112233445566778899 -in ciphertext.bin -out restored.txt
```

---

# OpenSSL -> CryptoCore

OpenSSL формирует только ciphertext.

Поэтому IV необходимо передать CryptoCore через `--iv`.

Пример:

```powershell
cryptocore --algorithm aes --mode cbc --decrypt --key 000102030405060708090a0b0c0d0e0f --iv AABBCCDDEEFF00112233445566778899 --input openssl_cipher.bin --output restored.txt
```

---

# Подготовка данных для NIST STS

Для подготовки случайных данных для NIST Statistical Test Suite используется:

```text
scripts/generate_nist_data.py
```

Основная логика находится в:

```text
src/cryptocore/nist_data.py
```

Запуск:

```powershell
python scripts/generate_nist_data.py
```

По умолчанию создаётся файл:

```text
nist_test_data.bin
```

размером:

```text
10 000 000 байт
```

то есть примерно 10 MB.

Для генерации всех байтов используется:

```python
generate_random_bytes(...)
```

из общего CSPRNG-модуля CryptoCore.

Файл `nist_test_data.bin` добавлен в `.gitignore` и не должен храниться в Git-репозитории.

---

# NIST Statistical Test Suite

NIST STS используется для отдельной статистической проверки выхода CSPRNG.

Для подготовки данных необходимо выполнить:

```powershell
python scripts/generate_nist_data.py
```

После этого полученный файл:

```text
nist_test_data.bin
```

может быть передан в NIST Statistical Test Suite.

Пример запуска NIST STS:

```bash
./assess 1000000
```

Рекомендуется:

1. выбрать пользовательский входной файл;
2. указать `nist_test_data.bin`;
3. выбрать все 15 статистических тестов;
4. использовать бинарный режим;
5. проанализировать итоговый отчёт:

```text
experiments/AlgorithmTesting/finalAnalysisReport.txt
```

Основной уровень значимости:

```text
p-value >= 0.01
```

Единичные статистические отклонения возможны, однако массовое количество провалов может указывать на проблему с генератором.

## Статус NIST STS

Проект содержит подготовку данных и инструкцию для запуска NIST STS.

Фактический результат полного запуска NIST STS в данном README не заявляется как успешно пройденный до выполнения отдельного статистического тестирования.

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
|       |-- csprng.py
|       |-- nist_data.py
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
|   `-- test_nist_data.py
|
|-- scripts/
|   |-- round_trip_test.py
|   |-- openssl_interop_test.py
|   `-- generate_nist_data.py
|
|-- plaintext.txt
|-- pyproject.toml
|-- requirements.txt
|-- README.md
`-- .gitignore
```

---

# Реализация режимов AES

## ECB

Каждый блок обрабатывается независимо.

Используется PKCS#7 padding.

IV не используется.

---

## CBC

Для первого блока используется IV.

Каждый plaintext-блок объединяется операцией XOR с предыдущим ciphertext-блоком.

Для первого блока используется IV.

Используется PKCS#7 padding.

---

## CFB-128

AES шифрует IV или предыдущий ciphertext-блок.

Полученный блок используется как keystream и объединяется с исходными данными через XOR.

Размер сегмента составляет 128 бит.

Padding не используется.

---

## OFB

AES последовательно шифрует предыдущий выходной блок.

Первым входным значением является IV.

Полученный поток объединяется с исходными данными через XOR.

Padding не используется.

---

## CTR

IV используется как начальное значение 128-битного счётчика.

Для каждого блока:

1. значение счётчика шифруется AES;
2. результат используется как keystream;
3. keystream объединяется с данными через XOR;
4. счётчик увеличивается на единицу.

Padding не используется.

---

# Безопасность IV

Для каждого нового шифрования в режимах:

- CBC;
- CFB;
- OFB;
- CTR

создаётся новый случайный IV длиной 16 байт.

Начиная со Sprint 3 он генерируется через:

```python
generate_random_bytes(16)
```

IV не является секретным и поэтому сохраняется непосредственно перед ciphertext:

```text
IV + ciphertext
```

AES-ключ в зашифрованный файл не записывается.

---

# Проверка проекта перед сдачей

Запустить все автоматические тесты:

```powershell
pytest -v
```

Запустить round-trip:

```powershell
python scripts/round_trip_test.py
```

Проверить OpenSSL:

```powershell
$env:Path += ";C:\Program Files\OpenSSL-Win64\bin"
openssl version
```

Запустить interoperability-тест:

```powershell
python scripts/openssl_interop_test.py
```

Ожидаемый результат:

```text
Result: 11/11 checks passed
OpenSSL interoperability: PASSED
```

Проверить генерацию данных NIST:

```powershell
python scripts/generate_nist_data.py
```

Проверить состояние Git:

```powershell
git status
```

Для полностью сохранённого проекта ожидается:

```text
nothing to commit, working tree clean
```

---

# Итоги Sprint 1

В Sprint 1 реализованы:

- базовая структура проекта;
- CLI;
- AES-128 ECB;
- PKCS#7 padding;
- бинарный File I/O;
- round-trip;
- проверка совместимости ECB с OpenSSL.

---

# Итоги Sprint 2

В Sprint 2 реализованы:

- AES-128 CBC;
- AES-128 CFB-128;
- AES-128 OFB;
- AES-128 CTR;
- ручная логика режимов поверх AES-примитива;
- автоматическая генерация IV;
- формат `<IV><ciphertext>`;
- поддержка явного `--iv` при расшифровании;
- interoperability с OpenSSL в обоих направлениях.

---

# Итоги Sprint 3

В Sprint 3 реализованы:

- отдельный CSPRNG-модуль;
- `generate_random_bytes(num_bytes)`;
- использование `os.urandom()`;
- автоматическая генерация AES-128 ключа;
- вывод автоматически созданного ключа в stdout;
- обязательный `--key` при расшифровании;
- сохранение возможности передать пользовательский ключ;
- предупреждение о потенциально слабых пользовательских ключах;
- перевод генерации IV на единый CSPRNG;
- тест 1000 уникальных случайных значений;
- базовый тест распределения единичных битов;
- обработка ошибок CSPRNG;
- подготовка 10 MB случайных данных;
- сценарий подготовки данных для NIST STS;
- инструкция по запуску NIST STS.

Фактический полный прогон NIST STS должен выполняться отдельно перед окончательным подтверждением TEST-3 Sprint 3.