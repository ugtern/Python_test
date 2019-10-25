# Python_test

порядок действий:

1) python -m venv ./venv - устанавливаем виртуальное окружение из которого будет работать тестер
2) с запущенным ВО (source ./venv/bin/activate) запускаем pip install -r requirements.txt
3) docker-compose build
4) docker-compose up
5) переходим в каталог фронтенда и запускаем npm install
6) npm run dev
готово. для запуска проекта docker-compose up, для запуска тестов из виртуального окружения python tester.py