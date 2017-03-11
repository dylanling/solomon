from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^crawl_author$', views.crawl_author, name='crawl_author'),
]