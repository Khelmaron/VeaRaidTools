from django.db import models
import django_filters
from django.forms import ModelForm
from rest_framework import serializers

class Gildencharakter(models.Model):

    Charaktername = models.CharField(max_length = 30, primary_key = True)
    Spielername = models.ForeignKey('Spieler', on_delete = models.CASCADE, blank = True, null = True)
    Gildenrang = models.CharField(max_length = 30, null = False, blank = False)

    def __str__(self):
        return self.Charaktername

    class Meta:
        ordering = ['Charaktername']

class Spieler(models.Model):

    Spielername = models.CharField(max_length = 50, primary_key = True)
    Anlagedatum = models.DateField(auto_now_add = True)
    Aktiv       = models.BooleanField(default = False)

    def __str__(self):
        return self.Spielername

    class Meta:
        ordering = ['Anlagedatum']

class Raid(models.Model):

    Raidstatus = (
        ('SC', 'scheduled'),
        ('FI', 'finished'),
        ('CA', 'canceled')
        )

    Raid_status = models.CharField(max_length = 2, choices = Raidstatus, default = 'SC')
    WarcraftlogsID = models.CharField(max_length = 16, blank = True, null = True, unique = True)
    InstanceName = models.CharField(max_length = 50)
    Raiddatum = models.DateTimeField()
    Raidstart = models.DateTimeField()
    Raidende = models.DateTimeField()
    Raidteilnehmer = models.ManyToManyField(Gildencharakter, through = 'Raidinformationen')
    Teilnehmer = models.ManyToManyField(Spieler, through = 'Attendency')

    def __str__(self):
        return self.WarcraftlogsID

    class Meta:
        ordering = ['-Raiddatum']

class RaidByStatus(django_filters.FilterSet):

    Raid_status = django_filters.ChoiceFilter(choices = (
                                                    ('SC', 'scheduled'),
                                                    ('FI', 'finished'),
                                                    ('CA', 'canceled')
                                                    ))

    class Meta:

        model = Raid
        fields = ['Raid_status']

class Raidinformationen(models.Model):

# Muss eigentlich irgendwie an den Spieler ran
    Teilnehmerstatus = (
        ('AT', 'attending'),
        ('NA', 'not attending'),
        ('ST', 'standby'),
        ('CF', 'confirmed'),
        ('IV', 'invited'),
        ('PA', 'participated')
        )

    Teilnahmer_status = models.CharField(max_length = 2, choices = Teilnehmerstatus, default = 'IV')
    Teilnehmer = models.ForeignKey(Gildencharakter, on_delete=models.PROTECT)
    Raid = models.ForeignKey(Raid, on_delete=models.CASCADE)
#    Spieler = models.ForeignKey(Spieler, on_delete=models.CASCADE, blank = True, null = True)
#    did_participate = models.BooleanField(default = False)

class Attendency(models.Model):

    Raid = models.ForeignKey(Raid, on_delete=models.CASCADE)
    Spieler = models.ForeignKey(Spieler, on_delete=models.CASCADE)
    did_participate = models.BooleanField(default = False)

    class Meta:
        unique_together = (('Raid', 'Spieler'))

class PlayerSerializer(serializers.HyperlinkedModelSerializer):
     class Meta:
        model = Spieler
        fields = ('Spielername', 'Anlagedatum', 'Aktiv')
