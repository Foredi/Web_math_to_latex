from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.core.exceptions import ValidationError
from .models import Images, User

User = User

class RegisterForm(forms.ModelForm):
    """
    The default registration form for users.
    """
    username = forms.CharField(max_length=100,required=True,
                               widget=forms.TextInput(attrs={
                                                             'class': 'form-control',
                                                             'id': "inputUsername"
                                                             }))
    email = forms.EmailField(required=True,widget=forms.TextInput(attrs={
                                                           'class': 'form-control',
                                                           'id': 'inputEmail',
                                                           }))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'inputPassword',
                                                                  }))
    password_2 = forms.CharField(required=True, label='Confirm Password', widget=forms.PasswordInput(attrs={
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'inputPassword2',
                                                                  }))
    
    checkbox = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input',
                                                                                     'id': 'gridCheck'
                                                                                     }))

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_2', 'checkbox']

    def clean_username(self):
        '''
        Verify username is available.
        '''
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError("Username is taken")
        return username

    def clean(self):
        '''
        Verify both passwords match.
        '''
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")
        if password is not None and password != password_2:
            self.add_error("password_2", "Your passwords must match")

        return cleaned_data

class PasswordChangeForm1(PasswordChangeForm):
    def clean_old_password(self):
        old_password = self.cleaned_data.get("old_password")
        if not self.user.check_password(old_password):
            raise ValidationError("Mật khẩu cũ không đúng")
        return old_password

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']

class UserAdminCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password = forms.CharField(widget=forms.PasswordInput)
    password_2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username']

    def clean(self):
        '''
        Verify both passwords match.
        '''
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")
        if password is not None and password != password_2:
            self.add_error("password_2", "Your passwords must match")
        return cleaned_data

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    # password = ReadOnlyPasswordHashField()
    password = forms.CharField(widget=forms.PasswordInput)
    password_2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'is_active']

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]



class LoginForm(AuthenticationForm):
    username = forms.CharField(label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'type': 'text',
            'autofocus': True,
            'required': 'required'
        })
    )
    
    password = forms.CharField(label='', 
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'name': 'password',
            'required': 'required'
        }),
    )

    remember_me = forms.BooleanField(required=False, label='Remember Me')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class ImageForm(forms.ModelForm):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control mb-3',
            'placeholder': 'Enter name',
            'required': 'required'
        })
    )
    image = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control mb-3',
            'required': 'required'
        })
    )

    class Meta:
        model = Images
        fields = ['name', 'image']