# Generated by Django 5.0.4 on 2025-02-06 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_alter_bookevent_our_service'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookevent',
            name='our_service',
            field=models.CharField(choices=[('Trivandrum', 'Trivandrum'), ('kollam', 'kollam'), ('Alappuzha', 'Alappuzha'), ('Kottayam', 'Kottayam')], max_length=50),
        ),
    ]
