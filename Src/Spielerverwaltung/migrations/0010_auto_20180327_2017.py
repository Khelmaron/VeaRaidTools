# Generated by Django 2.0.2 on 2018-03-27 18:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Spielerverwaltung', '0009_auto_20180326_0046'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='gildencharakter',
            options={'ordering': ['Charaktername']},
        ),
        migrations.AlterModelOptions(
            name='raid',
            options={'ordering': ['Raiddatum']},
        ),
        migrations.AlterModelOptions(
            name='spieler',
            options={'ordering': ['Anlagedatum']},
        ),
    ]
