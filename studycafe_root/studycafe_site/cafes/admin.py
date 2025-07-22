from django.contrib import admin
from .models import Cafe, Rating, CafePhoto, Follow, Bookmark, Profile

# Register your models here.
@admin.register(Cafe)
class CafeAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'has_wifi', 'has_power_outlet', 'has_restroom')
    list_filter = ('has_wifi', 'has_power_outlet', 'has_restroom')
    search_fields = ('name', 'address')

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('cafe', 'user', 'stars', 'created_at')

@admin.register(CafePhoto)
class CafePhotoAdmin(admin.ModelAdmin):
    list_display = ('cafe', 'uploaded_by', 'caption', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('cafe__name', 'caption')

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('follower', 'following', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('follower__username', 'following__username')

@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'cafe', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'cafe__name')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')
    search_fields = ('user__username',)