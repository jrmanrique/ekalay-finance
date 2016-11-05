from django.conf.urls import url

from . import views

urlpatterns = [
#     /finance/
    url(r'^$', views.view, name='index'),
    url(r'^view/$', views.view, name='view'),
#     url(r'^edit/$', views.edit, name='edit'),

#     /finance/inflows
    url(r'^inflows/add/$', views.InflowCreate.as_view(), name='inflow-add'),
    url(r'^inflows/(?P<pk>\d+)/edit/$', views.InflowEdit.as_view(), name='inflow-edit'),
    url(r'^inflows/(?P<pk>\d+)/delete/$', views.InflowDelete.as_view(), name='inflow-delete'),

#     /finance/outflows
    url(r'^outflows/add/$', views.OutflowCreate.as_view(), name='outflow-add'),
    url(r'^outflows/(?P<pk>\d+)/edit/$', views.OutflowEdit.as_view(), name='outflow-edit'),
    url(r'^outflows/(?P<pk>\d+)/delete/$', views.OutflowDelete.as_view(), name='outflow-delete'),
    
#     /finance/statements/
    url(r'^statement/$', views.statement, name='statement'),
    url(r'^statement/toggle$', views.toggleMonthed, name='toggle-monthed'), # Currently not in use
 
#     /finance/admin
    url(r'^admin/$', views.FinAdmin.as_view(), name='finadmin'),
    url(r'^admin/edit/(?P<pk>\d+)$', views.FinAdminEdit.as_view(), name='finadmin-edit'),
    url(r'^admin/delete/(?P<pk>\d+)$', views.FinAdminDelete.as_view(), name='finadmin-delete'),
]
