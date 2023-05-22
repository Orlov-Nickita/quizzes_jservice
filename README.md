# Настройка работы проекта на операционной среде Linux

## Установка виртуального окружения и библиотек/пакетов

Установка всех необходимых библиотек производится с использованием файла с зависимостями requirements.txt

Перед установкой пакетов и библиотек, необходимо удостовериться, что все действия происходят внутри виртуального
окружения. Поэтому сначала необходимо его создать (если этого еще не было сделано)

```text
python3 -m venv venv
```

Данная команда создаст папку venv в папке, откуда была выполнена команда, и в терминале появится запись *(venv)*
Теперь можно выполнить установку всех требуемых для работы библиотек и пакетов.
Для этого необходимо в терминале (находясь в папке, в которой расположен файл requirements.txt) выполнить следующую
команду:

```text
pip install -r requirements.txt
```

## Подготовка базы данных PostgreSQL и создание виртуального окружения переменных

Подключаемся к терминалу psql от имени пользователя по умолчанию postgres, выполнив следующий код

```text
sudo -u postgres psql
```

Создаем базу данных, создаем нового пользователя, меняем некоторые настройки (кодировка, чтение транзакций и 
часовой пояс), открываем для созданного пользователя все возможности работы с новой БД

```postgresql
CREATE DATABASE db_name;
CREATE USER username WITH PASSWORD 'password';
ALTER ROLE username SET client_encoding TO 'utf8';
ALTER ROLE username SET default_transaction_isolation TO 'read committed';
ALTER ROLE username SET timezone TO 'Europe/Moscow';
GRANT ALL PRIVILEGES ON DATABASE db_name TO username;
```

В директории вместе с текущим файлом расположен файл ".env.template". Нужно переименовать его в ".env" и переместить
в одну директорию вместе с файлом settings.py, а потом заполнить по принципу:

```dotenv
DEBUG=True_or_False
#в соответствии с созданными пользователем и БД
DB_NAME=db_name
DB_USER=username
DB_PASSWORD=password
DB_HOST=localhost
```
