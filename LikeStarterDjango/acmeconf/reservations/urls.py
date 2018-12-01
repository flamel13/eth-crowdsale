from django.urls import path
from . import views
from django.conf.urls import url

from rest_framework.authtoken import views as authviews


app_name = 'reservations'

urlpatterns = [
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^register/$', views.register, name='register'),
    url(r'^(?P<event_id>[0-9]+)/reservation/$', views.reservation, name='reservation'),
    url(r'^$', views.index, name='index'),
    path('<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),
    url(r'^api-token-auth/', authviews.obtain_auth_token),
    url(r'^(?P<event_id>[0-9]+)/upload/$', views.model_form_upload, name='upload'),
    url(r'^user_reservations/$', views.user_reservations, name='user_reservations'),
    url(r'^(?P<event_id>[0-9]+)/delete_confirm/$', views.delete_reservation, name='delete_object'),
    url(r'^logout_user/$', views.logout_usr, name='logout_user'),
    url(r'^add_campaign/$', views.event_form, name='add_campaign'),
    url(r'^like/$', views.likes, name='like_url'),
    url(r'^blocktest/$', views.ethTest, name='blocktest'),
    url(r'^upwallet/$', views.update_wallet, name='upwallet'),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.MEDIA_ROOT)
