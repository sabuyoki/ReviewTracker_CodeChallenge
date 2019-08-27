from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.create_list),
    url(r'^create_list/$', views.create_list),
]