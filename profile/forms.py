from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["bio", "profile_picture"]
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 3, "placeholder": "Tell us about yourself..."}),
        }
