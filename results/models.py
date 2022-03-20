from django.db import models


# Create your models here.
class Constructor(models.Model):
    name = models.CharField(max_length=100)
    colour = models.CharField(max_length=7)

    def __str__(self):
        return self.name


class Driver(models.Model):
    name = models.CharField(max_length=100)
    number = models.PositiveIntegerField()
    team = models.ForeignKey(Constructor, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.name} ({self.number})"


class Player(models.Model):
    name = models.CharField(max_length=100)
    colour = models.CharField(max_length=7)

    @property
    def points(self):
        return sum(map(lambda pred: pred.total_points, Prediction.objects.filter(by_player=self)))

    def __str__(self):
        return self.name


class GrandPrix(models.Model):
    name = models.CharField(max_length=100)
    number = models.PositiveIntegerField()
    sprint_weekend = models.BooleanField()
    logo = models.CharField(max_length=5)

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
        return sum(self.total_points_dict.values())

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
        result = Prediction.objects.get(is_result=True, grand_prix=self.grand_prix)
        if self.pole == result.pole:
            points['pole'] = 5
        result_top3 = [result.p1, result.p2, result.p3]
        pred_top3 = [self.p1, self.p2, self.p3]
        for i in range(0, len(result_top3)):
            if result_top3[i] == pred_top3[i]:
                points[f"p{i}"] = 3
            elif result_top3[i] in pred_top3:
                points[f"p{i}"] = 1
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
                points[f"sp{i}"] = 1
        return points

    class Meta:
        unique_together = [['by_player', 'grand_prix']]
