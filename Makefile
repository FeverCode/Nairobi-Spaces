serve:
	python3 manage.py runserver

migrate:
	python3 manage.py migrate

check:
	python3 manage.py check

shell:
	python3 manage.py shell

makemigrations:
	python3 manage.py makemigrations

test:
	coverage run manage.py test && coverage report && coverage html

superuser:
	python3 manage.py createsuperuser