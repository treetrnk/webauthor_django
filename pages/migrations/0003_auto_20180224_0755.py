# Generated by Django 2.0.2 on 2018-02-24 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_auto_20180223_1212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='pub_date',
            field=models.DateTimeField(),
        ),
    ]
