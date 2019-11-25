from django.db import models


class Currency(models.Model):
    code = models.CharField('Code', max_length=3, unique=True)
    name = models.CharField('Name', max_length=40, null=True, blank=True)

    class Meta:
        verbose_name = 'Currency'
        verbose_name_plural = 'Currencies'
        ordering = ('name',)

    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        new_currency = False
        if not self.pk:
            new_currency = True
        super().save(*args, **kwargs)

        if new_currency:
            Rate.objects.create_currency_rates(self)


class RateManager(models.Manager):
    def create_currency_rates(self, new_currency):
        new_rates = list()
        new_rates.append(self.model(from_currency=new_currency, to_currency=new_currency, rate=1))

        for currency in Currency.objects.all():
            if currency != new_currency:
                new_rates.append(self.model(from_currency=new_currency, to_currency=currency, rate=0))
                new_rates.append(self.model(from_currency=currency, to_currency=new_currency, rate=0))

        self.model.objects.bulk_create(new_rates)


class Rate(models.Model):
    from_currency = models.ForeignKey(Currency, on_delete=models.CASCADE,
                                      verbose_name='From currency', related_name='rates_from')
    to_currency = models.ForeignKey(Currency, on_delete=models.CASCADE,
                                    verbose_name='To currency', related_name='rates_to')
    rate = models.FloatField('Rate')
    created = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    objects = RateManager()

    class Meta:
        verbose_name = 'Rate'
        verbose_name_plural = 'Rates'
        #unique_together = ('from_currency', 'to_currency')
        ordering = ('created',)

    def __str__(self):
        return f"Rate from {self.from_currency} to {self.to_currency} is {self.rate}"

    def calculate_amount(self, amount):
        return self.rate * amount
