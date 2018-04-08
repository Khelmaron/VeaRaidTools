from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, CreateView
from .models import Gildencharakter, Spieler, Raid, Raidinformationen, PlayerSerializer, Attendency, RaidByStatus
from .apiInterface import Guildmemberhandler, RaidlogInterface, AuthHandler
from .utils import get_raiddetails, get_new_logs, delete_players, assign_player, get_chars, update_activity, delete_attendence
import datetime
from rest_framework import viewsets
from rest_framework.response import Response
from .forms import CreatePlayerForm, CreateRaidForm
from django.forms import Form

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

    def post(self, request):

        if 'delete_logs' in request.POST:
            Raid.objects.all().delete()
            return HttpResponseRedirect('/Raiduebersicht/')
#            AuthHandler.get_authCode()

        logs = get_new_logs()
        for log in logs:
            raid = Raid(WarcraftlogsID = log['id'], InstanceName = log['title'],
                Raiddatum = datetime.datetime.fromtimestamp(log['start']/1000),
                Raidstart = datetime.datetime.fromtimestamp(log['start']/1000),
                Raidende = datetime.datetime.fromtimestamp(log['end']/1000))
            raid.save()

        return HttpResponseRedirect('/Raiduebersicht/')

class RaidDetailView(DetailView):

    model = Raid

    def get_context_data(self, **kwargs):
        context = super(RaidDetailView, self).get_context_data(**kwargs)

##      Prüfung ob für den Raid bereits Informationen in der Informationstabelle vorliegen.
##      Falls nein werden diese über die Funktion mittelbar an der WarcraftlogsAPI abgeholt.
        if not Raidinformationen.objects.filter(Raid = context['raid'].id).exists():
            get_raiddetails(context['raid'].WarcraftlogsID)
            context['success'] = True

        return context

class PlayerDetailView(DetailView):

    model = Spieler

    def get_context_data(self, **kwargs):
        # Hilfsfunktion, muss unbedingt entfernt werden!
        update_activity()

        context = super(PlayerDetailView, self).get_context_data(**kwargs)

#       Filter zuerst alle Charaktere, die zu dem Spieler zugeordnet sind, und übergibt diese an das template ind er Variable characters
        context['characters'] = Gildencharakter.objects.filter(Spielername__exact=context['spieler'])
        context['latest_raids'] = Raid.objects.all()[:10]
        return context

    def post(self, request, pk):

        delete_attendence(Spieler.objects.get(pk=pk))
        return HttpResponseRedirect('/Raiduebersicht/')

class PlayerViewSet(viewsets.ModelViewSet):

    queryset = Spieler.objects.all()
    serializer_class = PlayerSerializer

    def getPlayers(self, request):
        return Response(serializer_class.data)

#class ScheduledRaids(ListFilteredMixin, ListView):
#    filter_set = RaidByStatus
#    model = Raid
#    template_name = 'scheduled_raids.html'
#    paginate_by = 15

#    def get_queryset(self):
#
#        queryset = Raid.objects.filter(raid_status = 'SC')
#        return queryset

def scheduled_raids(request):

    f = RaidByStatus(request.GET, queryset = Raid.objects.all())
    return render(request, 'Spielerverwaltung/scheduled_raids.html', { 'filter' : f })

class Raidcreation(FormView):
    template_name = 'create_raid.html'
    form_class = CreateRaidForm
    success_url = '/Raiduebersicht/'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        return HttpResponseRedirect('/Raiduebersicht/')

class RaidCreate(CreateView):
    model = Raid
    template_name_suffix = '_create'
    fields = ['Raidstart', 'Raidende', 'Teilnehmer']
