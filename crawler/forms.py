from django import forms

class AuthorForm(forms.Form):
    author_url = forms.CharField(label='Author Profile URL', max_length=255)