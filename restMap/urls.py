
from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

app_name = 'restMap'

urlpatterns = [

    url(r'^counties/update/rema$', views.updateRema, name='update_rema'),
    url(r'^counties/update/kiwi', views.updateKiwi, name='update_kiwi'),
    url(r'^counties/update/spar', views.updateSpar, name='update_spar'),
    url(r'^counties/update/joker', views.updateJoker, name='update_joker'),
]

urlpatterns = format_suffix_patterns(urlpatterns)