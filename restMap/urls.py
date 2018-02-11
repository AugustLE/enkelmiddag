
from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

app_name = 'restMap'

urlpatterns = [

    url(r'^counties/update/rema$', views.updateRema, name='update_rema'),
    url(r'^counties/update/kiwi', views.updateKiwi, name='update_kiwi'),
    url(r'^counties/update/spar', views.updateSpar, name='update_spar'),
    url(r'^counties/update/joker', views.updateJoker, name='update_joker'),
    url(r'^counties&cities/get/all', views.CountyCityList.as_view(), name='get_all_counties&cities'),
    url(r'^counties/get/all', views.CountyList.as_view(), name='get_all_counties'),
    url(r'^stores/get/all', views.StoreList.as_view(), name='get_all_stores'),

]

urlpatterns = format_suffix_patterns(urlpatterns)