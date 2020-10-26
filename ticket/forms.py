from django import forms
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()


class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=10)
    first_name = forms.CharField(label="First Name")
    last_name = forms.CharField(label="Last Name")
    email = forms.EmailField(label='Email address')
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [

            'first_name',
            'last_name',
            'username',
            'email',
            'password',
            'confirm_password',

        ]

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = 'Enter a valid e-mail'


class UserLoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Username'

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            print(user)
            if not user:
                raise forms.ValidationError('This user does not exist')
            if not user.check_password(password):
                raise forms.ValidationError('Incorrect password')
            if not user.is_active:
                raise forms.ValidationError('This user is not active')
        return super(UserLoginForm, self).clean(*args, **kwargs)




Departments = (
    ('PWSLab DevOps Support', 'PWSLab DevOps Support'),
    ('iSupport', 'iSupport' ),
)

Categories = (
    ( 'none', 'none' ),
    ( 'NEW Project CI/CD Pipeline Setup', 'NEW Project CI/CD Pipeline Setup' ),
    ( 'Update CI/CD Pipeline Configuration', 'Update CI/CD Pipeline Configuration' ),
    ( 'DevSecOps Pipeline Setup', 'DevSecOps Pipeline Setup' ),
    ( 'CI/CD pipeline failure', 'CI/CD pipeline failure' ),
    ( 'Automated Deployment failure', 'Automated Deployment failure' ),
    ( 'Docker and Containers', 'Docker and Containers' ),
    ( 'Others', 'Others' ),
)

Priorities = (
    ( 'none', 'none' ),
    ( 'High - Production System Down', 'High - Production System Down' ),
    ( 'Medium - System Impaired', 'Medium - System Impaired' ),
    ( 'Low - General Guidance', 'Low - General Guidance' ),
)

class NewTicketForm(forms.Form):
    department = forms.ChoiceField(label='Department', choices=Departments)
    category = forms.ChoiceField(label='Category', choices=Categories)
    subject = forms.CharField(label='Subject')
    description = forms.CharField(label='Description')
    priority = forms.ChoiceField(label='Priority', choices=Priorities)

    name = forms.CharField(label='Name')
    email = forms.CharField(label='Email')


class UpdateTicketForm(forms.Form):
    subject = forms.CharField(label='Subject')
    description = forms.CharField(label='Description')
    priority = forms.ChoiceField(label='Priority', choices=Priorities)
