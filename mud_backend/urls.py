from django.conf.urls import url

from . import views
from . import actions

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^actions$', actions.index, name='actions'),
]
