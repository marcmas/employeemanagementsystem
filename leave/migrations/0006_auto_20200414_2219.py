# Generated by Django 3.0.4 on 2020-04-14 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0005_rejectleave'),
    ]

    operations = [
        migrations.AddField(
            model_name='vacationlimit',
            name='children_days_constant',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='vacationlimit',
            name='normal_days_constant',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='vacationlimit',
            name='request_days_constant',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
