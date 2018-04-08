from django import template
from ..models import Raid, Raidinformationen

register = template.Library()

@register.inclusion_tag('scheduledraids.html')
def scheduled(status):
    queryset = Raids.objects.filter(raid_status = status)
    return {
        'raid_list' : queryset
    }

#@register.simple_Tag
#def anmelde_statistik(raid):
#    for playerstatus in Raidinformationen.Teilnahmer_status.all()
#        playerstatus = 0
#    for Spieler in raid:
#    return
