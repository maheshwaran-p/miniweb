# Generated by Django 3.2.8 on 2021-10-28 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_rename_owners_class_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeturl',
            name='endtime',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='meeturl',
            name='starttime',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
