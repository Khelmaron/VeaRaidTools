"""VeaRaidOrganizer URL Configuration

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
from django.urls import path
from django.conf.urls import url
from Spielerverwaltung.views import (homeView,
                                    playeroverView,
                                    charoverView,
                                    RaidoverView,
                                    RaidDetailView,
                                    PlayerViewSet,
                                    PlayerDetailView,
#                                    ScheduledRaids,
                                    scheduled_raids,
                                    Raidcreation,
                                    RaidCreate)
from django_filters.views import FilterView
from Spielerverwaltung.models import Raid
from Spielerverwaltung import views


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', homeView.as_view()),
    url(r'^Charakteruebersicht/', charoverView.as_view(), name = 'Charakteruebersicht'),
    url(r'^Spieleruebersicht/', playeroverView.as_view(), name = 'Spieleruebersicht'),
    url(r'^Raiduebersicht/', RaidoverView.as_view(), name = 'raid_overview'),
    url(r'^Raiddetail/(?P<pk>\d+)/$', RaidDetailView.as_view(), name = 'raid_details'),
    url(r'^api/', PlayerViewSet.as_view({'get' : 'getPlayers'})), #  include('rest_framework.urls', namespace='rest_framework'))
    url(r'^Playerdetail/(?P<pk>[-\w]+)/$', PlayerDetailView.as_view(), name = 'player_details'),
    url(r'^Raidschedule/', views.scheduled_raids, name = 'raid_schedule'),
    url(r'^CreateRaid/', Raidcreation.as_view(), name = 'create_raid'),
    url(r'^RaidCreator/', RaidCreate.as_view(), name = 'createraid')
]
