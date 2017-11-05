from django.conf.urls import url 
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^dashboard$', views.dashboard),
    url(r'^success$', views.success),
    url(r'^addquote$', views.addquote),
    url(r'^favorite/(?P<quote_id>\d+)$', views.favorite),
    url(r'^remove/(?P<quote_id>\d+)$', views.remove),
    url(r'^userpage/(?P<id>\d+)$', views.userpage)
]