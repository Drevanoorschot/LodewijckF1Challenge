"""F1Challenge URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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

import results
from F1Challenge import views
from results import views as result_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.landing_page, name='home'),
    path('leaderboard', result_views.leaderboard, name='leaderboard'),
    path('player/<int:p_id>', result_views.player_view, name='player'),
    path('players', result_views.players_view, name='players'),
    path('gp/<int:gp_id>', result_views.grandprix_view, name='grandprix'),
    path('gps', result_views.gps_view, name='gps'),
    path('stats', result_views.stats_view, name='stats')
]
