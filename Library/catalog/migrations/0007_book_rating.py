# Generated by Django 2.2 on 2019-12-11 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_auto_20191211_1226'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='rating',
            field=models.FloatField(default=0, verbose_name='Average rate'),
        ),
    ]
