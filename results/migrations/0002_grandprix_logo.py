# Generated by Django 4.0.3 on 2022-03-20 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='grandprix',
            name='logo',
            field=models.CharField(default='.', max_length=1),
            preserve_default=False,
        ),
    ]
