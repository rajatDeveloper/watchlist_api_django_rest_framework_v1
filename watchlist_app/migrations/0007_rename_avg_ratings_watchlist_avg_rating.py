# Generated by Django 4.1.2 on 2023-07-27 04:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('watchlist_app', '0006_watchlist_avg_ratings_watchlist_number_rating'),
    ]

    operations = [
        migrations.RenameField(
            model_name='watchlist',
            old_name='avg_ratings',
            new_name='avg_rating',
        ),
    ]
