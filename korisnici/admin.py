from django.contrib import admin

# Register your models here.
from .models import User, Svestenik

admin.site.register(User)
admin.site.register(Svestenik)
