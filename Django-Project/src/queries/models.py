from django.db import models

# Create your models here.
class Query(models.Model):
    dateStart = models.DateField(auto_now=False, auto_now_add=False)
    dateEnd = models.DateField(auto_now=False, auto_now_add=False)
    keyword = models.TextField(blank=True)
