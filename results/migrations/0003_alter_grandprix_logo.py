# Generated by Django 4.0.3 on 2022-03-20 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0002_grandprix_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grandprix',
            name='logo',
            field=models.CharField(max_length=5),
        ),
    ]