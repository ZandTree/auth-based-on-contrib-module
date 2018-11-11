from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserCreateForm(UserCreationForm):
    email = forms.EmailField(max_length=200)
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields["username"].label = "Your username"
        self.fields["email"].label = "Your Email address"

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError('Email addresses must be unique.')
        return email
# just to make post request possible
class LogoutForm(forms.Form):
    pass
