from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name="news_index"),
	url(r'^fetch$', views.fetch, name="news_fetch"),
]