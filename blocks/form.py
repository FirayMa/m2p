from django.forms import ModelForm, Textarea,TextInput
from django import forms 
from .models import Block

 
 
class BlockForm(ModelForm): 
    class Meta:
        model = Block
        fields = ['title', 'desc', 'type']
        exclude = ['status', 'date']
 
        
