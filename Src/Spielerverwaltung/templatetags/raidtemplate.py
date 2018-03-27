from django import template
from ..models import Raid, Gildencharakter

register = template.Library()

@register.inclusion_tag('raidtemplate.html', takes_context=True)
def show_raid(context, raid):
    if (set(Gildencharakter.objects.filter(Spielername_id=context['spieler'])) & set(raid.Raidteilnehmer.all())):
        background = True
    else:
        background = False

    return {
        'player' : context['spieler'],
        'raid' : raid,
        'background' : background
    }
