# Generated by Django 4.0.3 on 2022-03-19 16:58

import colorfield.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Constructor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('colour', colorfield.fields.ColorField(default='#FFFFFF', image_field=None, max_length=18, samples=None)),
            ],
        ),
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('number', models.PositiveIntegerField()),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='results.constructor')),
            ],
        ),
        migrations.CreateModel(
            name='GrandPrix',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('number', models.PositiveIntegerField()),
                ('sprint_weekend', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('colour', colorfield.fields.ColorField(default='#FFFFFF', image_field=None, max_length=18, samples=None)),
            ],
        ),
        migrations.CreateModel(
            name='Prediction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_result', models.BooleanField(default=False)),
                ('by_player', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='by', to='results.player')),
                ('constructor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='constructor', to='results.constructor')),
                ('fastest_lap', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='fastest_lap', to='results.driver')),
                ('grand_prix', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grand_prix', to='results.grandprix')),
                ('p1', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='p1', to='results.driver')),
                ('p2', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='p2', to='results.driver')),
                ('p3', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='p3', to='results.driver')),
                ('pole', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='pole', to='results.driver')),
                ('sprint_p1', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sprint_p1', to='results.driver')),
                ('sprint_p2', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sprint_p2', to='results.driver')),
                ('sprint_p3', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sprint_p3', to='results.driver')),
            ],
        ),
    ]
