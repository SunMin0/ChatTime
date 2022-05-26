
from django import forms


class AddProductForm(forms.Form):
    quantity = forms.IntegerField()
    is_update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
    size = forms.CharField(max_length=50, widget=forms.HiddenInput)
    temp = forms.CharField(max_length=50, widget=forms.HiddenInput)
#size,temp 넣기위해서 추가