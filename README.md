$ """ Mac Linux """
$ virtualenv env
$ source env/bin/activate
$ python3 -m venv env
$ pip3 install -r requirements.txt

$ python3 manage.py makemigrations
$ python3 manage.py migrate
$ python3 manage.py createsuperuser
$ python3 manage.py runserver

$ """ Windown """
$ virtualenv env_win
$ .\env_win\Scripts\activate
$ pip install -r requirements.txt

$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py createsuperuser
$ python manage.py runserver

$pip freeze > requirements.txt
