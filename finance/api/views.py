from django.contrib.auth.models import Group
from django.db.models import Q
from rest_framework import generics, permissions
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination

from finance.models import AccountTypes, CashInflow, CashOutflow, ChartOfAccounts
from .serializers import CashInflowSerializer, CashInflowCreateSerializer, CashInflowEditSerializer


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


# Custom Pagination


class FlowPageNumberPagination(PageNumberPagination):
    page_size = 3


# Views


class CashInflowList(generics.ListAPIView):
    serializer_class = CashInflowSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['ref_num', 'account_title', 'flow_type', 'payor', 'document', 'notes']
    pagination_class = FlowPageNumberPagination

    def get_queryset(self, *args, **kwargs):
        queryset_list = CashInflow.objects.all()
        query = self.request.GET.get("q")
        if query:
            try:
                int(query)
                queryset_list = queryset_list.filter(
                    Q(ref_num__exact = query)
                ).distinct()
            except ValueError:
                queryset_list = queryset_list.filter(
                    Q(account_title__icontains = query) |
                    Q(flow_type__icontains = query) |
                    Q(payor__icontains = query) |
                    Q(document__icontains = query) |
                    Q(notes__icontains = query)
                ).distinct()
        return queryset_list


class CashInflowCreate(generics.CreateAPIView):
    queryset = CashInflow.objects.all()
    serializer_class = CashInflowCreateSerializer
    permission_classes = [IsElevatedAdminUser]

    def perform_create(self, serializer):
        serializer.save()


class CashInflowEdit(generics.RetrieveAPIView):
    queryset = CashInflow.objects.all()
    serializer_class = CashInflowEditSerializer
    permission_classes = [IsElevatedAdminUser]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
