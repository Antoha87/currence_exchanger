import json
import requests
import logging

from celery import shared_task
from currency_exchanger.celery import app as celery_app

from django_bulk_update.helper import bulk_update

from .models import Currency, Rate
from django.conf import settings


logger = logging.getLogger(__name__)

APP_ID = settings.APP_ID
CURRENCIES_LIST = settings.CURRENCIES_LIST


def get_rate(data, from_currency, to_currency):
    data = json.loads(data)
    return round(data['rates'][to_currency] / data['rates'][from_currency], 2)


@celery_app.task(name="get all need currencies")
def get_all_currencies():
    logger.info("RUN CELERY TASK - Get all need currencies from openexchangerates.org")
    response = requests.get('https://openexchangerates.org/api/currencies.json')
    if response.ok:
        data = json.loads(response.text)
        for code, name in data.items():
            if code in CURRENCIES_LIST:
                Currency.objects.get_or_create(code=code, name=name)
                logger.info("OK")
    else:
        logger.critical('No response data from openexchangerates.org! Please try later!')


@shared_task(name="get latest exchange rates")
def get_latest_rates():
    logger.info("RUN CELERY TASK - Get latest exchange rates from openexchangerates.org")
    response = requests.get(f'https://openexchangerates.org/api/latest.json?app_id={APP_ID}')
    if response.ok:
        rates = Rate.objects.select_related('from_currency').select_related('to_currency').all()
        for rate in rates:
            rate.rate = get_rate(response.text, rate.from_currency.code, rate.to_currency.code)
        bulk_update(rates, update_fields=['rate'])
        logger.info("OK")
    else:
        logger.critical('No response data from openexchangerates.org! Please try later!')

