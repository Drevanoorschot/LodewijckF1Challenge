from django.shortcuts import render

# Create your views here.
from results.models import Player, Prediction, GrandPrix


def leaderboard(request):
    predictions_per_race = {}
    for gp in GrandPrix.objects.all():
        predictions_per_race.update({gp: {}})
        for player in Player.objects.all():
            if not Prediction.objects.filter(by_player=player, grand_prix=gp).exists():
                continue
            predictions_per_race[gp].update({player: Prediction.objects.get(
                by_player=player,
                grand_prix=gp
            ).total_points})
    return render(request, 'leaderboard.html', context={
        'predictions': predictions_per_race,
        'players': sorted(Player.objects.all(), key=lambda x: x.points, reverse=True),
        'grandprixs': GrandPrix.objects.all().order_by('number')
    })
