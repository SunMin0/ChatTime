from django import forms
from .models import Product



class ProductForm(forms.ModelForm):
    class Meta:
        model = Product  # 사용할 모델
        exclude = ()