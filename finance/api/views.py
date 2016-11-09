from rest_framework import generics, permissions, status
from rest_framework.response import Response

from finance.models import AccountTypes, CashInflow, CashOutflow, ChartOfAccounts
from .serializers import CashInflowSerializer, CashInflowCreateSerializer


class CashInflowList(generics.ListAPIView):
    queryset = CashInflow.objects.all()
    serializer_class = CashInflowSerializer
    permission_classes = [permissions.IsAuthenticated]


class CashInflowCreate(generics.CreateAPIView):
    queryset = CashInflow.objects.all()
    serializer_class = CashInflowCreateSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        serializer.save()


class CashInflowDetail(generics.RetrieveAPIView):
    queryset = CashInflow.objects.all()
    serializer_class = CashInflowSerializer
    permission_classes = [permissions.IsAuthenticated]


class CashInflowUpdate(generics.RetrieveUpdateAPIView):
    queryset = CashInflow.objects.all()
    serializer_class = CashInflowSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_update(self, serializer):
        serializer.save()


class CashInflowDelete(generics.DestroyAPIView):
    queryset = CashInflow.objects.all()
    serializer_class = CashInflowSerializer
    permission_classes = [permissions.IsAdminUser]

