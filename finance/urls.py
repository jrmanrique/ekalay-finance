from django.conf.urls import url

from . import views

urlpatterns = [
#     /finance/
    url(r'^$', views.index, name='index'),
    url(r'^view/$', views.index, name='view'),
    url(r'^add/$', views.FlowAdd.as_view(), name='add'),

#     /finance/inflows/
    url(r'^inflows/edit/(?P<pk>\d+)/(?P<slug>[-\w]*)/$', views.InflowEdit.as_view(), name='inflow-edit'),
    url(r'^inflows/delete/(?P<pk>\d+)/(?P<slug>[-\w]*)/$', views.inflow_delete, name='inflow-delete'),

#     /finance/outflows/
    url(r'^outflows/edit/(?P<pk>\d+)/(?P<slug>[-\w]*)/$', views.OutflowEdit.as_view(), name='outflow-edit'),
    url(r'^outflows/delete/(?P<pk>\d+)/(?P<slug>[-\w]*)/$', views.outflow_delete, name='outflow-delete'),

#     /finance/statements/
    url(r'^statement/$', views.statement, name='statement'),
    url(r'^statement/toggle$', views.statement_toggle_view, name='toggle-monthed'), # Currently not in use

#     /finance/admin/
    url(r'^admin/$', views.FinAdmin.as_view(), name='finadmin'),
    url(r'^admin/edit/(?P<pk>\d+)/(?P<ref_num>\d+)$', views.FinAdminEdit.as_view(), name='finadmin-edit'),
    url(r'^admin/delete/(?P<pk>\d+)/(?P<ref_num>\d+)$', views.FinAdminDelete.as_view(), name='finadmin-delete'),
]
