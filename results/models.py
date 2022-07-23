import numpy
import pandas

from django.db import models

# Create your models here.
from scipy import stats


class Nationality(models.Model):
    name = models.CharField(max_length=50)
    flag = models.CharField(max_length=5)

    def __str__(self):
        return f"{self.flag} {self.name}"


class Constructor(models.Model):
    name = models.CharField(max_length=100)
    colour = models.CharField(max_length=7)
    nationality = models.ForeignKey(Nationality, on_delete=models.PROTECT, related_name='country', null=True)

    def __str__(self):
        return self.name


class Driver(models.Model):
    name = models.CharField(max_length=100)
    number = models.PositiveIntegerField()
    team = models.ForeignKey(Constructor, on_delete=models.PROTECT, related_name='team')
    short = models.CharField(max_length=3)
    nationality = models.ForeignKey(Nationality, on_delete=models.PROTECT, related_name='nationality', null=True)

    @property
    def colour(self):
        return self.team.colour

    def __str__(self):
        return f"{self.name} ({self.number})"


class Player(models.Model):
    name = models.CharField(max_length=100)
    colour = models.CharField(max_length=7)

    @property
    def points(self):
        completed_gps = set(map(lambda pred: pred.grand_prix, Prediction.objects.filter(is_result=True)))
        return sum(map(lambda pred: pred.total_points,
                       Prediction.objects.filter(by_player=self, grand_prix__in=completed_gps)))

    @property
    def points_mean(self):
        completed_gps = set(map(lambda pred: pred.grand_prix, Prediction.objects.filter(is_result=True)))
        return numpy.mean(list(map(lambda pred: pred.total_points,
                                   Prediction.objects.filter(by_player=self, grand_prix__in=completed_gps))))

    @property
    def points_std_dev(self):
        completed_gps = set(map(lambda pred: pred.grand_prix, Prediction.objects.filter(is_result=True)))
        return numpy.std(list(map(lambda pred: pred.total_points,
                                  Prediction.objects.filter(by_player=self, grand_prix__in=completed_gps))))

    @property
    def points_dict(self):
        predictions = Prediction.objects.filter(by_player=self)
        return {
            'pole': sum(map(lambda pred: pred.total_points_dict.get('pole'), predictions)),
            'p1': sum(map(lambda pred: pred.total_points_dict.get('p1'), predictions)),
            'p2': sum(map(lambda pred: pred.total_points_dict.get('p2'), predictions)),
            'p3': sum(map(lambda pred: pred.total_points_dict.get('p1'), predictions)),
            'constructor': sum(map(lambda pred: pred.total_points_dict.get('constructor'), predictions)),
            'fastest_lap': sum(map(lambda pred: pred.total_points_dict.get('fastest_lap'), predictions)),
            'sp1': sum(map(lambda pred: pred.total_points_dict.get('sp1') if pred.total_points_dict.get(
                'sp1') is not None else 0, predictions)),
            'sp2': sum(map(lambda pred: pred.total_points_dict.get('sp2') if pred.total_points_dict.get(
                'sp2') is not None else 0, predictions)),
            'sp3': sum(map(lambda pred: pred.total_points_dict.get('sp3') if pred.total_points_dict.get(
                'sp3') is not None else 0, predictions)),
        }

    def __str__(self):
        return self.name


class GrandPrix(models.Model):
    name = models.CharField(max_length=100)
    number = models.PositiveIntegerField()
    sprint_weekend = models.BooleanField()
    logo = models.CharField(max_length=5)

    @property
    def vote_entropy(self):
        predictions = Prediction.objects.filter(grand_prix=self, is_result=False)
        if not predictions.exists():
            return {"empty": 0}
        cols = ['pole_id',
                'p1_id',
                'p2_id',
                'p3_id',
                'constructor_id',
                'fastest_lap_id',
                'sprint_p1_id',
                'sprint_p2_id',
                'sprint_p3_id']
        predictions = pandas.DataFrame.from_records(
            predictions.values())
        entropy_dict = {}
        for col in cols:
            entropy = stats.entropy(pandas.Series(data=predictions[col]).value_counts())
            entropy_dict.update({col.replace("_id", ""): entropy})
        return entropy_dict

    @property
    def total_vote_entropy(self):
        return numpy.mean(list(self.vote_entropy.values()))

    def __str__(self):
        return f"{self.logo} {self.name}"


class Prediction(models.Model):
    by_player = models.ForeignKey(Player, on_delete=models.PROTECT, blank=True, null=True, related_name='by')
    is_result = models.BooleanField(default=False)
    grand_prix = models.ForeignKey(GrandPrix, on_delete=models.CASCADE, related_name='grand_prix')
    pole = models.ForeignKey(Driver, on_delete=models.PROTECT, related_name='pole')
    p1 = models.ForeignKey(Driver, on_delete=models.PROTECT, related_name='p1')
    p2 = models.ForeignKey(Driver, on_delete=models.PROTECT, related_name='p2')
    p3 = models.ForeignKey(Driver, on_delete=models.PROTECT, related_name='p3')
    constructor = models.ForeignKey(Constructor, on_delete=models.PROTECT, related_name='constructor')
    fastest_lap = models.ForeignKey(Driver, on_delete=models.PROTECT, related_name='fastest_lap', blank=True, null=True)
    sprint_p1 = models.ForeignKey(Driver, on_delete=models.PROTECT, related_name='sprint_p1', blank=True, null=True)
    sprint_p2 = models.ForeignKey(Driver, on_delete=models.PROTECT, related_name='sprint_p2', blank=True, null=True)
    sprint_p3 = models.ForeignKey(Driver, on_delete=models.PROTECT, related_name='sprint_p3', blank=True, null=True)

    def __str__(self):
        if self.is_result:
            return f"{self.grand_prix} Result".upper()
        else:
            return f"{self.grand_prix} prediction by {self.by_player}"

    @property
    def total_points(self):
        return None if not Prediction.objects.filter(is_result=True, grand_prix=self.grand_prix).exists() else sum(
            self.total_points_dict.values())

    @property
    def total_points_dict(self):
        points = {
            "pole": 0,
            "p1": 0,
            "p2": 0,
            "p3": 0,
            "constructor": 0,
            "fastest_lap": 0,
        }
        if self.grand_prix.sprint_weekend:
            points.update({
                "sp1": 0,
                "sp2": 0,
                "sp3": 0
            })
        results = Prediction.objects.filter(is_result=True, grand_prix=self.grand_prix)
        if not results.exists():
            return points
        result = results[0]
        if self.pole == result.pole:
            points['pole'] = 5
        result_top3 = [result.p1, result.p2, result.p3]
        pred_top3 = [self.p1, self.p2, self.p3]
        for i in range(0, len(result_top3)):
            if result_top3[i] == pred_top3[i]:
                points[f"p{i + 1}"] = 3
            elif pred_top3[i] in result_top3:
                points[f"p{i + 1}"] = 1
        if self.constructor == result.constructor:
            points['constructor'] = 5
        if self.fastest_lap == result.fastest_lap:
            points['fastest_lap'] = 3
        if not self.grand_prix.sprint_weekend:
            return points
        result_top3s = [result.sprint_p1, result.sprint_p2, result.sprint_p3]
        pred_top3s = [self.sprint_p1, self.sprint_p2, self.sprint_p3]
        for i in range(0, len(result_top3)):
            if result_top3s[i] == pred_top3s[i]:
                points[f"sp{i + 1}"] = 1
        return points

    class Meta:
        unique_together = [['by_player', 'grand_prix']]
