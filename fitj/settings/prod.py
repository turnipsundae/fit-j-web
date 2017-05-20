"""
Django settings for fitj project on Heroku. Fore more info, see:
https://github.com/heroku/heroku-django-template

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

from fitj.settings.base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Allow all host headers
# ALLOWED_HOSTS = ['*']
ALLOWED_HOSTS = ['fitj.herokuapp.com', 'www.fit-j.com']

# broker url for RabbitMQ broker for Celery
app.conf.update(BROKER_URL=os.environ['CLOUDAMQP_URL'])
