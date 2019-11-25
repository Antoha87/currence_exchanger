from django.test import TestCase

from rate.models import Rate, Currency


class ManagersTest(TestCase):
    fixtures = ['currency', 'rate']

    def test_rate_Manager_create_currency_rates(self):

        Currency.objects.bulk_create([Currency(code="RUB", name="Russian Ruble")])

        new_currency = Currency.objects.get(code="RUB", name="Russian Ruble")

        Rate.objects.create_currency_rates(new_currency)

        new_rates_from_count = Rate.objects.filter(from_currency=new_currency).count()

        self.assertEqual(new_rates_from_count, 6)

        new_rates_to_count = Rate.objects.filter(to_currency=new_currency).count()
        self.assertEqual(new_rates_to_count, 6)
