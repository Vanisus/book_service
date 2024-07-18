# Система управления библиотекой

Этот проект представляет собой систему управления библиотекой на основе микросервисов, которая позволяет управлять книгами, пользователями, арендой и загрузкой файлов. Проект состоит из нескольких микросервисов, каждый из которых отвечает за определенную часть системы. Микросервисы взаимодействуют друг с другом через HTTP-запросы.

## Микросервисы

1. **API Gateway**: Входная точка для всех клиентов, маршрутизирующая запросы к соответствующим микросервисам.
2. **Book Service**: Управление книгами, включая добавление, обновление и получение информации о книгах.
3. **User Service**: Управление пользователями, включая регистрацию и получение информации о пользователях.
4. **Rental Service**: Управление арендой книг, включая аренду и возврат книг.
5. **File Service**: Управление загрузкой и хранением файлов, связанных с книгами.

## Возможности

- **Управление книгами**: Добавление, обновление и получение информации о книгах.
- **Управление пользователями**: Регистрация и получение информации о пользователях.
- **Управление арендой**: Аренда и возврат книг.
- **Загрузка файлов**: Загрузка и управление файлами, связанными с книгами.
- **API Gateway**: Централизованная входная точка для маршрутизации запросов к соответствующим микросервисам.

## Подготовка

- Установите Docker и Docker Compose на свою систему.
- Базовые знания о FastAPI и Docker.

## Запуск проекта

### Клонирование репозитория

```bash
git clone https://github.com/your-repo/library-management-system.git
cd library-management-system
```

### Переменные окружения

Создайте файл `.env` в корневом каталоге проекта и добавьте необходимые переменные окружения. Пример файла `.env`:

```env

DATABASE_URL=postgresql+asyncpg://user:password@postgres:5432/book_service
FILE_SERVICE_URL=http://file_service:5004

BOOK_SERVICE_URL=http://book_service:5007
USER_SERVICE_URL=http://user_service:5005
RENTAL_SERVICE_URL=http://rental_service:5006
FILE_SERVICE_URL=http://file_service:5004

UPLOAD_DIRECTORY=/app/uploads
```

### Docker Compose

Соберите и запустите сервисы с помощью Docker Compose:

```bash
docker compose up --build
```

### Доступ к сервисам

- API Gateway: `http://localhost:5008`
- К остальным сервисам открыт доступ только через API Gateway

### Swagger UI

Каждый сервис предоставляет автоматически сгенерированный интерфейс Swagger UI для изучения API:

- API Gateway: `http://localhost:5008/docs`

## Вклад

Не стесняйтесь форкать репозиторий и отправлять пул-реквесты. Для крупных изменений сначала откройте issue, чтобы обсудить, что вы хотите изменить.

## Лицензия

Этот проект лицензирован под лицензией MIT. См. файл LICENSE для подробностей.
