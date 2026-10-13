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

Для реализации базового AES-примитива используется библиотека PyCryptodome.

В режимах CBC, CFB, OFB и CTR логика режима реализована в проекте поверх AES-128 ECB.

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

Пример:

```text
000102030405060708090a0b0c0d0e0f
```

Начиная со Sprint 3 параметр `--key` является необязательным при шифровании.

При расшифровании параметр `--key` остаётся обязательным.

---

# Автоматическая генерация AES-ключа

Если при шифровании параметр `--key` не указан, CryptoCore автоматически создаёт криптографически стойкий случайный ключ AES-128 длиной 16 байт.

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
- выводится сразу после генерации;
- не записывается в зашифрованный файл.

Пользователь должен сохранить сгенерированный ключ самостоятельно.

Для последующего расшифрования необходимо передать его через параметр `--key`.

Пример:

```powershell
cryptocore --algorithm aes --mode ctr --decrypt --key 1a2b3c4d5e6f7890fedcba9876543210 --input ciphertext.bin --output decrypted.txt
```

---

# Пользовательский AES-ключ

Если пользователь явно указывает параметр `--key`, CryptoCore использует переданный ключ.

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

Потенциально слабыми считаются:

- ключи из одного повторяющегося байта;
- полностью нулевой ключ;
- последовательность байтов от `00` до `0F`;
- обратная последовательность байтов от `0F` до `00`.

Пример:

```text
00000000000000000000000000000000
```

При обнаружении такого значения CryptoCore выводит предупреждение в `stderr`.

Например:

```text
[WARNING] Обнаружен потенциально слабый AES-ключ: ключ состоит из одного повторяющегося байта.
```

Операция при этом не прерывается.

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

Для генерации используется системный источник случайности:

```python
os.urandom()
```

Стандартный псевдослучайный генератор:

```python
random
```

для формирования криптографических ключей и IV не используется.

CSPRNG применяется для:

- автоматической генерации AES-128 ключей;
- генерации IV для CBC;
- генерации IV для CFB;
- генерации IV для OFB;
- генерации IV для CTR;
- подготовки случайных данных для NIST STS.

Функция проверяет корректность запрашиваемого количества байт.

При ошибке системного источника случайности возникает понятная ошибка:

```text
RuntimeError
```

---

# AES-128 ECB

ECB обрабатывает каждый блок независимо.

IV не используется.

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

Каждый plaintext-блок объединяется операцией XOR с предыдущим ciphertext-блоком.

Для первого блока используется IV.

## Шифрование

```powershell
cryptocore --algorithm aes --mode cbc --encrypt --key 000102030405060708090a0b0c0d0e0f --input plaintext.txt --output encrypted_cbc.bin
```

Либо с автоматически созданным ключом:

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

AES используется для шифрования IV или предыдущего ciphertext-блока.

Полученный результат используется как keystream и объединяется с данными через XOR.

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

AES последовательно шифрует предыдущий выходной блок.

Первым входным значением является IV.

Полученный поток объединяется с исходными данными через XOR.

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

Для каждого блока:

1. текущее значение счётчика шифруется AES;
2. полученный результат используется как keystream;
3. keystream объединяется с данными через XOR;
4. счётчик увеличивается на единицу.

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

Оставшаяся часть файла содержит ciphertext.

AES-ключ в файл не записывается.

---

# Расшифрование без --iv

Если файл был создан CryptoCore, параметр `--iv` указывать не требуется.

Пример:

```powershell
cryptocore --algorithm aes --mode cbc --decrypt --key 000102030405060708090a0b0c0d0e0f --input encrypted_cbc.bin --output restored.txt
```

CryptoCore автоматически:

1. читает первые 16 байт;
2. использует их как IV;
3. оставшуюся часть файла рассматривает как ciphertext;
4. выполняет расшифрование.

---

# Явное указание IV

Параметр `--iv` используется при расшифровании ciphertext, созданного внешней программой, например OpenSSL.

Пример:

```powershell
cryptocore --algorithm aes --mode cbc --decrypt --key 000102030405060708090a0b0c0d0e0f --iv AABBCCDDEEFF00112233445566778899 --input openssl_cipher.bin --output restored.txt
```

В этом случае весь входной файл считается ciphertext.

IV берётся из параметра `--iv`.

Передавать `--iv` при шифровании запрещено.

