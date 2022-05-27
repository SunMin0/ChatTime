from django.db import models
from django.urls import reverse
from django.db import models
from django.urls import reverse
# from imagekit.models import ProcessedImageField
# from pilkit.processors import ResizeToFill


class Cafe(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    lat = models.FloatField()
    long = models.FloatField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name



class Product(models.Model):
    category = models.CharField(max_length=50)
    name = models.CharField(max_length=200, db_index=True)
    # slug = models.SlugField(max_length=200, db_index=True, unique=True, allow_unicode=True)
    image = models.ImageField(upload_to='products', null=False)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=0, null=True)
    available_display = models.BooleanField('Display', default=True)
    available_order = models.BooleanField('Order', default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
        index_together = [['id']]

    def __str__(self):
        return self.name

# class ProductImage(models.Model) :
#     productImage = models.ForeignKey(Product, on_delete=models.CASCADE)
#     image = models.ImageField(upload_to='products/%Y/%m/%d')