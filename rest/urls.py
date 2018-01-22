from django.conf.urls import url, include

from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken import views as rest_framework_views

app_name = 'rest'

#static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = [

    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
    #url(r'^login/$', views.UserAuth.as_view()),
    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^get_auth_token/$', rest_framework_views.obtain_auth_token, name='get_auth_token'),
    url(r'^user/login/$', views.UserAuthToken.as_view(), name='login'),
    url(r'^media/imagedir/dinners/(?P<dinner_id>[0-9]+)/.*$', views.ImageDinnerView.as_view(), name='image_view'),
    url(r'^media/imagedir/weeks/(?P<week_id>[0-9]+)/.*$', views.ImageWeekView.as_view(), name='image_week_view'),
    url(r'^media/imagedir/ingredientTypes/(?P<ing_type_id>[0-9]+)/.*$', views.image_view_ing_type, name='image_view_ing_type'),
    url(r'^dinner/(?P<pk>[0-9]+)/$', views.DinnerDetail.as_view(), name='dinner'),
    url(r'^dinners/$', views.DinnerList.as_view(), name='dinners'),
    url(r'^weeks/$', views.WeekList.as_view(), name='weeks'),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


urlpatterns = format_suffix_patterns(urlpatterns)