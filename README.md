# Shakespeare-backend

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
└── shakespeare-project
    ├── manage.py
    ├── personas
    ├── shakespeare
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
CREATE DATABASE myproject;
```

2) Create a db new user

```
CREATE USER shakespeare-admin WITH PASSWORD 'salesforce1';
```

## Elastic Beanstalk Deploys

Make sure that whatever elastic beanstalk url is generated, is put into the `shakespeare.settings` `ALLOWED_HOSTS`

```eb deploy```