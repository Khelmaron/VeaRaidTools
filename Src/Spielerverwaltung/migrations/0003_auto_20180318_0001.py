# Generated by Django 2.0.2 on 2018-03-17 23:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Spielerverwaltung', '0002_auto_20180311_1823'),
    ]

    operations = [
        migrations.AddField(
            model_name='raid',
            name='InstanceName',
            field=models.CharField(default='unknown', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='raid',
            name='WarcraftlogsID',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
    ]
