from django.contrib import admin
from .models import CarMake, CarModel

class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 5

class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]
    list_display = ('name',)
    search_fields = ['name', 'description']

admin.site.register(CarMake, CarMakeAdmin)
