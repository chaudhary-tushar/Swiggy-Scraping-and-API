# Generated by Django 4.1.7 on 2023-04-03 14:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djswig', '0005_alter_city_options_alter_restaurantdat_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='city',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='restaurantdat',
            options={'managed': False},
        ),
    ]
