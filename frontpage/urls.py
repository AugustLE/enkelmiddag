from django.conf.urls import url, include

from . import views

app_name = 'frontpage'

urlpatterns = [

    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^rest/', include('rest.urls')),

]