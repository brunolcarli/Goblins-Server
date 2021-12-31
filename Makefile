
run:
	python manage.py runserver 0.0.0.0:11000 --settings=game_server.settings.${ENV_REF}


migrate:
	python manage.py makemigrations --settings=game_server.settings.${ENV_REF}
	python manage.py migrate --settings=game_server.settings.${ENV_REF}


install:
	pip install -r game_server/requirements/${ENV_REF}.txt


shell:
	python manage.py shell --settings=game_server.settings.${ENV_REF}
