from django.shortcuts import render

# Create your views here.
from results.models import Player, Prediction, GrandPrix


def leaderboard(request):
    return render(request, 'leaderboard.html', context={
        'leaderboard': _make_leaderboard(),
        'players': sorted(Player.objects.all(), key=lambda x: x.points, reverse=True),
        'grandprixs': GrandPrix.objects.all().order_by('number'),
        'chart': _make_chart(),
    })


def _make_leaderboard():
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
    return predictions_per_race


def _make_chart():
    chart = {}
    chart.update({
        'labels': list(map(lambda gp: gp.logo, GrandPrix.objects.all())),
        'scores': {}
    })
    for player in Player.objects.all():
        score = []
        for gp in GrandPrix.objects.all().order_by('number'):
            prediction = Prediction.objects.filter(by_player=player, grand_prix=gp)
            if prediction.exists():
                if len(score) == 0:
                    score.append(prediction[0].total_points)
                else:
                    score.append(prediction[0].total_points + score[-1])
            else:
                if len(score) == 0:
                    score.append(0)
                else:
                    score.append(score[-1])
        chart['scores'].update({
            player: score
        })
    return chart


def player_view(request, p_id):
    player = Player.objects.get(id=p_id)
    return render(request, 'player.html', context={
        'player': player,
        'predictions': Prediction.objects.filter(by_player=player)
    })


def grandprix_view(request, gp_id):
    gp = GrandPrix.objects.get(id=gp_id)
    predictions = sorted(Prediction.objects.filter(grand_prix=gp), key=lambda pred: pred.total_points, reverse=True)
    return render(request, 'grandprix.html', context={
        'grandprix': gp,
        'predictions': predictions,
        'result_exists': Prediction.objects.filter(grand_prix=gp, is_result=True)
    })


def gps_view(request):
    return render(request, 'gps.html', context={
        'gps': GrandPrix.objects.all()
    })


def players_view(request):
    return render(request, 'players.html', context={
        'players': Player.objects.all().order_by('name')
    })



