from django.db.models.signals import post_save
from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class Cafe(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to='cafes/', blank=True)   
    has_wifi = models.BooleanField(default=False)
    has_power_outlet = models.BooleanField(default=False)
    has_restroom = models.BooleanField(default=False)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    posted_at = models.DateTimeField(auto_now_add=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    opening_time = models.TimeField(null=True, blank=True)
    closing_time = models.TimeField(null=True, blank=True)

    def average_rating(self):
        ratings = self.ratings.all()
        if ratings:
            return sum(r.stars for r in ratings) / len(ratings)
        return 0

    def is_open_now(self):
        if not self.opening_time or not self.closing_time:
            return None  # Unknown
        
        now = datetime.now().time()
        
        # Handle normal hours (e.g., 9:00 AM - 6:00 PM)
        if self.opening_time <= self.closing_time:
            return self.opening_time <= now <= self.closing_time
        # Handle overnight hours (e.g., 8:00 PM - 2:00 AM)
        else:
            return now >= self.opening_time or now <= self.closing_time

    def __str__(self):
        return self.name

class Rating(models.Model):
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('cafe', 'user') # each user can only rate each cafe once
    
    def __str__(self):
        return f"{self.user.username} rated {self.cafe.name} {self.stars} stars"


class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE, related_name='bookmarked_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'cafe')


class CafePhoto(models.Model):
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='cafe_photos/')
    caption = models.CharField(max_length=200, blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"Photo for {self.cafe.name}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        # When a new user is created, also create a Profile
        Profile.objects.create(user=instance)
    # Every time the user is saved, save the profile too
    instance.profile.save()