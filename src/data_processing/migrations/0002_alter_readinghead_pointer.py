# Generated by Django 3.2.9 on 2021-11-15 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_processing', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='readinghead',
            name='pointer',
            field=models.IntegerField(default=0),
        ),
    ]
