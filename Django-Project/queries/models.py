import datetime as dt
from django.db import models
from django.contrib import admin
from django.utils import timezone

# Create your models here.

class Query(models.Model):
    queryDate = models.DateTimeField(auto_now=False, auto_now_add=True)
    dateStart = models.DateField(auto_now=False, auto_now_add=False)
    dateEnd = models.DateField(auto_now=False, auto_now_add=False)
    keyword = models.TextField(blank=True)
    # result = models.IntegerField(blank=True)
    # FileField(upload_to=user_directory_path)

    def __str__(self):
        # strftime("%m %d %Y")
        return self.dateStart.__str__() + " -> " + self.dateEnd.__str__()

class Transaction(models.Model):
    query = models.ForeignKey(Query, on_delete=models.CASCADE)
    trans_name = models.CharField(max_length=200)
    trans_date = models.DateField(auto_now=False, auto_now_add=False)
    trans_comment = models.CharField(max_length=500)
    trans_amount = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.trans_date.strftime("%m/%d/%Y") + " " + self.trans_name + " " + str(self.trans_amount) + " " + self.trans_comment
