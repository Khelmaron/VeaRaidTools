from django.db import models
from rest_framework import serializers

class Gildencharakter(models.Model):

    Charaktername = models.CharField(max_length = 30, primary_key = True)
    Spielername = models.ForeignKey('Spieler', on_delete = models.CASCADE, blank = True, null = True)
    Gildenrang = models.CharField(max_length = 30, null = False, blank = False)

    def __str__(self):
        return self.Charaktername


class Spieler(models.Model):

    Spielername = models.CharField(max_length = 50, primary_key = True)
    Anlagedatum = models.DateField(auto_now_add = True)
    Aktiv       = models.BooleanField(default = False)

    def __str__(self):
        return self.Spielername

class Raid(models.Model):

    WarcraftlogsID = models.CharField(max_length = 16, blank = True, null = True)
    InstanceName = models.CharField(max_length = 50)
    Raiddatum = models.DateTimeField()
    Raidteilnehmer = models.ManyToManyField(Gildencharakter, through = 'Raidinformationen')

class Raidinformationen(models.Model):

    Teilnehmer = models.ForeignKey(Gildencharakter, on_delete=models.CASCADE)
    Raid = models.ForeignKey(Raid, on_delete=models.CASCADE)
    Spieler = models.ForeignKey(Spieler, on_delete=models.CASCADE, blank = True, null = True)
    did_participate = models.BooleanField(default = False)

class PlayerSerializer(serializers.HyperlinkedModelSerializer):
     class Meta:
        model = Spieler
        fields = ('Spielername', 'Anlagedatum', 'Aktiv')
