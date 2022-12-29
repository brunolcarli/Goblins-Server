
run:
	python manage.py runserver 0.0.0.0:11000 --settings=game_server.settings.${ENV_REF}


migrate:
	python manage.py makemigrations --settings=game_server.settings.${ENV_REF}
	python manage.py migrate --settings=game_server.settings.${ENV_REF}


install:
	pip install -r requirements.txt


shell:
	python manage.py shell --settings=game_server.settings.${ENV_REF}

run_docker:
	docker-compose build
	docker-compose up -d
	docker exec game_server_container ./manage.py migrate

pipe:
	make install
	make migrate
	make run
