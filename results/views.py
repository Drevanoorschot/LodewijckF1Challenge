from difflib import SequenceMatcher

import pandas
from django.contrib.auth.decorators import login_required
from django.db.models import QuerySet
from django.shortcuts import render, redirect
# Create your views here.
from django.urls import reverse

from results.models import Player, Prediction, GrandPrix, Driver, Constructor


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
            if prediction.exists() and prediction[0].total_points is not None:
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
    predictions = Prediction.objects.filter(grand_prix=gp)
    if Prediction.objects.filter(grand_prix=gp, is_result=True).exists():
        predictions = sorted(predictions, key=lambda pred: pred.total_points, reverse=True)
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


@login_required
def upload_csv(request):
    if request.method == "GET":
        return render(request, 'csv_upload.html', context={"gps": GrandPrix.objects.all()})
    if request.method == "POST":
        grand_prix = GrandPrix.objects.get(name=request.POST['grand_prix'])
        for prediction in Prediction.objects.filter(grand_prix=grand_prix): prediction.delete()
        drivers = Driver.objects.all()
        players = Player.objects.all()
        constructors = Constructor.objects.all()
        data = pandas.read_csv(request.FILES['data'])
        for i, row in data.iterrows():
            prediction = Prediction()
            prediction.grand_prix = grand_prix
            prediction.by_player = _find_match(row['Naam'], players)
            prediction.pole = _find_match(row['Pole position'], drivers)
            prediction.p1 = _find_match(row['#1'], drivers)
            prediction.p2 = _find_match(row['#2'], drivers)
            prediction.p3 = _find_match(row['#3'], drivers)
            prediction.constructor = _find_match(row['Constructor winst'], constructors)
            prediction.fastest_lap = _find_match(row['Snelste ronde'], drivers)
            if not grand_prix.sprint_weekend:
                prediction.save()
                continue
            prediction.sprint_p1 = _find_match(row['s#1'], drivers)
            prediction.sprint_p2 = _find_match(row['s#2'], drivers)
            prediction.sprint_p3 = _find_match(row['s#3'], drivers)
            prediction.save()
        return redirect(reverse('grandprix', args=[grand_prix.id]))


def _find_match(match_string: str, objects: QuerySet, field_name='name'):
    match_string = match_string.lower()
    best = objects.first()
    best_ratio = SequenceMatcher(None, getattr(best, field_name).lower(), match_string).ratio()
    for obj in objects:
        ratio = SequenceMatcher(None, getattr(obj, field_name).lower(), match_string).ratio()
        if best_ratio > ratio:
            continue
        best = obj
        best_ratio = ratio
    return best
