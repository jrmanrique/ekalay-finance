from django.contrib.auth.models import Group
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from finance.models import AccountTypes, CashInflow, CashOutflow, ChartOfAccounts
from .serializers import CashInflowSerializer, CashInflowCreateSerializer


# Custom Permissions


class IsSuperUser(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        else:
            return False


class IsElevatedAdminUser(permissions.BasePermission):
    users_in_group = Group.objects.get(name="Finance").user_set.all()

    def has_permission(self, request, view):
        if request.user in self.users_in_group or request.user.is_superuser:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if request.user in self.users_in_group or request.user.is_superuser:
            return True
        else:
            return False


# Views


class CashInflowList(generics.ListAPIView):
    queryset = CashInflow.objects.all()
    serializer_class = CashInflowSerializer
    permission_classes = [permissions.IsAdminUser]


class CashInflowCreate(generics.CreateAPIView):
    queryset = CashInflow.objects.all()
    serializer_class = CashInflowCreateSerializer
    permission_classes = [IsElevatedAdminUser]

    def perform_create(self, serializer):
        serializer.save()


class CashInflowDetail(generics.RetrieveAPIView):
    queryset = CashInflow.objects.all()
    serializer_class = CashInflowSerializer
    permission_classes = [permissions.IsAdminUser]


class CashInflowUpdate(generics.RetrieveUpdateAPIView):
    queryset = CashInflow.objects.all()
    serializer_class = CashInflowSerializer
    permission_classes = [IsElevatedAdminUser]

    def perform_update(self, serializer):
        serializer.save()


class CashInflowDelete(generics.DestroyAPIView):
    queryset = CashInflow.objects.all()
    serializer_class = CashInflowSerializer
    permission_classes = [IsElevatedAdminUser]
