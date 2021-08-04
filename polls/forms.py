from django import forms
from .models import Party, LGA


class PollForm(forms.Form):
    party_abbreviation = forms.ModelChoiceField(label="Party", queryset=Party.objects.all())
    party_score = forms.CharField(label="Party Score", widget=forms.NumberInput())
    entered_by_user = forms.CharField(label="Entered by User", max_length=50)
    date_entered = forms.DateTimeField(label="Date Entered", widget=forms.DateTimeInput(
        attrs={"type": "date"}   
    ))


class LGAForm(forms.Form):
    lga = forms.ModelChoiceField(label="Select LGA", required=False, queryset=LGA.objects.all(), widget=forms.Select(
        attrs={"class": "form-control"}
    ))