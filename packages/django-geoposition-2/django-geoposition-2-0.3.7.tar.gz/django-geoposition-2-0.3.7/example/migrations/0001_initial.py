# Generated by Django 2.0.1 on 2018-07-18 10:12

from django.db import migrations, models
import geoposition.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='PointOfInterest',
            fields=[
                ('id',
                 models.AutoField(
                     auto_created=True,
                     primary_key=True,
                     serialize=False,
                     verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=50)),
                ('zipcode', models.CharField(max_length=10)),
                ('position',
                 geoposition.fields.GeopositionField(
                     blank=True, max_length=42)),
            ],
            options={
                'verbose_name_plural': 'points of interest',
            },
        ),
    ]
