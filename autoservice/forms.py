from .models import CarComments, OrderComments
from django import forms

class CarCommentsForm(forms.ModelForm):
    class Meta:
        model = CarComments
        fields = ['content']
        labels = {'content': ''}

class OrderCommentsForm(forms.ModelForm):
    class Meta:
        model = OrderComments
        fields = ['content']
        labels = {'content': ''}