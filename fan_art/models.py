from django.db import models
from datetime import date

from profiles.models import UserProfile
from series.models import Series


class FanArt(models.Model):
    image = models.ImageField()
    title = models.CharField(max_length=254)
    artist_name = models.CharField(max_length=254, null=True, blank=True)
    description = models.TextField()
    is_approved = models.BooleanField(default=False)
    publish_date = models.DateField(default=date.today)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='fan_art')
    series = models.ForeignKey(Series, on_delete=models.SET_NULL, null=True, related_name='fan_art')

    def __str__(self):
        return f'Title: {self.title}, by user {self.user_profile.user}'
