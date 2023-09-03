from django import forms
from .models import User,Offer

class AvatarForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['avatar']

class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ['gpa', 'ielts_score', 'institution', 'major', 'offer_image']