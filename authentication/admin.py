# authentication/admin.py
from django.contrib import admin
from .models import CustomUser, Location

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active', 'location', 'display_covered_locations')

    def display_covered_locations(self, obj):
        return ', '.join(location.name for location in obj.covered_locations.all())

    display_covered_locations.short_description = 'Covered Locations'

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Location)
