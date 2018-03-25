from .models import Spieler
from .models import Gildencharakter
from .models import Raid, Raidinformationen
from .apiInterface import RaidlogInterface
from datetime import date, timedelta

def delete_players(playerlist):

    for player in playerlist:
        p = Spieler.objects.filter(Spielername = player)
        p.delete()

def get_raiddetails(reportID):

    participants = RaidlogInterface.get_participants(reportID)
    guild_participants = Gildencharakter.objects.filter(Charaktername__in = participants)
    raid = Raid.objects.filter(WarcraftlogsID = reportID)
    for part in guild_participants:
        r = Raidinformationen(Raid = raid.first(), Teilnehmer = part)
        r.save()

def get_attendency(player, datestart = timedelta(days=30), datefinish = date.today):
    pass

def assign_player(character, player):

    try:
        char = Gildencharakter.objects.get(Charaktername=character)
        char.Spielername = Spieler.objects.get(Spielername=player)
        char.save()
    except:
        pass

def get_chars(player):

    return Gildencharakter.objects.filter(Spielername__exact=player)

def update_activity():

    for player in Spieler.objects.all():
        set_playeractive(player)

def set_playeractive(player):

    if Gildencharakter.objects.filter(Spielername__exact=player, Gildenrang__lt=5):
        player.Aktiv = True
    else:
        player.Aktiv = False
    player.save()

#    except:
#        pass
