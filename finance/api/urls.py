from django.conf.urls import url

from . import views

urlpatterns = [
    # api/finance/
    # url(r'^$', views.CashInflowList.as_view(), name='inflow-list'),

    # api/finance/inflows
    url(r'^inflows/$', views.CashInflowList.as_view(), name='inflow-list'),
    url(r'^inflows/create/$', views.CashInflowCreate.as_view(), name='inflow-create'),
    url(r'^inflows/(?P<pk>\d+)/$', views.CashInflowDetail.as_view(), name='inflow-detail'),
    url(r'^inflows/(?P<pk>\d+)/update/$', views.CashInflowUpdate.as_view(), name='inflow-update'),
    url(r'^inflows/(?P<pk>\d+)/delete/$', views.CashInflowDelete.as_view(), name='inflow-delete'),
]
