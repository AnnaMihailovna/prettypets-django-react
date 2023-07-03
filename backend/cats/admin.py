from django.contrib import admin

from .models import Cat

class CatAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'birth_year', 'owner')
    search_fields = ('name',)
    list_filter = ('birth_year',)
    empty_value_display = '-пусто-'

admin.site.register(Cat, CatAdmin)
 
