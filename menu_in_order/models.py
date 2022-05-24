from django.db import models
from django.urls import reverse
from order.models import Order
from menu.models import Menu

class menu_in_order(models.Model):
    count = models.IntegerField()
    price = models.IntegerField()
    is_hot = models.BooleanField(default=False)
    is_small = models.BooleanField(default=False)
    order_id = models.ForeignKey(Order,on_delete=models.CASCADE)
    menu_id = models.ForeignKey(Menu,on_delete=models.CASCADE)

