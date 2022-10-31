from django import forms


class EmailSendForm(forms.Form):
    email = forms.EmailField(label='Email:', max_length=200, widget=forms.EmailInput(attrs={
        'placeholder': "Your Email"
    }))
