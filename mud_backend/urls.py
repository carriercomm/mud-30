from django.conf.urls import url

from . import actions

urlpatterns = [
    url(r'^actions$', actions.index, name='index'),
]
