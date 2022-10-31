from django import forms
from Acount_module.models import UserAcount


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email:', max_length=200, widget=forms.EmailInput(attrs={
        'class': 'form-style ',
        'id': 'logemail',
        'placeholder': "Your Email"
    }))
    password = forms.CharField(max_length=200, label='Password:', widget=forms.PasswordInput(attrs={
        'class': 'form-style',
        'id': 'logpass',
        'placeholder': "Your Password"
    }))


class RegisterForm(forms.Form):
    email = forms.EmailField(label='Email:', max_length=200, widget=forms.EmailInput(attrs={
        'class': 'form-style ',
        'id': 'logemail',
        'placeholder': "Your Email"
    }))
    password = forms.CharField(max_length=200, label='Password:', min_length=8, widget=forms.PasswordInput(attrs={
        'class': 'form-style',
        'id': 'logpass',
        'placeholder': "Your Password"
    }))
    repeat_password = forms.CharField(max_length=200, label='Password:', min_length=8,
                                      widget=forms.PasswordInput(attrs={
                                          'class': 'form-style',
                                          'id': 'logpass',
                                          'placeholder': "Your Password"
                                      }))


class ChangePassForm(forms.Form):
    current_password = forms.CharField(max_length=200, label='Current Password:', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your current password'
    }))
    new_password = forms.CharField(max_length=200, label='New Password:', min_length=8,
                                   widget=forms.PasswordInput(attrs={
                                       'class': 'form-control',
                                       'placeholder': 'Enter your new password'
                                   }))
    new_password_repeat = forms.CharField(max_length=200, label='New Password Repeat:', min_length=8,
                                          widget=forms.PasswordInput(attrs={
                                              'class': 'form-control',
                                              'placeholder': 'Repeat your new password'
                                          }))


class UserPanelForm(forms.ModelForm):
    class Meta:
        model = UserAcount
        fields = ['first_name', 'last_name', 'avatar', 'email', 'username']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'firstName'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'firstName'
            }),

            'avatar': forms.FileInput(),

            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'id': 'firstName'
            }),
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'username'
            })
        }
