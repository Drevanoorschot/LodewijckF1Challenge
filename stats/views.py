from django.shortcuts import render

# Create your views here.
from results.models import Prediction
from stats import stats


def stats_view(request):
    player_stats = stats.player_stats()
    result_stats = stats.result_stats()
    return render(request, 'stats.html', context={
        'player_stats': player_stats,
        'result_stats': result_stats,
        'race_count': len(Prediction.objects.filter(is_result=True))
    })
