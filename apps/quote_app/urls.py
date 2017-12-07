from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.quotes),
    url(r'^create$', views.create),
    url(r'^favorite/(?P<quote_id>\d+)$', views.favorite),
    url(r'^remove/(?P<quote_id>\d+)$', views.remove),
    url(r'^(?P<user_id>\d+)$', views.users),
    url(r'^logout$', views.logout),

]