from django.db import models
from django.contrib.auth.models import User


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
