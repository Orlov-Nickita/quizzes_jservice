# Описание проекта

Данное приложение создано для пополнения базы данных вопросами для викторины. Используются Flask, SQLAlchemy,
PostgreSQL, Docker. Возможно развернуть путем непосредственного запуска приложения, а также путем разворачивания
контейнера через docker-compose. Сервис обращается по API к ресурсу https://jservice.io/ и записывает необходимое
количество вопросов в базу данных (по умолчанию - 4 вопроса). В БД записывается вопрос, ответ, сложность, дата создания
вопроса и ID вопроса (соответствует ID получаемого вопроса от ресурса jservice.io)

# Настройка работы путем контейнеризации через docker-compose

## Подготовка перед запуском

1. Если Docker и docker-compose не установлены, то необходимо, руководствуясь документацией, осуществить установку
   дистрибутивов:
   https://docs.docker.com/engine/install/ubuntu/
   https://docs.docker.com/compose/install/linux/

2. Нужно создать папку на хостовой машине (в этой папке будет храниться копия базы данных из контейнера). При изменении
   директории, надо внести соответствующие правки в файл docker-compose на строке 34

```text
/var/lib/postgresql/quizzes/
```

3. Дать ей права на запись пользователю, под которым запускается Docker

```text
sudo chown -R $USER:$USER /var/lib/postgresql/quizzes/
```

Пример:

```text
sudo chown -R orlovnikita:orlovnikita /var/lib/postgresql/quizzes/
```

4. Открыть в терминале папку quizzes_jservice, содержащую текущий проект и выполнить две последовательные команды.
   Ожидание сборки образа контейнера составит примерно 1-2 минуты в зависимости от скорости интернета. Результатом
   станет
   запущенное flask приложение. Обратиться к нему можно через URL-адрес http://127.0.0.1:5000/questions/

```text
docker-compose build
docker-compose up
```

5. Проверить работу можно посредством отправки запроса

```text
curl -X POST -H "Content-Type: application/json" -d '{"questions_num": 4}' http://127.0.0.1:5000/questions/
```

Если после первоначального запуска возникнет ошибка
<pre>sqlalchemy.exc.OperationalError: TCP/IP connections on port 5432?</pre>
нужно перезапустить контейнер

## Просмотр базы данных из контейнера

1. Посредством команды docker ps смотрим ID действующей контейнера с базой данных postgres и далее подключаемся к
   нему через команду, где bf5f07cb3611 - это ID

```text
docker exec -it bf5f07cb3611 bash
```

2. Подключаемся к базе данных, где "DB_USER" и "DB_NAME" это параметры из файла docker-compose.yml

```text
psql -U "DB_USER" -d "DB_NAME"
```

## Примечание

Локальное хранение копии базы данных приводит к тому, что в случае каких-либо изменений в
переменных окружения после первого запуска контейнера могут возникать ошибки с доступом к БД

# Настройка работы проекта на операционной среде Linux без использования docker-compose

## Установка виртуального окружения и библиотек/пакетов

1. Создаем виртуальное окружение. Данная команда создаст папку venv в папке, откуда была выполнена команда, и в
   терминале появится запись *(venv)*

```text
python3 -m venv venv
```

2. Устанавливаем все требуемые для работы библиотеки. Для этого необходимо в терминале (находясь в папке, в которой
   расположен файл requirements.txt) выполнить следующую команду:

```text
pip install -r requirements.txt
```

## Подготовка базы данных PostgreSQL и создание виртуального окружения переменных

1. Подключаемся к терминалу psql от имени пользователя по умолчанию postgres

```text
sudo -u postgres psql
```

2. Создаем базу данных, создаем нового пользователя, меняем некоторые настройки (кодировка, чтение транзакций и
   часовой пояс), открываем для созданного пользователя все возможности работы с новой БД

```postgresql
CREATE DATABASE db_name;
CREATE USER username WITH PASSWORD 'password';
ALTER ROLE username SET client_encoding TO 'utf8';
ALTER ROLE username SET default_transaction_isolation TO 'read committed';
ALTER ROLE username SET timezone TO 'Europe/Moscow';
GRANT ALL PRIVILEGES ON DATABASE db_name TO username;
```

3. В директории вместе с текущим файлом расположен файл ".env.template". Нужно переименовать его в ".env" и переместить
   в одну директорию вместе с файлом settings.py, а потом заполнить по принципу:

```dotenv
DEBUG=True_or_False
#в соответствии с созданными пользователем и БД
DB_NAME=db_name
DB_USER=username
DB_PASSWORD=password
DB_HOST=localhost
```
