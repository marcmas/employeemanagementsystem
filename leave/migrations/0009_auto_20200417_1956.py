# Generated by Django 3.0.4 on 2020-04-17 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0008_auto_20200417_1351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leavenotificationemployee',
            name='date_read',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='leavenotificationemployee',
            name='status',
            field=models.CharField(choices=[('Add', 'Add'), ('Add Employee', 'Add Employee'), ('Accept Employee', 'Accept Employee'), ('Reject Employee', 'Reject Employee')], max_length=100, null=True),
        ),
    ]
