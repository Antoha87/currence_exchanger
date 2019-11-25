import logging
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from django.utils.encoding import force_text

logger = logging.getLogger(__name__)


class RatesViewTests(APITestCase):
    fixtures = ['currency', 'rate']

    def setUp(self):
        self.client = APIClient()

    def test_currencies_list(self):
        response = self.client.get('/api/currencies/')
        data = [{"id": 1, "code": "CZK", "name": "Czech Republic Koruna"},
                {"id": 2, "code": "EUR", "name": "Euro"},
                {"id": 3, "code": "PLN", "name": "Polish Zloty"},
                {"id": 4, "code": "UAH", "name": "Ukrainian Hryvnia"},
                {"id": 5, "code": "USD", "name": "United States Dollar"}]
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'), data)

    def test_rate_retrieve(self):
        response = self.client.get('/api/rate/', data={'from_currency': 1, 'to_currency': 1, 'amount': 1})

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'id': 1,
             'total_amount': 1,
             'rate': 1,
             'from_currency': 'CZK',
             'to_currency': 'CZK',
             })

    def test_create_all_currencies(self):
        response = self.client.get('/api/create_all_currencies/')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'),
                             {'message': 'All need currencies are created.'})

    def test_update_rates(self):
        response = self.client.get('/api/update_rates/')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'),
                             {'message': 'Rates are updated.'})
