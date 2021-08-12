# book_store_Razaghi
## Introduction

book store is an app for selling books online.
### Setup

You will need requirements.txt content to run this app.
use the following command in terminal

```bash
$ pip install -r requirements.txt
```

then

```bash
$ python manage.py makemigrations
```

This will create all the migrations file (database migrations) required to run this App.

Now, to apply this migrations run the following command
```bash
$ python manage.py migrate
```

One last step and then our todo App will be live. We need to create an admin user to run this App. On the terminal, type the following command and provide username, password and email for the admin user
```bash
$ python manage.py createsuperuser
```

Start the server by following command

```bash
$ python manage.py runserver
```
## Technologies used:

- **Backend**: Python Django Framework 3.12.4
- **Frontend**: HTML, CSS, JS + Bootstrap, jQuery
- **Database**: postgreSQL
