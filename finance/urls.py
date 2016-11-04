from django.conf.urls import url

from . import views

urlpatterns = [
#     /finance/
#     url(r'^$', views.index, name='index'),
    url(r'^$', views.view, name='index'),
    url(r'^view/$', views.view, name='view'),
#     url(r'^edit/$', views.edit, name='edit'),
    url(r'^statement/$', views.statement, name='statement'),
    url(r'^finadmin/$', views.finAdmin, name='finadmin'),

#     /finance/inflows
#     url(r'^inflows/$', views.inflows, name='inflows'),
    url(r'^inflows/add/$', views.InflowCreate.as_view(), name='inflow-add'),
    url(r'^inflows/(?P<pk>\d+)/edit/$', views.InflowEdit.as_view(), name='inflow-edit'),
    url(r'^inflows/(?P<pk>\d+)/delete/$', views.InflowDelete.as_view(), name='inflow-delete'),

#     /finance/outflows
#     url(r'^outflows/$', views.outflows, name='outflows'),
    url(r'^outflows/add/$', views.OutflowCreate.as_view(), name='outflow-add'),
    url(r'^outflows/(?P<pk>\d+)/edit/$', views.OutflowEdit.as_view(), name='outflow-edit'),
    url(r'^outflows/(?P<pk>\d+)/delete/$', views.OutflowDelete.as_view(), name='outflow-delete'),

#     /finance/accounts
    url(r'^accounts/add/$', views.AccountCreate.as_view(), name='account-add'),
    url(r'^accounts/(?P<pk>\d+)/edit/$', views.AccountEdit.as_view(), name='account-edit'),
    url(r'^accounts/(?P<pk>\d+)/delete/$', views.AccountDelete.as_view(), name='account-delete'),
]
