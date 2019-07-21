from django import forms
from rssgenerator.models import Items

class ItemsAdminForm(forms.ModelForm):
    localFiles = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), 
        required=False,
        label="Local images")

    class Meta:
        model = Items
        fields = '__all__'
