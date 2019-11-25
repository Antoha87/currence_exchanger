from django.test import TestCase

from rate.models import Currency, Rate


class ModelsTest(TestCase):
    fixtures = ['currency', 'rate']

    def test_rate_calculate_amout(self):
        rate = Rate.objects.all().first()
        total_amount = rate.calculate_amount(5)        

        self.assertEqual(rate.rate, 1)
        self.assertEqual(total_amount, 5)
        self.assertIsInstance(total_amount, float)

    def test_currency_save(self):

        new_currency = Currency.objects.create(code="RUB", name="Russian Ruble")
        
        new_rates_master_count = Rate.objects.filter(from_currency=new_currency).count()

        self.assertEqual(new_rates_master_count, 6)

        new_rates_slave_count = Rate.objects.filter(to_currency=new_currency).count()
        self.assertEqual(new_rates_slave_count, 6)
