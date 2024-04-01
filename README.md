# Авторизатор
## Описание проекта

Этот проект представляет собой API для управления пользователями и их ролями. Он реализован с использованием Python, FastAPI, SQLAlchemy и других технологий.
Установка и запуск

1) Клонируйте репозиторий на локальную машину:

```bash
git clone https://github.com/Dadoxr/fast_api.git
```
2) Перейдите в каталог проекта:

```bash
cd fast_api
```
4) Установите зависимости:

```bash
python3 -m venv .venv
. .venv/bin/activate
mv .env.sample .env
pip install -r requirements.txt
```

5) Настройте конфигурацию сервера:

```bash
make up
make init
```
5) Добавьте в env.py следующий вместо строчки `target_metadata = None`

```bash
import settings
config.set_main_option('sqlalchemy.url', settings.ALEMBIC_SQLALCHEMY_DATABASE_URL)
from db.models import Base
target_metadata = Base.metadata
```

7) Запустите приложение
```bash
make revision
make upgrade
make run
```
