from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class': 'w-full p-3 rounded-lg bg-slate-700 text-white border border-slate-600'
        })

        self.fields['password1'].widget.attrs.update({
            'class': 'w-full p-3 rounded-lg bg-slate-700 text-white border border-slate-600'
        })

        self.fields['password2'].widget.attrs.update({
            'class': 'w-full p-3 rounded-lg bg-slate-700 text-white border border-slate-600'
        })

class CustomAuthenticationForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class': 'w-full p-3 rounded-lg bg-slate-700 text-white border border-slate-600'
        })

        self.fields['password'].widget.attrs.update({
            'class': 'w-full p-3 rounded-lg bg-slate-700 text-white border border-slate-600'
        })