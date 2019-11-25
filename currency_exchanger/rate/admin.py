from django.contrib import admin
from .models import Currency, Rate


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'name')


@admin.register(Rate)
class RateAdmin(admin.ModelAdmin):
    list_display = ('from_currency', 'to_currency', 'rate', 'created', 'last_update')
    list_filter = ('from_currency',)


