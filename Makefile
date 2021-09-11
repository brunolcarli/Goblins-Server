
run:
	python manage.py runserver 0.0.0.0:11000 --settings=game_server.settings.common


migrate:
	python manage.py makemigrations --settings=game_server.settings.common
	python manage.py migrate --settings=game_server.settings.common