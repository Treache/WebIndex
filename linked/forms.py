from django import forms
from .link_tools import retrieve_categories_as_list_of_tuples

# LoginForm
class LoginForm(forms.Form):
    username = forms.CharField(max_length=15)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)

# Signup form
class SignUpForm(forms.Form):
    username = forms.CharField(max_length=15)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=32, widget=forms.PasswordInput)
    terms_and_conditions = forms.BooleanField()

# User Profile Form
class UserProfileForm(forms.Form):
    email_address = forms.EmailField(label='E-Mail')
    display_name = forms.CharField(max_length=15)
    # bio = forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":20}))
    bio = forms.CharField(max_length=500, widget=forms.Textarea())


# To make new Links
class LinkForm(forms.Form):
    name = forms.CharField(max_length=20)
    domain = forms.CharField(max_length=25)
    url = forms.CharField(max_length=32, widget=forms.URLInput)
    category = forms.CharField(widget=forms.Select(choices=retrieve_categories_as_list_of_tuples()))
    description = forms.CharField(max_length=350, widget=forms.TextInput)
    
class ReviewForm(forms.Form):
    rate = forms.IntegerField(
        widget=forms.Select(choices=[(v, v) for v in range(1, 6)])
    )
    review = forms.CharField(max_length=350)
