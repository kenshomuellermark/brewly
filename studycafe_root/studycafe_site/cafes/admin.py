from django.contrib import admin
from .models import Cafe, Rating

# Register your models here.
@admin.register(Cafe)
class CafeAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'has_wifi', 'has_power_outlet', 'has_restroom')
    list_filter = ('has_wifi', 'has_power_outlet', 'has_restroom')
    search_fields = ('name', 'address')

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('cafe', 'user', 'stars', 'created_at')