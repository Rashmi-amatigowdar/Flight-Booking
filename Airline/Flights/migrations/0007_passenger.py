# Generated by Django 3.2.6 on 2021-09-03 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Flights', '0006_flight'),
    ]

    operations = [
        migrations.CreateModel(
            name='Passenger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first', models.CharField(max_length=64)),
                ('last', models.CharField(max_length=64)),
                ('flight', models.ManyToManyField(blank=True, related_name='passengers', to='Flights.Flight')),
            ],
        ),
    ]