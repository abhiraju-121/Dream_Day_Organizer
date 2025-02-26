# Generated by Django 5.0.4 on 2025-02-07 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0014_bridalgroomservice_bridalgroomservicebooking'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='itinerary',
        ),
        migrations.AddField(
            model_name='bookevent',
            name='customize',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cateringbooking',
            name='customize_food',
            field=models.CharField(choices=[('non-veg', 'non-veg'), ('veg', 'veg'), ('north-indian', 'north-indian'), ('desserts', 'desserts')], default=1, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transportationbooking',
            name='rent_car',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='venuebooking',
            name='venue_customize',
            field=models.CharField(choices=[('indoor', 'indoor'), ('outdoor', 'outdoor'), ('other', 'other')], default=1, max_length=20),
            preserve_default=False,
        ),
    ]