Для ECB использование `--iv` также запрещено.

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

Поэтому программа может обрабатывать:

- текстовые файлы;
- изображения;
- архивы;
- документы;
- произвольные бинарные данные.

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

Автоматическими тестами проверяются:

- PKCS#7 padding;
- AES-128 ECB;
- AES-128 CBC;
- AES-128 CFB-128;
- AES-128 OFB;
- AES-128 CTR;
- CLI;
- проверка AES-128 ключей;
- необязательный ключ при шифровании;
- обязательный ключ при расшифровании;
- автоматическая генерация ключей;
- CSPRNG;
- генерация IV;
- использование общего CSPRNG для IV;
- формат `IV + ciphertext`;
- round-trip;
- работа с неполными блоками;
- слабые пользовательские ключи;
- уникальность случайных значений;
- базовое распределение случайных битов;
- подготовка файла для NIST STS.

---

# Тест CSPRNG

Основные тесты находятся в:

```text
tests/test_csprng.py
```

Проверяются:

- тип возвращаемого значения;
- требуемая длина;
- генерация различных значений;
- неправильный нулевой размер;
- отрицательный размер;
- нецелочисленный размер;
- ошибка системного источника `os.urandom()`;
- уникальность случайных значений;
- базовое распределение единичных битов.

---

# Тест 1000 случайных ключей

Для проверки уникальности функция:

```python
generate_random_bytes(16)
```

вызывается 1000 раз.

Полученные значения помещаются в множество.

Проверяется:

```text
Количество сгенерированных значений: 1000
Количество уникальных значений: 1000
```

Таким образом проверяется отсутствие повторов среди 1000 случайных 128-битных значений.

---

# Базовая статистическая проверка

В проекте выполняется базовая проверка доли единичных битов.

Для 1000 случайных 16-байтовых значений подсчитывается:

```text
количество единичных битов / общее количество битов
```

Допустимый диапазон теста:

```text
0.45 <= доля единичных битов <= 0.55
```

То есть доля единиц должна находиться примерно около 50%.

Данная проверка не заменяет полноценное статистическое тестирование NIST STS.

---

# Round-trip

Принцип проверки:

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

Sprint 3 позволяет выполнить шифрование без параметра `--key`.

Пример:

```powershell
cryptocore --algorithm aes --mode ctr --encrypt --input plaintext.txt --output sprint3_test.bin
```

Программа выводит:

```text
[INFO] Generated random key: ...
```

Полученный ключ необходимо использовать для расшифрования:

```powershell
cryptocore --algorithm aes --mode ctr --decrypt --key <GENERATED_KEY> --input sprint3_test.bin --output restored.txt
```

Файл:

```text
restored.txt
```

должен побайтово совпадать с исходным:

```text
plaintext.txt
```

---

# Совместимость с OpenSSL

Для проверки совместимости CryptoCore с OpenSSL используется:

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

его можно временно добавить в PATH:

```powershell
$env:Path += ";C:\Program Files\OpenSSL-Win64\bin"
```

После этого:

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

Отдельно выполняется побайтовое сравнение ciphertext AES-128 ECB.

Количество основных проверок:

```text
5 режимов × 2 направления = 10
```

Дополнительная проверка:

```text
CryptoCore ECB ciphertext == OpenSSL ECB ciphertext
```

Всего:

```text
11 проверок
```

При успешном прохождении ожидается:

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

Пример команды OpenSSL:

```powershell
openssl enc -aes-128-ecb -e -K 000102030405060708090a0b0c0d0e0f -nosalt -in plaintext.txt -out openssl_ecb.bin
```

ECB не использует IV.

Параметр:

```text
-nopad
```

не применяется, поскольку CryptoCore использует PKCS#7 padding.

Результаты CryptoCore и OpenSSL сравниваются побайтово.

---

# CryptoCore -> OpenSSL

Для CBC, CFB, OFB и CTR CryptoCore формирует:

```text
<16-byte IV><ciphertext>
```

Перед передачей данных OpenSSL необходимо:

1. извлечь первые 16 байт;
2. использовать их как IV;
3. передать OpenSSL оставшийся ciphertext.

Пример для CBC:

```powershell
openssl enc -aes-128-cbc -d -K 000102030405060708090a0b0c0d0e0f -iv AABBCCDDEEFF00112233445566778899 -in ciphertext.bin -out restored.txt
```

