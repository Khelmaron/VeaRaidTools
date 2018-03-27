from .models import Spieler
from .models import Gildencharakter
from .models import Raid, Raidinformationen, Attendency
from .apiInterface import RaidlogInterface
from datetime import date, timedelta

def delete_players(playerlist):

#   ggf mit performanterer Abfrage verwenden (Direkt auf die ganze Liste filtern)
    for player in playerlist:
        p = Spieler.objects.filter(Spielername = player)
        p.delete()

def get_raiddetails(reportID):

    participants = RaidlogInterface.get_participants(reportID)
    guild_participants = Gildencharakter.objects.filter(Charaktername__in = participants)
    players = guild_participants.values()
    raid = Raid.objects.filter(WarcraftlogsID = reportID)
    set_participants(raid.first(), players, status='True')
    for part in guild_participants:
        r = Raidinformationen(Raid = raid.first(), Teilnehmer = part)
        r.save()

def get_Raidkader():

    return Spieler.objects.filter(Aktiv=True)

def delete_attendence(player):

    Attendency.objects.filter(Spieler = player).delete()

def get_attendency(player, datestart = (date.today() - timedelta(days=30)), datefinish = date.today):

    return (Raid.objects.filter(Raidteilnehmer__Spielername__in=player, Raiddatum__range=[datestart, datefinish]).count / Raid.objects.filter(Raiddatum__range=[datestart, datefinish]))

def set_participants(raid, players, status=False):

#    attendency = Attendency.objects.all()
#    if Attendency.objects.filter(Raid__WarcraftLogsID__exact = raid).exists():
#        affected_raid = Attendency.objects.filter(raid = raid)
#    else:
#
#   Legt erstmal für jeden Spieler im Raidkader einen Attendence-Satz an, der zum Abrufzeitpunkt den Flag "aktiv"
    for member in get_Raidkader():
        a = Attendency(Raid = raid, Spieler = member)
        a.save()

#Trägt den Status in Attendence entweder auf True oder false ein.
    for player in players:
        raid.did_participate = status

def get_new_logs():
    logs = RaidlogInterface.get_latest_report_ids()
    new_logs = [ x for x in logs if x['id'] not in Raid.objects.all().values_list('WarcraftlogsID',flat = True)]
    return new_logs

## Derzeit werden alle Spieler immer geupdatet, auch wenn nichts verändert wird => Performance kann noch deutlich verbessert werden
def assign_player(character, player):

    try:
        char = Gildencharakter.objects.get(Charaktername=character)
        char.Spielername = Spieler.objects.get(Spielername=player)
        char.save()
    except:
        pass

def get_chars(player):

    return Gildencharakter.objects.filter(Spielername__exact=player)

#   Kann vermutlich auch performanter geschrieben werden
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
