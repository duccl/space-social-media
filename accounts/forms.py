from django import forms
from django.contrib.auth.models import User

class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username","password",'email')

    def is_valid(self):
        pass

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class':'special'})
        self.fields['password'].widget.attrs.update({'class':'special'})