---

# OpenSSL -> CryptoCore

При формировании внешнего ciphertext OpenSSL IV передаётся CryptoCore явно.

Пример:

```powershell
cryptocore --algorithm aes --mode cbc --decrypt --key 000102030405060708090a0b0c0d0e0f --iv AABBCCDDEEFF00112233445566778899 --input openssl_cipher.bin --output restored.txt
```

---

# Подготовка данных для NIST STS

Для подготовки случайных данных используется:

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

По умолчанию создаётся:

```text
nist_test_data.bin
```

Размер:

```text
10 000 000 байт
```

Все данные формируются через общий CSPRNG проекта:

```python
generate_random_bytes(...)
```

Файл:

```text
nist_test_data.bin
```

добавлен в `.gitignore` и не хранится в Git-репозитории.

---

# NIST Statistical Test Suite

Для полноценной статистической проверки выхода CSPRNG использовалась:

```text
NIST Statistical Test Suite 2.1.2
```

Тестирование выполнялось в Ubuntu через WSL.

Был использован файл:

```text
data/nist_test_data.bin
```

сгенерированный CryptoCore через CSPRNG на основе:

```python
os.urandom()
```

Размер исходного файла:

```text
10 000 000 байт
```

то есть:

```text
80 000 000 бит
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

Объём:

```text
80 × 1 000 000 = 80 000 000 бит
```

Формат входного файла:

```text
Binary
```

Были выбраны все 15 статистических тестов.

Команда запуска:

```bash
./assess 1000000
```

---

# Выполненные тесты NIST STS

Выполнены все группы статистических тестов:

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

---

# Результаты NIST STS

Итоговый отчёт сформирован в:

```text
experiments/AlgorithmTesting/finalAnalysisReport.txt
```

Для выборки из 80 последовательностей NIST STS указал минимально допустимую пропорцию:

```text
76/80
```

Для Random Excursions и Random Excursions Variant из-за количества подходящих последовательностей использовалось 53 последовательности.

Минимально допустимая пропорция:

```text
50/53
```

Основные результаты:

```text
Frequency               80/80
BlockFrequency          79/80
CumulativeSums          80/80
CumulativeSums          80/80
Runs                    79/80
LongestRun              79/80
Rank                    79/80
FFT                     80/80
OverlappingTemplate     78/80
Universal               79/80
ApproximateEntropy      79/80
Serial                  80/80
Serial                  79/80
LinearComplexity        80/80
```

Для многочисленных под-тестов:

```text
NonOverlappingTemplate
```

пропорции находились в диапазоне:

```text
77/80 – 80/80
```

что не ниже минимальной границы:

```text
76/80
```

---

# Random Excursions

Для Random Excursions было доступно:

```text
53
```

последовательности.

Полученные пропорции находились в диапазоне:

```text
51/53 – 53/53
```

Минимально допустимое значение:

```text
50/53
```

Таким образом, требование по пропорции выполнено.

---

# Random Excursions Variant

Для Random Excursions Variant также использовались:

```text
53
```

последовательности.

Полученные значения находились в диапазоне:

```text
51/53 – 53/53
```

Минимально допустимое значение:

```text
50/53
```

Требование по пропорции также выполнено.

---

# P-VALUE в NIST STS

Подавляющее большинство полученных значений `P-VALUE` находится выше:

```text
0.01
```

В одном из под-тестов `NonOverlappingTemplate` получено:

```text
P-VALUE = 0.004715
PROPORTION = 79/80
```

При этом пропорция прошедших последовательностей значительно выше требуемой:

```text
76/80
```

Значение uniformity P-VALUE также остаётся выше критической границы:

```text
0.0001
```

Единичное такое значение среди большого количества под-тестов не свидетельствует о систематической проблеме генератора.

---

# Итог NIST STS

По результатам выполненного статистического тестирования:

```text
NIST STS: PASSED
```

Все 15 групп статистических тестов были выполнены.

Пропорции успешно прошедших последовательностей соответствуют минимальным значениям, указанным итоговым отчётом NIST STS.

Большинство полученных P-VALUE значительно превышают уровень:

```text
0.01
```

Статистическое тестирование не выявило систематических признаков неудовлетворительного распределения случайных данных CSPRNG.

TEST-3 Sprint 3 выполнен.

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

# Основные файлы Sprint 3

## csprng.py

```text
src/cryptocore/csprng.py
```

Содержит общий криптографически стойкий генератор случайных байтов на основе `os.urandom()`.

---

## iv.py

```text
src/cryptocore/iv.py
```

Использует общий CSPRNG для создания 16-байтовых IV.

---

## cli_parser.py

```text
src/cryptocore/cli_parser.py
```

Поддерживает необязательный `--key` при шифровании и обязательный `--key` при расшифровании.

---

## main.py

```text
src/cryptocore/main.py
```

Реализует:

- автоматическую генерацию ключа;
- вывод сгенерированного ключа;
- использование пользовательского ключа;
- предупреждение о слабых ключах;
- выбор режима;
- генерацию и обработку IV;
- обработку ошибок.

---

## nist_data.py

```text
src/cryptocore/nist_data.py
```

Реализует генерацию большого бинарного файла случайных данных для NIST STS.

---

## generate_nist_data.py

```text
scripts/generate_nist_data.py
```

Создаёт:

```text
nist_test_data.bin
```

размером 10 000 000 байт.

---

# Основные тесты Sprint 3

## test_csprng.py

Проверяет:

- длину данных;
- тип данных;
- уникальность;
- 1000 случайных значений;
- базовое распределение битов;
- ошибки размера;
- ошибку системного источника случайности.

---

## test_iv.py

Проверяет:

- длину IV;
- разбор hexadecimal IV;
- добавление IV к ciphertext;
- извлечение IV;
- использование общего CSPRNG для генерации IV.

---

## test_cli.py

Проверяет:

- поддерживаемые режимы;
- ключ AES-128;
- использование IV;
- запрет IV при шифровании;
- запрет IV для ECB;
- необязательный ключ при шифровании;
- обязательный ключ при расшифровании;
- сохранение поддержки пользовательского ключа.

---

## test_modes_integration.py

Проверяет:

- round-trip режимов;
- IV в начале зашифрованного файла;
- расшифрование с явно переданным IV;
- сохранение работы ECB;
- автоматическую генерацию AES-ключа;
- использование пользовательского ключа;
- обнаружение простых слабых ключей;
- вывод предупреждения в stderr.

---

## test_nist_data.py

Проверяет:

- создание файла случайных данных;
- требуемый размер;
- наличие записанных данных;
- отсутствие постоянного одинакового значения.

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

Добавить OpenSSL в PATH:

```powershell
$env:Path += ";C:\Program Files\OpenSSL-Win64\bin"
```

Проверить:

```powershell
openssl version
```

Запустить interoperability:

```powershell
python scripts/openssl_interop_test.py
```

При успешной проверке:

```text
Result: 11/11 checks passed
OpenSSL interoperability: PASSED
```

Проверить состояние Git:

```powershell
git status
```

Для полностью сохранённого проекта:

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
- проверка совместимости AES-128 ECB с OpenSSL.

---

# Итоги Sprint 2

В Sprint 2 реализованы:

- AES-128 CBC;
- AES-128 CFB-128;
- AES-128 OFB;
- AES-128 CTR;
- ручная логика режимов поверх AES-примитива;
- генерация IV;
- формат `<IV><ciphertext>`;
- поддержка явного `--iv` при расшифровании;
- interoperability с OpenSSL;
- проверка совместимости в обоих направлениях.

---

# Итоги Sprint 3

В Sprint 3 реализованы:

- отдельный CSPRNG-модуль;
- функция `generate_random_bytes(num_bytes)`;
- использование `os.urandom()`;
- обработка ошибок системного источника случайности;
- автоматическая генерация 16-байтового AES-128 ключа;
- вывод автоматически созданного ключа в stdout;
- отсутствие ключа в ciphertext;
- обязательный `--key` при расшифровании;
- поддержка пользовательского ключа при шифровании;
- предупреждение о потенциально слабых ключах;
- перевод всех IV на единый CSPRNG;
- тест 1000 уникальных 128-битных значений;
- базовая проверка распределения единичных битов;
- генерация 10 MB данных для NIST STS;
- автоматические тесты генерации файла;
- полный запуск NIST Statistical Test Suite 2.1.2;
- запуск всех 15 статистических тестов;
- проверка 80 последовательностей по 1 000 000 бит;
- подтверждение соответствия пропорций установленным границам NIST.

Полный прогон NIST STS выполнен.