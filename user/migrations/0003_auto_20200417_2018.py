# Generated by Django 3.0.4 on 2020-04-17 18:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20200417_2016'),
    ]

    operations = [
        migrations.RenameField(
            model_name='section',
            old_name='section',
            new_name='name',
        ),
    ]
