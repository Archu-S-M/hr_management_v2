from django import forms


# Login form

class LoginForm(forms.Form):
    admin_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                              'placeholder': 'Admin Name'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control',
                                                                 'placeholder': 'Password'}))

# Registration form
class RegisterForm(forms.Form):

    admin_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                               'placeholder': 'Admin Name'}))

    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control',
                                                          'placeholder': 'Email'}))

    consultancy_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                                    'placeholder': 'Consultancy Name'}))

    phone_no = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                               'placeholder': 'Phone Number'}))

    website = forms.URLField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                            'placeholder': 'Website URL'}))

    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'placeholder': 'Password'}))

    rpt_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'placeholder': 'Retype Password'}))

