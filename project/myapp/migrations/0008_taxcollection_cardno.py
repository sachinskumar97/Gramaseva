# Generated by Django 3.1.6 on 2021-06-01 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_auto_20210531_1351'),
    ]

    operations = [
        migrations.AddField(
            model_name='taxcollection',
            name='cardno',
            field=models.CharField(default='0', max_length=500),
            preserve_default=False,
        ),
    ]
