# Generated by Django 4.0.3 on 2022-03-20 23:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0005_driver_short'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driver',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='team', to='results.constructor'),
        ),
    ]
