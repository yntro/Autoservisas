from .models import CarReview, OrderNotes
from django import forms

class CarReviewForm(forms.ModelForm):
    class Meta:
        model = CarReview
        fields = ['content']
        labels = {'content': ''}

class OrderNoteForm(forms.ModelForm):
    class Meta:
        model = OrderNotes
        fields = ['content']
        labels = {'content': ''}