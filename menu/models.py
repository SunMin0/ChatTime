from django.db import models
from cafe.models import Cafe
# Create your models here.



class Menu(models.Model):
    title = models.CharField(max_length=200)
    price = models.IntegerField()
    description = models.TextField(blank=True)
    img = models.ImageField()
    small_price = models.IntegerField()
    large_price = models.IntegerField()
    cafe_id = models.ForeignKey(Cafe,on_delete=models.CASCADE)



