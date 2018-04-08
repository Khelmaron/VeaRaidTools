# Generated by Django 2.0.2 on 2018-04-04 22:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Spielerverwaltung', '0011_auto_20180327_2019'),
    ]

    operations = [
        migrations.RenameField(
            model_name='raid',
            old_name='Teilnehmr',
            new_name='Teilnehmer',
        ),
        migrations.AddField(
            model_name='raid',
            name='Raid_status',
            field=models.CharField(choices=[('SC', 'scheduled'), ('FI', 'finished'), ('CA', 'canceled')], default='SC', max_length=2),
        ),
        migrations.AddField(
            model_name='raid',
            name='Raidende',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='raid',
            name='Raidstart',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='raidinformationen',
            name='Teilnahmer_status',
            field=models.CharField(choices=[('AT', 'attending'), ('NA', 'not attending'), ('ST', 'standby'), ('CF', 'confirmed'), ('IV', 'invited'), ('PA', 'participated')], default='IV', max_length=2),
        ),
    ]
