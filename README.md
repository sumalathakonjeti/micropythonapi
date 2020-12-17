# micropythonapi
make an api which offers up data from a database. test it local and then host it on Heroku.

## Quick!

We need a microservice hosted on Heroku! It needs to "speak" a REST API. It has to be backed by a PostgresQL database. 
The boss says you have to use Django and Django REST Framework (DRF) to do the work.

At this point, this project has got a django site running, with an admin set of pages.

The data we need loaded into the SQL database is in the `bestsellers-with-categories.csv` file. There i data on 550 some books in there.

First you need to get the Django project running! You need to run some setup commands:

```
$ python3 -m venv venv
$ source venv/bin/activate
$ pip3 install -r requirements.txt
$ cd booksapi
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py createsuperuser --email admin@example.com --username admin
$
```

1) create a python virtual env for the project on your local machine.

The first of these creates all the migrations for the database schema. The second applies them to the current database. (Locally that will be sqlite, on Heroku it will be Postgres) The Third puts a "superuser" into the database so you can log into the admin inteface within the django site.

### Useful commands

run these from inside the `micropythonapi/booksapi` folder

`python manage.py runserver` will start python web server on your local machine running on port 8000

click on `http://localhost:8000` and `http://localhost:8000/admin` 