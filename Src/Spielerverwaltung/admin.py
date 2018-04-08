from django.contrib import admin
from .models import Gildencharakter, Spieler, Raid, Raidinformationen, Attendency
# Register your models here.
admin.site.register(Gildencharakter)
admin.site.register(Spieler)
admin.site.register(Raid)
admin.site.register(Raidinformationen)
admin.site.register(Attendency)
