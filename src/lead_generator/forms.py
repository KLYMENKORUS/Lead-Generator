from django import forms


class LeadForm(forms.Form):
    keywords = forms.CharField(label='Keywords', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Example: Restaurant, Hotel'}))
    location = forms.CharField(label='Location', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Example: San Francisco'}))



