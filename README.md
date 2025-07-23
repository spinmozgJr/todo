# Запуск
docker-compose up --build

# API
- Регистрация POST /api/v1/auth/users/
- Логин POST /auth/token/login/
- Выход POST /auth/token/logout/
- Все доступные задачи GET /api/v1/todos
- Конкретная задача GET /api/v1/todos/{id}
- Содание задачи POST /api/v1/todos/
- Обновление задачи PATCH api/v1/todos/{id}/
- Удаление задачи DELETE api/v1/todos/{id}/
- Экспорт задач POST /api/todos/export/
- Фильтр ?status=done/pending priority=low/medium/high
- Поиск ?search=
