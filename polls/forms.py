from django import forms
from .models import AnnouncedPUResults, Party, AgentName


class PollForm(forms.Form):
    party_abbreviation = forms.ModelChoiceField(label="Party", queryset=Party.objects.all())
    party_score = forms.CharField(label="Party Score", widget=forms.NumberInput())
    entered_by_user = forms.CharField(label="Entered by User", max_length=50)
    date_entered = forms.DateTimeField(label="Date Entered", widget=forms.DateTimeInput(
        attrs={"type": "date"}   
    ))
    