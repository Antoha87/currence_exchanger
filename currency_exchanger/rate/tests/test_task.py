import requests

from django.test import TestCase

from rate.tasks import get_latest_rates, APP_ID, get_rate
from rate.models import Rate


class TasksTest(TestCase):
    fixtures = ['currency', 'rate']

    def test_get_latest_rates(self):
        response = requests.get(f'https://openexchangerates.org/api/latest.json?app_id={APP_ID}')
        api_rate = get_rate(data=response.text, to_currency='EUR', from_currency='USD')
        
        get_latest_rates()

        db_rate = Rate.objects.get(from_currency__code='USD', to_currency__code='EUR')
        self.assertEqual(round(api_rate, 2), db_rate.rate)
