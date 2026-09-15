# CryptoCore

CryptoCore — консольная программа для шифрования и расшифрования файлов с использованием алгоритма AES-128 в режиме ECB и дополнения PKCS#7.

## Возможности

Программа поддерживает:

* алгоритм AES-128;
* режим ECB;
* шифрование файлов;
* расшифрование файлов;
* текстовые и бинарные файлы;
* ключи в шестнадцатеричном формате;
* PKCS#7 padding;
* автоматическое формирование имени выходного файла;
* проверку ошибок входных параметров;
* тестирование полного цикла шифрования и расшифрования.

## Требования

Для работы проекта необходимы:

* Python 3.10 или новее;
* pip;
* библиотека PyCryptodome.

Основная криптографическая зависимость:

```text
pycryptodome>=3.20.0
```

Для запуска автоматических тестов дополнительно используется:

```text
pytest
```

## Структура проекта

```text
cryptocore/
├── src/
│   └── cryptocore/
│       ├── __init__.py
│       ├── __main__.py
│       ├── main.py
│       ├── cli_parser.py
│       ├── file_io.py
│       ├── padding.py
│       └── modes/
│           ├── __init__.py
│           └── ecb.py
│
├── tests/
│   ├── test_padding.py
│   ├── test_ecb.py
│   └── test_cli.py
│
├── scripts/
│   └── round_trip_test.py
│
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Установка

### 1. Создание виртуального окружения

Windows PowerShell:

```powershell
python -m venv .venv
```

### 2. Активация виртуального окружения

```powershell
.\.venv\Scripts\Activate.ps1
```

После активации в начале строки терминала должно появиться:

```text
(.venv)
```

### 3. Установка зависимостей

```powershell
pip install -r requirements.txt
```

Для запуска тестов:

```powershell
pip install pytest
```

### 4. Установка CryptoCore

Из корневой директории проекта:

```powershell
pip install -e .
```

После установки программа становится доступна через команду:

```powershell
cryptocore
```

Проверить установку можно командой:

```powershell
cryptocore --help
```

## Использование

Общий формат команды:

```text
cryptocore --algorithm ALGORITHM --mode MODE (--encrypt | --decrypt) --key KEY --input INPUT_FILE [--output OUTPUT_FILE]
```

Для текущей версии поддерживаются:

```text
--algorithm aes
--mode ecb
```

### Параметры

`--algorithm`

Определяет алгоритм шифрования.

В текущем спринте поддерживается только:

```text
aes
```

`--mode`

Определяет режим работы блочного шифра.

В текущем спринте поддерживается только:

```text
ecb
```

`--encrypt`

Выполнить шифрование.

`--decrypt`

Выполнить расшифрование.

Одновременно можно указать только один из параметров:

```text
--encrypt
--decrypt
```

`--key`

Ключ AES-128 в шестнадцатеричном формате.

Ключ должен содержать 16 байт, то есть 32 шестнадцатеричных символа.

Пример:

```text
000102030405060708090a0b0c0d0e0f
```

`--input`

Путь к входному файлу.

`--output`

Путь к выходному файлу.

Параметр является необязательным. Если он не указан, CryptoCore автоматически сформирует имя выходного файла.

## Пример шифрования

Исходный файл:

```text
plaintext.txt
```

Команда:

```powershell
cryptocore --algorithm aes --mode ecb --encrypt --key 000102030405060708090a0b0c0d0e0f --input plaintext.txt --output ciphertext.bin
```

После выполнения будет создан файл:

```text
ciphertext.bin
```

## Пример расшифрования

```powershell
cryptocore --algorithm aes --mode ecb --decrypt --key 000102030405060708090a0b0c0d0e0f --input ciphertext.bin --output decrypted.txt
```

После выполнения будет создан:

```text
decrypted.txt
```

Его содержимое должно полностью совпадать с исходным файлом `plaintext.txt`.

## Автоматическое имя выходного файла

Параметр `--output` можно не указывать.

Например:

```powershell
cryptocore --algorithm aes --mode ecb --encrypt --key 000102030405060708090a0b0c0d0e0f --input plaintext.txt
```

Программа автоматически создаст:

```text
plaintext.txt.enc
```

При расшифровании:

```powershell
cryptocore --algorithm aes --mode ecb --decrypt --key 000102030405060708090a0b0c0d0e0f --input plaintext.txt.enc
```

будет создан:

```text
plaintext.txt.enc.dec
```

## Реализация AES-128 ECB

CryptoCore использует AES-примитив из библиотеки PyCryptodome:

```python
from Crypto.Cipher import AES
```

Сам алгоритм AES не реализуется вручную.

Логика режима ECB реализована в проекте отдельно:

1. входные данные дополняются по стандарту PKCS#7;
2. данные разбиваются на блоки размером 16 байт;
3. каждый блок отдельно передаётся AES;
4. зашифрованные блоки объединяются;
5. при расшифровании выполняется обратная операция;
6. PKCS#7 padding проверяется и удаляется.

## PKCS#7 Padding

AES использует блоки размером 16 байт.

Если размер файла не кратен 16 байтам, перед шифрованием к нему добавляются дополнительные байты согласно стандарту PKCS#7.

При расшифровании padding проверяется и удаляется.

## Работа с файлами

Файлы читаются и записываются в бинарном режиме.

Поэтому CryptoCore может работать как с текстовыми, так и с бинарными файлами, например:

```text
.txt
.bin
.jpg
.png
.pdf
.zip
```

## Тестирование

Для запуска автоматических тестов используется pytest.

Команда:

```powershell
pytest
```

Тесты проверяют:

* PKCS#7 padding;
* удаление padding;
* некорректный padding;
* AES-128 ECB шифрование;
* AES-128 ECB расшифрование;
* обработку нескольких блоков;
* обработку бинарных данных;
* проверку длины ключа;
* проверку hexadecimal-ключа;
* обработку некорректного ciphertext.

## Round-trip тест

Также проект содержит отдельный тест полного цикла:

```powershell
python scripts/round_trip_test.py
```

Он выполняет:

```text
исходный файл
      ↓
шифрование
      ↓
ciphertext
      ↓
расшифрование
      ↓
сравнение с исходным файлом
```

При успешной проверке программа выводит:

```text
PASS: расшифрованный файл полностью совпадает с исходным.
```

## Ручная проверка файлов

В Windows PowerShell можно проверить полное совпадение файлов на уровне байтов:

```powershell
$original = [System.IO.File]::ReadAllBytes("roundtrip_original.txt")
$decrypted = [System.IO.File]::ReadAllBytes("roundtrip_decrypted.txt")

[System.Linq.Enumerable]::SequenceEqual($original, $decrypted)
```

Успешный результат:

```text
True
```

## Обработка ошибок

CryptoCore проверяет:

* наличие обязательных аргументов;
* правильность алгоритма;
* правильность режима;
* наличие ровно одного действия `--encrypt` или `--decrypt`;
* hexadecimal-формат ключа;
* длину AES-128 ключа;
* существование входного файла;
* возможность чтения и записи файлов;
* корректность длины ciphertext;
* корректность PKCS#7 padding.

При ошибке выводится понятное сообщение, а программа завершается с ненулевым кодом возврата.

## Зависимости

Основная библиотека:

```text
PyCryptodome
```

Установка:

```powershell
pip install pycryptodome
```

Библиотека используется для AES-примитива:

```python
Crypto.Cipher.AES
```

Для тестирования:

```text
pytest
```

Установка:

```powershell
pip install pytest
```
