# Тестовое задание на позицию junior python developer
## Руководство по запуску и настройке приложения
### Сертификаты для успешной генерации JWT
Приложение использует аутентификацию и авторизацию при помощи JWT.
<br>
Для генерации public и private ключей нужно использовать следующие команды, чтобы сгенерировать ключи:
<br>
- _требуется предварительная установка утилиты **openssl**_
``` terminal
mkdir certs
openssl genrsa -out certs/jwt-private.pem 2048
openssl rsa -in certs/jwt-private.pem -outform PEM -pubout -out certs/jwt-public.pem
```
- **_mkdir certs_** - создание директории для хранения ключей
- **_openssl genrsa -out certs/jwt-private.pem 2048_** - генерация **public** ключа
- **_openssl rsa -in certs/jwt-private.pem -outform PEM -pubout -out certs/jwt-public.pem_** - генерация **public** ключа на основе **private**
<br>

Для демонстрации задания директория **_certs_** с ключами уже создана. 
### Переменные окружения
В корне проекта приведен файл **_.env-example_**, по которому нужно создать **_.env_**:
<br>
```
MODE=PROD

DB_NAME=postgres
DB_USER=postgres
DB_PASS=YOUR_PASSWORD_FOR_POSTGRES_USER  # изменить на свой пароль
DB_HOST=postgre
DB_PORT=5432

POSTGRES_PASSWORD=YOUR_PASSWORD_FOR_POSTGRES_USER  # изменить на свой пароль

TEST_DB_NAME=postgres
TEST_DB_USER=postgres
TEST_DB_PASS=postgres
TEST_DB_HOST=postgre
TEST_DB_PORT=5432

ALGORITHM=ALGORITHM
```

### Запуск приложения
Приложение запускается в docker-контейнере по команде:
``` terminal
docker compose up --build
```