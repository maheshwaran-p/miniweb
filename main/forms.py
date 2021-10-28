from django import forms
from .models import MeetUrl
class MeetUrlModelForm(forms.ModelForm):
    class Meta:
        model = MeetUrl
        fields = '__all__'