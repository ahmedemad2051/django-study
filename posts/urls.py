from django.conf.urls import url
from . import views

app_name='posts'

urlpatterns=[
    url(r'^$',views.index,name='index'),
    url(r'^(?P<pk>\d+)/$',views.detail,name='detail'),
    url(r'^create/$',views.create,name='create'),
    url(r'^(?P<pk>\d+)/edit/$',views.edit,name='edit'),
    url(r'^(?P<pk>\d+)/delete/$',views.delete,name='delete'),

]