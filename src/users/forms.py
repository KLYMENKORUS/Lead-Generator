from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model


User = get_user_model()


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username'}
    ))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}
    ))

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            queryset = User.objects.filter(username=username)
            if not queryset.exists():
                raise forms.ValidationError(f'User with this username {username} not already exists')

            if not check_password(password, queryset[0].password):
                raise forms.ValidationError(f'Password is incorrect')

            user = authenticate(username=username, password=password)

            if not user:
                raise forms.ValidationError(f'User {username} has been banned')

            return super(LoginForm, self).clean(*args, **kwargs)


class UserSignUpForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Come up with a username'}))
    first_name = forms.CharField(widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Enter your the first name'}))
    last_name = forms.CharField(widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Enter your the last name'}))
    email = forms.EmailField(required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter your the email'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Come up with a password'}))
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Repeat password'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'password2']

    def clean_password2(self):
        data = self.cleaned_data
        if data.get('password') != data.get('password2'):
            raise forms.ValidationError('Password missmatch')
        return data.get('password2')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                'A user with this username already exists!'
            )
        return username


class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Enter your the first name'}))
    last_name = forms.CharField(widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Enter your the last name'}))
    keyword = forms.CharField(label='Keyword', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Example: Restaurant, Hotel'}),
                              required=False)
    location = forms.CharField(label='Location', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Example: San Francisco'}),
                               required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'keyword', 'location']

