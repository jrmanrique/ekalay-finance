from rest_framework import generics, status
from rest_framework.response import Response

from finance.models import AccountTypes, CashInflow, CashOutflow, ChartOfAccounts
from .serializers import CashInflowSerializer, CashInflowCreateSerializer


class CashInflowList(generics.ListAPIView):
    queryset = CashInflow.objects.all()
    serializer_class = CashInflowSerializer


class CashInflowCreate(generics.CreateAPIView):
    queryset = CashInflow.objects.all()
    serializer_class = CashInflowCreateSerializer


class CashInflowDetail(generics.RetrieveAPIView):
    queryset = CashInflow.objects.all()
    serializer_class = CashInflowSerializer


class CashInflowUpdate(generics.UpdateAPIView):
    queryset = CashInflow.objects.all()
    serializer_class = CashInflowSerializer


class CashInflowDelete(generics.DestroyAPIView):
    queryset = CashInflow.objects.all()
    serializer_class = CashInflowSerializer
