from django.db import models

# Create your models here.
class Stock(models.Model):
    symbol = models.TextField(max_length=20)
    date = models.TextField(max_length=25)
    price = models.TextField(max_length=25)