from django import template
from datetime import date, timedelta
from ..models import Raid


register = template.Library()

@register.filter(name = 'attendence')
def attendence(value, datestart = (date.today() - timedelta(days=30)), datefinish = date.today()):
    return (Raid.objects.filter(Raidteilnehmer__Spielername=value, Raiddatum__range=[datestart, datefinish]).count()
        / Raid.objects.filter(Raiddatum__range=[datestart, datefinish]).count() * 100
    )


# Soll ein Filter für die letzten x Raids statt Datumsfilter werden
#@register.filter(name = 'attendenceByAmount')
#def attendenceByAmount(value, amount = 10):
#    latest_raids = Raid.objects.all()[:10]
#    return (len({x for x in latest_raids if value in latest_raids}) / amount)
