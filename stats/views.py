from django.shortcuts import render

# Create your views here.
from stats import stats


def stats_view(request):
    player_stats = stats.player_stats()
    return render(request, 'stats.html', context={'player_stats':player_stats})
