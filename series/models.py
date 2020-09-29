from django.db import models


class Series(models.Model):
    """ Series Model """

    class Meta:
        verbose_name_plural = 'Series'

    name = models.CharField(max_length=250)
    description = models.TextField()
    page_url = models.CharField(max_length=1024)

    def __str__(self):
        return self.name
