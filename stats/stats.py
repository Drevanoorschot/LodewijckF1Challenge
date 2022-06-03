from functools import reduce

from results.models import Player, Prediction, GrandPrix


class Stat:
    def __init__(self,
                 p1, p1_points,
                 p2, p2_points,
                 p3, p3_points,
                 title):
        self.p1 = (p1, p1_points)
        self.p2 = (p2, p2_points)
        self.p3 = (p3, p3_points)
        self.title = title


def player_stats() -> list[Stat]:
    predictions = Prediction.objects.filter(is_result=False).all()
    results = Prediction.objects.filter(is_result=True).all()
    gps = GrandPrix.objects.all()
    players = Player.objects.all()
    stats = []
    # 1 most wins
    stat = dict(map(lambda p: (p, 0), players))
    for gp in gps:
        winner = sorted(predictions.filter(grand_prix=gp), key=lambda p: p.total_points, reverse=True)[0].by_player
        stat[winner] = stat[winner] + 1
    stats.append(create_stat(stat, "meeste punten"))
    # 2 most correct poles# 3 most correct p1
    # 4 most correct p2
    # 5 most correct p3
    # 6 most correct constructors
    # 7 most correct fastest laps
    # 8 most correct sprint positions
    poles = dict(map(lambda p: (p, 0), players))
    p1s = dict(map(lambda p: (p, 0), players))
    p2s = dict(map(lambda p: (p, 0), players))
    p3s = dict(map(lambda p: (p, 0), players))
    constructors = dict(map(lambda p: (p, 0), players))
    fastest_laps = dict(map(lambda p: (p, 0), players))
    sprints = dict(map(lambda p: (p, 0), players))
    for gp in gps:
        relevant = predictions.filter(grand_prix=gp).all()
        for player in players:
            if results.filter(grand_prix=gp).first().pole == relevant.filter(by_player=player).first().pole:
                poles[player] = poles[player] + 1
            if results.filter(grand_prix=gp).first().p1 == relevant.filter(by_player=player).first().p1:
                p1s[player] = p1s[player] + 1
            if results.filter(grand_prix=gp).first().p2 == relevant.filter(by_player=player).first().p2:
                p2s[player] = p2s[player] + 1
            if results.filter(grand_prix=gp).first().p3 == relevant.filter(by_player=player).first().p3:
                p3s[player] = p3s[player] + 1
            if results.filter(grand_prix=gp).first().constructor == relevant.filter(by_player=player).first().constructor:
                constructors[player] = constructors[player] + 1
            if results.filter(grand_prix=gp).first().fastest_lap == relevant.filter(by_player=player).first().fastest_lap:
                fastest_laps[player] = fastest_laps[player] + 1
            if not gp.sprint_weekend:
                continue
            if results.filter(grand_prix=gp).first().sprint_p1 == relevant.filter(by_player=player).first().sprint_p1:
                sprints[player] = sprints[player] + 1
            if results.filter(grand_prix=gp).first().sprint_p2 == relevant.filter(by_player=player).first().sprint_p2:
                sprints[player] = sprints[player] + 1
            if results.filter(grand_prix=gp).first().sprint_p3 == relevant.filter(by_player=player).first().sprint_p3:
                sprints[player] = sprints[player] + 1
    stats.append(create_stat(poles, "pole positions"))
    stats.append(create_stat(p1s, "P1s"))
    stats.append(create_stat(p2s, "P2s"))
    stats.append(create_stat(p3s, "P3s"))
    stats.append(create_stat(constructors, "constructors"))
    stats.append(create_stat(fastest_laps, "snelste rondes"))
    stats.append(create_stat(sprints, "sprint positites"))
    return stats


def create_stat(stat, title):
    stat = sorted(stat.items(), key=lambda i: i[1], reverse=True)
    return Stat(
        p1=stat[0][0], p1_points=stat[0][1],
        p2=stat[1][0], p2_points=stat[1][1],
        p3=stat[2][0], p3_points=stat[2][1],
        title=title
    )
