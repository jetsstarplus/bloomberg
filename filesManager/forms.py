
from django import forms
from filesManager.models import Files

class FileForm(forms.ModelForm):
    class Meta:
        model= Files
        fields= ["file_name", "file"]