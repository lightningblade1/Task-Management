# Install celery
    pip install celery
#Install RabbitMQ

# Run Celery
    celery -A Task_management worker -l info --pool=solo
#'Task management' is the app name change accordingly

# Run RabbitMQ
Run:
C:\Program Files\RabbitMQ Server\rabbitmq_server-3.8.6\sbin\rabbitmq-server.bat

Now we use Flower
#####
#Go to
C:\django\yt-django-celery-series-intro-install-run-task\venv\lib\site-packages\tornado\platform\asyncio.py

#and add this code:
import sys

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

To run flower :
celery -A Task_management flower -l info --pool=solo

Now we use django celery beat
#####
pip install django-celery-beat
 add django-celery-beat as an installed app in settings file

#migrate using
python manage.py migrate

#now go to admin and see if you can add periodic tasks.
#if your addition task is not shown in admin page,
#add these in the root   __init__.py   file

from __future__ import absolute_import, unicode_literals

from .celery import app as celery_app

__all__=('celery_app',)
