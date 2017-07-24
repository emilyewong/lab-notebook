from django.conf.urls import url

from . import views

app_name = 'lab_notebook'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # regex for note id
    url(r'^(?P<lab_note_id>[0-9]+)/detail/$', views.detail, name='detail'),
    url(r'^record/$', views.record, name='record'),
    url(r'^save/$', views.save, name='save'),
]