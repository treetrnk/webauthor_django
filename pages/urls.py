from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^.*$', views.page, name='page'),
    url(r'^(?:home)||$', views.page, name='home'),
]

