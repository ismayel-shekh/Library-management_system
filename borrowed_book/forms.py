from django import forms
from .models import borrowed_history
class history(forms.ModelForm):
    class Meta:
        model = borrowed_history
        fields = '__all__'