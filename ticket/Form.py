from django.forms import ModelForm, Textarea,TextInput
from django import forms
from .models import Ticket
class TicketForm(ModelForm):
    
    class Meta:
        model = Ticket
        fields = ['title', 'comments']
        widgets = {
                    'title':  TextInput(attrs={'size': '80'}),
                    'comments':  Textarea(attrs={'cols': 80, 'rows': 20}),
                }

    