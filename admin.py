from django.contrib import admin
from fileman.models import *

class SettingAdmin(admin.ModelAdmin):
   list_display = ('owner', 'root', 'home')

admin.site.register(Setting, SettingAdmin)

class HistoryAdmin(admin.ModelAdmin):
    list_display = ('action', 'date', 'author')
    list_filter = ('date',)

admin.site.register(History, HistoryAdmin)

class AliasAdmin(admin.ModelAdmin):
   pass

admin.site.register(Alias, AliasAdmin)
