from django.contrib import admin

# Register your models here.

from .models import Adresa,Dogadjaj,Planer, CrkvenaOpstina, Eparhija, Slava, Parohija,Domacinstvo
from .models import Ukucanin,UkucaninTemp,NareceniTemp,Nareceni,PreminuliTemp,Preminuli

admin.site.register(Eparhija)
admin.site.register(Adresa)
admin.site.register(CrkvenaOpstina)
admin.site.register(Slava)
admin.site.register(Parohija)
admin.site.register(Domacinstvo)
admin.site.register(Dogadjaj)
admin.site.register(Planer)
admin.site.register(Ukucanin)
admin.site.register(UkucaninTemp)
admin.site.register(Nareceni)
admin.site.register(NareceniTemp)
admin.site.register(Preminuli)
admin.site.register(PreminuliTemp)