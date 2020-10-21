from django.db import models

# Create your models here.
class Search(models.Model):
    search = models.CharField(max_length=200) 
    created = models.DateTimeField()

    def __str__(self):
        return '{}'.format(self.search)

    class Meta:
        verbose_name_plural = 'Searches'