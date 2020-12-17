# micropythonapi
make an api which offers up data from a database. test it local and then host it on Bookku.

## Quick!

We need a microservice hosted on Bookku! It needs to "speak" a REST API. It has to be backed by a PostgresQL database. 
The boss says you have to use Django and Django REST Framework (DRF) to do the work.

At this point, this project has got a django site running, with an admin set of pages.

The data we need loaded into the SQL database is in the `bestsellers-with-categories.csv` file. There i data on 550 some books in there.

First you need to get the Django project running! You need to run some setup commands:

```
$ git checkout main
$ python3 -m venv venv
$ source venv/bin/activate
$ pip3 install -r requirements.txt
$ cd booksapi

$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py createsuperuser --email admin@example.com --username admin

$ python manage.py runserver
```

Create a python virtual env for the project on your local machine.

Start it by source'ing the activation.

Pip install all the required packages for the project.

CD into the main code directory.

Then first `manage.py` commands creates all the migrations for the database schema. The second applies them to the current database. (Locally that will be sqlite, on Bookku it will be Postgres) The third puts a "superuser" into the database so you can log into the admin inteface within the django site.

The fourth runs the server.
Look at both 
`http://localhost:8000` and `http://localhost:8000/admin`
The second you should oogin as admin with the password you chose in the createsuperuser step.

### Your Mission

Work thru these steps. 

### Serialize the Book model

Now we’re starting to get into some new waters. We need to tell REST Framework about our Book model and how it should serialize the data.
Remember, serialization is the process of converting a Model to JSON. Using a serializer, we can specify what fields should be present in the JSON representation of the model.
The serializer will turn our Books into a JSON representation so the API user can parse them, even if they’re not using Python. In turn, when a user POSTs JSON data to our API, the serializer will convert that JSON to a Book model for us to save or validate.
To do so, let’s create a new file — books/serializers.py
In this file, we need to:

- Import the Book model
- Import the REST Framework serializer
- Create a new class that links the Book with its serializer

Here’s how:

```
# serializers.py
from rest_framework import serializers

from .models import Book

class BookSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Book
        fields = ('name', 'alias')
```

### Display the data

Now, all that’s left to do is wire up the URLs and views to display the data!

#### Views

Let’s start with the view. We need to render the different Books in JSON format.
To do so, we need to:

- Query the database for all Books
- Pass that database queryset into the serializer we just created, so that it gets converted into JSON and rendered

In books/views.py:

```
# views.py
from rest_framework import viewsets

from .serializers import BookSerializer
from .models import Book


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by('name')
    serializer_class = BookSerializer
```

ModelViewSet is a special view that Django Rest Framework provides. It will handle GET and POST for Books without us having to do any more work.

#### Site URLs

Okay, awesome. We’re soooooo close. The last step is to point a URL at the viewset we just created.

In Django, URLs get resolved at the project level first. So there’s a file in booksapi/booksapi directory called urls.py .

Head over there. You’ll see the URL for the admin site is already in there. Now, we just need to add a URL for our API. For now, let’s just put our API at the index:

# booksapi/urls.py
```
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('books.urls')),
 ]
```

#### API URLs

If you’re paying attention and not just blindly copy-pasting, you’ll notice that we included 'booksapi.urls' . That’s a path to a file we haven’t edited yet. And that’s where Django is going to look next for instructions on how to route this URL.

So, let’s go there next — books/urls.py:
```
# booksapi/urls.py
from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'Books', views.BookViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
```

Notice we added something called router that we imported from rest_framework.
The REST Framework router will make sure our requests end up at the right resource dynamically. If we add or delete items from the database, the URLs will update to match. Cool right?

A router works with a viewset (see views.py above) to dynamically route requests. In order for a router to work, it needs to point to a viewset, and in most cases, if you have a viewset you’ll want a router to go with it.

So far, we’ve only added one model+serializer+viewset to the router — Books. But we can add more in the future repeating the same process above for different models! 

Of course, if you only want to use standard DRF Views instead of viewsets, then urls.py will look a little different. You don’t need a router to use simple views, and you can just add them with:

`path('path/to/my/view/', MySimpleView.as_view())`

Test it out!

Start up the Django server again:
```
$ python manage.py runserver
```

Now go to localhost:8000

### What about Data?

First, add three books (three of your favorite) for test data. They do not have ot be real. Make sure that your API returns a JSON payload that contains your test books.

Then, you need to figure out how to load the 550 books in the big csv file.

Well, decide on using one of these methods to read the data into your local sqlite database.

https://stackoverflow.com/questions/2459979/how-to-import-csv-data-into-django-models

### Okay, Heroku

Now I'd like you to save all your changes to github, and figure out a way to load all this up to a Heroku app. https://heroku.com 
Get a free account.
Download the CLI - use it to make your app and then to move your app from your git repo up to heroku and run it.
Heroku is a terrific hosting site that allows you to take a complete python app like this one and put it up and make it publicly available.

There are a lot of pages that help you do this. By the way, the Procfile I supplied, it might or might not work. It might need editing.

You will need to load your data from the csv into your Heroku database too. So be careful when you choose a method. 
If you do a pip install to add a python package to load the data, you need to add that package to the requirements.txt file. 
(That way, Heroku will know you need it and install it automatically for you like it does with all the other required packages.)

### Useful commands

run this from inside the `micropythonapi/booksapi` folder

`python manage.py runserver` will start python web server on your local machine running on port 8000

click on `http://localhost:8000` and `http://localhost:8000/admin` 