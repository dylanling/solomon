from django import forms

class AuthorForm(forms.Form):
    author_id = forms.IntegerField(label='Author ID: ', min_value=1)