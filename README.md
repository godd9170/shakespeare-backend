# Shakespeare-backend
[![CircleCI](https://circleci.com/gh/Saasli/shakespeare-backend/tree/master.svg?style=svg&circle-token=169056e79165a14b945cc31617539c132b8083b6)](https://circleci.com/gh/Saasli/shakespeare-backend/tree/master)

## Getting Started

The best way to develop this API is with a python3 virtual environment. I like to keep the venv within this repo (it's .gitignored so long as you call it *-venv or ENV) such that the tree looks like this:

```
.
├── ENV
│   ├── bin
│   ├── include
│   ├── lib
│   └── pip-selfcheck.json
├── README.md
├── requirements.txt
└── shakespeare
    └── manage.py
```

Instructions on setting up a virtual environment can be found below.

### Create a Virtual Env + Install Packages

1) Get virtualenv

```sudo pip install virtualenv```

2) Create a new virtual env in python 3

```virtualenv -p python3 shakespeare-venv```

3) Install all the requirements

```pip install -r requirements.txt```

### Create a local Dev DB

`shakespeare-backend` uses postgres, so you'll need to set up a local psql server in order to run it.

1) Create a new local db

```
psql
CREATE DATABASE shakespeare-dev;
```

2) Create a db new user and allow them to make new DBs (for testing)

```
CREATE USER shakespeareadmin WITH PASSWORD 'salesforce1';
ALTER USER shakespeareadmin CREATEDB;
```

### Redis and Celery

1) Starting Redis

```
redis-server &
```

2) Starting Celery workers

From the project's root folder (the one containing ``manage.py``) run:
```
celery worker -A shakespeare --loglevel=INFO
```

## Elastic Beanstalk Deploys

Obtain ebcli tools with

```
pip install awsebcli
```

Make sure that you've got an AWS account, and your credentials are environment variables named

```
export AWS_ACCESS_KEY_ID=xxx
export AWS_SECRET_ACCESS_KEY=xxx
```

Make sure that whatever elastic beanstalk url is generated, is put into the `shakespeare.settings` `ALLOWED_HOSTS`

```eb deploy```

## Notable Libraries

#### [social-app-django](http://python-social-auth.readthedocs.io/)

Used to a) authenticate users into the app, b) permit access to the gmail SMTP server.

#### [django-rest-framework](http://django-rest-framework.readthedocs.io/en/latest/)

Handles the exposure of the shakespeare API

#### [django-organizations](https://github.com/bennylope/django-organizations)

A schema that defines organizations so we can share shakespeare resources across multiple users of a common account.

#### [django-rest-framework-social-oauth2](https://github.com/PhilipGarnero/django-rest-framework-social-oauth2)

The genius behind marrying `social-app-django` and `django-rest-framework`. Offers a 'convert' endpoint that turns the access token from the client into an auth with our api.

#### [django-cors-headers](https://github.com/ottoyiu/django-cors-headers)

Allows us to make requests to our API from javascript on an alternate domain
