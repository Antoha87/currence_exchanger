from django.http import JsonResponse

from rest_framework import generics, status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Currency, Rate
from .tasks import get_latest_rates, get_all_currencies
from .serializers import CurrencySerializer, RateSerializer, RateListSerializer


class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


class RateListApiView(generics.ListCreateAPIView):
    queryset = Rate.objects.all()
    serializer_class = RateListSerializer


class RateRetrieveApiView(APIView):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer

    def get(self, request):
        serializer = RateSerializer(data=request.GET)
        if serializer.is_valid():
            rate = Rate.objects.filter(from_currency=serializer.validated_data['from_currency'],
                                       to_currency=serializer.validated_data['to_currency']).first()
            print(rate)
            amount = rate.calculate_amount(serializer.validated_data['amount'])
            data = {
                'id': rate.pk,
                'from_currency': rate.from_currency.code,
                'to_currency': rate.to_currency.code,
                'rate': rate.rate,
                'total_amount': amount
            }

            return JsonResponse(data)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def update_rates_now(request):
    get_latest_rates.delay()
    return JsonResponse({'message': 'Rates are updated.'})


@api_view(['GET'])
def create_all_currencies(request):
    get_all_currencies.delay()
    return JsonResponse({'message': 'All need currencies are created.'})
