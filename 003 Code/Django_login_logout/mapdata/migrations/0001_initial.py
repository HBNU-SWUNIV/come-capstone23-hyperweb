# Generated by Django 4.1 on 2023-04-04 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mapdata',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place', models.TextField(blank=True, null=True)),
                ('category1', models.TextField(blank=True, null=True)),
                ('category2', models.TextField(blank=True, null=True)),
                ('category3', models.TextField(blank=True, null=True)),
                ('sido', models.TextField(blank=True, db_column='Sido', null=True)),
                ('sigungu', models.TextField(blank=True, db_column='SiGunGu', null=True)),
                ('eup', models.TextField(blank=True, db_column='Eup', null=True)),
                ('bunji', models.TextField(blank=True, db_column='Bunji', null=True)),
                ('streetname', models.TextField(blank=True, db_column='StreetName', null=True)),
                ('streetnumber', models.TextField(blank=True, db_column='StreetNUmber', null=True)),
                ('latitude', models.FloatField(blank=True, db_column='Latitude', null=True)),
                ('longitude', models.FloatField(blank=True, db_column='Longitude', null=True)),
                ('zipcode', models.IntegerField(blank=True, db_column='ZipCode', null=True)),
                ('streetaddress', models.TextField(blank=True, db_column='StreetAddress', null=True)),
                ('lotnumberaddress', models.TextField(blank=True, db_column='LotNumberAddress', null=True)),
                ('callnumber', models.TextField(blank=True, db_column='CallNumber', null=True)),
                ('homepage', models.TextField(blank=True, db_column='Homepage', null=True)),
                ('closeddays', models.TextField(blank=True, db_column='ClosedDays', null=True)),
                ('runningtime', models.TextField(blank=True, db_column='RunningTime', null=True)),
                ('parkingavailable', models.TextField(blank=True, db_column='ParkingAvailable', null=True)),
                ('fee', models.TextField(blank=True, db_column='Fee', null=True)),
                ('restrictions', models.TextField(blank=True, db_column='Restrictions', null=True)),
                ('inside', models.TextField(blank=True, db_column='Inside', null=True)),
                ('outside', models.BinaryField(blank=True, db_column='Outside', null=True)),
                ('placeexp', models.TextField(blank=True, db_column='PlaceExp', null=True)),
                ('surcharge', models.TextField(blank=True, db_column='Surcharge', null=True)),
            ],
            options={
                'db_table': 'mapdata',
                'managed': False,
            },
        ),
    ]