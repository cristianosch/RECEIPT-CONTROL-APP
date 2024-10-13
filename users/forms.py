from django import forms
from .models import Profile

class EditProfile(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'meta']
        widgets = {
            'user' : forms.HiddenInput(), # Tornar o user invisivel
            'bio' : forms.Textarea(attrs={'class':'card1','rows': 10, 'cols':20 }),
            'meta': forms.Textarea(attrs={'rows': 1, 'cols':5})
        }
