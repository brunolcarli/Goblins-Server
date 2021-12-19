
run:
	python manage.py runserver 0.0.0.0:11000 --settings=game_server.settings.common


migrate:
	python manage.py makemigrations --settings=game_server.settings.common
	python manage.py migrate --settings=game_server.settings.common


install:
	pip install -r game_server/requirements/${ENV_REF}.txt


shell:
	python manage.py shell --settings=game_server.settings.${ENV_REF}
