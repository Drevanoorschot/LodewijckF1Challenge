from colorfield.fields import ColorField
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

    def __str__(self):
        return self.name


class GrandPrix(models.Model):
    name = models.CharField(max_length=100)
    number = models.PositiveIntegerField()
    sprint_weekend = models.BooleanField()

    def __str__(self):
        return self.name


class Prediction(models.Model):
    by_player = models.ForeignKey(Player, on_delete=models.PROTECT, blank=True, null=True, related_name='by')
    is_result = models.BooleanField(default=False)
    grand_prix = models.ForeignKey(GrandPrix, on_delete=models.CASCADE, related_name='grand_prix')
    pole = models.ForeignKey(Driver, on_delete=models.PROTECT, related_name='pole')
    p1 = models.ForeignKey(Driver, on_delete=models.PROTECT, related_name='p1')
    p2 = models.ForeignKey(Driver, on_delete=models.PROTECT, related_name='p2')
    p3 = models.ForeignKey(Driver, on_delete=models.PROTECT, related_name='p3')
    constructor = models.ForeignKey(Constructor, on_delete=models.PROTECT, related_name='constructor')
    fastest_lap = models.ForeignKey(Driver, on_delete=models.PROTECT, related_name='fastest_lap')
    sprint_p1 = models.ForeignKey(Driver, on_delete=models.PROTECT, related_name='sprint_p1', blank=True, null=True)
    sprint_p2 = models.ForeignKey(Driver, on_delete=models.PROTECT, related_name='sprint_p2', blank=True, null=True)
    sprint_p3 = models.ForeignKey(Driver, on_delete=models.PROTECT, related_name='sprint_p3', blank=True, null=True)

    def __str__(self):
        return f"{self.grand_prix} prediction by {self.by_player}"

    class Meta:
        unique_together = [['by_player', 'grand_prix']]
