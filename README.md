# Wolnowarze - Backend

# [Live demo](https://wolnowarze.grykom.pl/)
# [API demo](https://api.wolnowarze.grykom.pl/)

## Wolnowarze project 
#### [_] [Frontend React.js](https://github.com/grykom/wolnowarze_frontend)
#### [x] [Backend Django-Python](https://github.com/grykom/wolnowarze_backend)
#### [_] [Backend API docs React.js (optional)](https://github.com/grykom/wolnowarze_api_docs)


## About
Django backend for Wolnowarze project. 

## How to
- Pull this repo and install requirements
``` 
git pull https://github.com/grykom/wolnowarze_backend.git
pip install -r requirements.txt
```
- create ```/wolnowarze/local_settings.py``` file and modify the settings
- run database things:
```
python manage.py makemigrations api
python manage.py migrate
```
- create an administrator account (```python manage.py createsuperuser```) and log in (```/admin```), then add some posts in WhySlowcooker
- Visit ```/api/cron/pull-data``` wait and refresh it a few times. You can also add this to cron once a day
- (optional) if you want [API docs](https://github.com/grykom/wolnowarze_api_docs), copy ```index.html``` to ```/api/templates/api/``` and rest files (logo, maniest, css) to ```/public/```

## Sample local_settings.py
```
from .settings import *

// how many recipes should be fetched at once
CRON_FETCH_LIMIT = 10

// change IP to your backend web address and add domain/IP to allowed hosts
SITE_URL = "http://127.0.0.1:8000"
ALLOWED_HOSTS = ['127.0.0.1']

// A secret key for a Django installation, change it to a unique value 
SECRET_KEY = "secret_key"

// other
DEBUG = False
CORS_ALLOW_ALL_ORIGINS = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}
```

## TestCase
```
python manage.py test
```
```
.................................
----------------------------------------------------------------------
Ran 35 tests in 3.644s

OK
Destroying test database for alias 'default'...
```