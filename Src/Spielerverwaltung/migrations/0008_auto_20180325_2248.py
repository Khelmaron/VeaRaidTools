# Generated by Django 2.0.2 on 2018-03-25 20:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Spielerverwaltung', '0007_auto_20180325_2246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='raidinformationen',
            name='Teilnehmer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Spielerverwaltung.Gildencharakter'),
        ),
    ]