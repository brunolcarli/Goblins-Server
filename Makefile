
run:
	python manage.py runserver 0.0.0.0:11000


migrate:
	python manage.py makemigrations
	python manage.py migrate