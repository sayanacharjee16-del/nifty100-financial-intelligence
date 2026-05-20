import os
import ssl
from celery import Celery

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'b100_intelligence.settings')

app = Celery('b100_intelligence')

UPSTASH_URL = os.getenv('UPSTASH_REDIS_URL')
app.conf.broker_url = UPSTASH_URL
app.conf.result_backend = UPSTASH_URL
app.conf.broker_use_ssl = {'ssl_cert_reqs': ssl.CERT_NONE}
app.conf.redis_backend_use_ssl = {'ssl_cert_reqs': ssl.CERT_NONE}
# ----------------------------------------

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')