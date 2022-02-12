![Actions Status](https://github.com/wwwwwdy/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)
# Foodgram
### Foodgram - это ваш продуктовый помощник
***
### Описание проекта:

Проект Foodgram собирает любимые рецепты пользователей. 
Подписываясь на любимых авторов, можно отслеживать их обновления.
Рецепты можно добавлять в избранное, а также положить в корзину покупок и скачать перечень необходимых ингредиентов!
***
### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```bash
https://github.com/wwwwwdy/foodgram-project-react.git
```

```bash
cd foodgram-project-react
```

Cоздать и активировать виртуальное окружение:

```bash
python -m venv env
```

```bash
source env/bin/activate
```

```bash
python -m pip install --upgrade pip
```

Перейти в директирию и установить зависимости из файла requirements.txt:

```bash
cd backend/foodgram&&pip install -r requirements.txt
```

Выполнить миграции:

```bash
python manage.py migrate
```

Запустите docker-compose командой:
```bash
docker-compose up -d
```
Развернутое приложение доступно по адресу:
```
http://62.84.121.150/
```

