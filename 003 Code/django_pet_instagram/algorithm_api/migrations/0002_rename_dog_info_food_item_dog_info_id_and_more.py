# Generated by Django 4.2 on 2023-07-02 03:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('algorithm_api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='food_item',
            old_name='dog_info',
            new_name='dog_info_id',
        ),
        migrations.RenameField(
            model_name='nut_7_save',
            old_name='dog_info',
            new_name='dog_info_id',
        ),
        migrations.RenameField(
            model_name='nut_report',
            old_name='dog_info',
            new_name='dog_info_id',
        ),
    ]