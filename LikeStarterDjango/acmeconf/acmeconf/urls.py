"""acmeconf URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from django.conf.urls import url, include
from django.contrib.auth.models import User
from reservations.models import Event, EventReservation
from rest_framework import routers, serializers, viewsets
from rest_framework.routers import DefaultRouter
from rest_framework.response import Response
from rest_framework.serializers import HyperlinkedModelSerializer
from django.shortcuts import get_object_or_404
from rest_framework_extensions.mixins import NestedViewSetMixin
from rest_framework_extensions.routers import NestedRouterMixin

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class EventSerializer(serializers.HyperlinkedModelSerializer):
    dates = serializers.JSONField(required=False)
    class Meta:
        model = Event
        fields = ('id', 'name', 'dates', 'subsStart', 'contDeadline', 'subsDeadline', 'city', 'address', 'cap', 'location', 'max_seats', 'available_seats', 'date', 'ticket_price', 'staff_ticket_price', 'available_money', 'is_open', 'is_open_contr')

# Serializers define the API representation.
class UserReservationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EventReservation
        fields = ('id', 'event', 'user', 'is_staff', 'bank_user')

# ViewSets define the view behavior.
class UserViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# ViewSets define the view behavior.
class EventViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

# ViewSets define the view behavior.
class UserReservationViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = EventReservation.objects.all()
    serializer_class = UserReservationSerializer

class NestedDefaultRouter(NestedRouterMixin, DefaultRouter):
    pass

router = NestedDefaultRouter()

events_router = router.register('event_reservations', UserReservationViewSet)
events_router = router.register('users', UserViewSet)
events_router = router.register('events', EventViewSet)

#nested_links
events_router.register(
    'user_reservations', UserReservationViewSet,
    base_name='booking',
    parents_query_lookups=['event'])


urlpatterns = [
    path('reservations/', include('reservations.urls')),
    path('admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
