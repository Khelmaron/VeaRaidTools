from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Gildencharakter, Spieler, Raid, Raidinformationen, PlayerSerializer
from .apiInterface import Guildmemberhandler, RaidlogInterface
from .utils import get_raiddetails
import datetime
from rest_framework import viewsets
from rest_framework.response import Response

from .forms import CreatePlayerForm
from django.forms import Form
from .utils import delete_players, assign_player, get_chars, update_activity

class homeView(TemplateView):

    def get(self, request):
        template = "base.html"

        return render(request, template, {})

class charoverView(ListView):

    model = Gildencharakter
    template = 'Charakteruebersicht.html'
    paginate_by = 10

    def get_queryset(self):

        queryset = Gildencharakter.objects.filter(Gildenrang__lte=4 ).order_by('Charaktername')
        return queryset


    def get_context_data(self, **kwargs):
        context = super(charoverView, self).get_context_data(**kwargs)
        queryset_player = Spieler.objects.all()
        context['Spielerliste'] = queryset_player
        return context

    def post(self, request):

        if 'save' in request.POST:
            form = request.POST.lists()
            for key, item in form:
                assign_player(key, ''.join(item))
            return HttpResponseRedirect('/Charakteruebersicht/')

        guildmembers = Guildmemberhandler.return_guildmembers()
        new_guildmembers = [ x for x in guildmembers if x['name'] not in Gildencharakter.objects.all().values_list('Charaktername',flat = True)]
        for member in new_guildmembers:
            m = Gildencharakter( Charaktername = member['name'],
                Gildenrang = member['rank'])
            m.save()
        return HttpResponseRedirect('/Charakteruebersicht/')

class playeroverView(TemplateView):

    def get(self, request):

        test = CreatePlayerForm()
        paginate_by = 2
        template = 'Spieleruebersicht.html'
        queryset = Spieler.objects.all()
        context = {
            'Spielerliste' : queryset,
            'form' : test
                    }

        return render (request, template, context)

    def post(self, request):

        if request.POST.get('add') == "Add":
            form = CreatePlayerForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data['name']
                player = Spieler(name)
                player.save()

        elif request.POST.get('delete') == "Delete":
            playerlist = request.POST.getlist('Selected_Players', None)
            delete_players(playerlist)

        return HttpResponseRedirect('/Spieleruebersicht/')

class RaidoverView(ListView):

    model = Raid
    paginate_by = 10

    def get_queryset(self):

        return super(RaidoverView, self).get_queryset().order_by('-Raiddatum')

    def post(self, request):

        logs = RaidlogInterface.get_latest_report_ids()
        for log in logs:
            raid = Raid(WarcraftlogsID = log['id'], InstanceName = log['title'],
                Raiddatum = datetime.datetime.fromtimestamp(log['start']/1000))
            raid.save()

        return HttpResponseRedirect('/Raiduebersicht/')

class RaidDetailView(DetailView):

    model = Raid

##    def get_context_data(self, **kwargs):
##        context = super(RaidDetailView, self).get_context_data(**kwargs)
##        queryset_player = Raidinformationen.objects.filter()
##        context['Spielerliste'] = queryset_player
##        return context



    def get_context_data(self, **kwargs):
        context = super(RaidDetailView, self).get_context_data(**kwargs)

##      Prüfung ob für den Raid bereits Informationen in der Informationstabelle vorliegen.
##      Falls nein werden diese über die Funktion mittelbar an der WarcraftlogsAPI abgeholt.
        if not Raidinformationen.objects.filter(Raid = context['raid'].id).exists():
            get_raiddetails(context['raid'].WarcraftlogsID)
            context['success'] = True

        context['Raidinfomrationen'] = Raidinformationen.objects.filter(Raid = context['raid'].id)

        return context

class PlayerDetailView(DetailView):

    model = Spieler

    def get_context_data(self, **kwargs):
        # Hilfsfunktion, muss unbedingt entfernt werden!
        update_activity()

        context = super(PlayerDetailView, self).get_context_data(**kwargs)

#       Filter zuerst alle Charaktere, die zu dem Spieler zugeordnet sind, und übergibt diese an das template ind er Variable characters
        context['characters'] = Gildencharakter.objects.filter(Spielername__exact=context['spieler'])
        return context


class PlayerViewSet(viewsets.ModelViewSet):

    queryset = Spieler.objects.all()
    serializer_class = PlayerSerializer

    def getPlayers(self, request):
        return Response(serializer_class.data)
