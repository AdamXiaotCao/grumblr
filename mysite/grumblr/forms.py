from django import forms

from django.contrib.auth.models import User
from models import *

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Person
        exclude = ('user', 'follows', 'blocks', 'description')
        widgets = {'picture' : forms.FileInput() }

    username = forms.CharField(max_length = 20)
    password1 = forms.CharField(max_length = 200,
                                label='Password',
                                widget = forms.PasswordInput())
    password2 = forms.CharField(max_length = 200,
                                label='Confirm password',
                                widget = forms.PasswordInput())


    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(RegistrationForm, self).clean()

        # Confirms that the two password fields match
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")

        # We must return the cleaned data we got from our parent.
        return cleaned_data


    # Customizes form validation for the username field.
    def clean_username(self):
        # Confirms that the username is not already present in the
        # User model database.
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")





# We must registrationformturn the cleaned data we got from the cleaned_data
        # dictionary
        return username
class EditForm(forms.ModelForm):
    class Meta:
        model = Person
        exclude = ('user','follows','blocks','email_address')
        widgets = {'picture' : forms.FileInput() }

    password1 = forms.CharField(max_length = 200,
                                    label='Password',
                                    widget = forms.PasswordInput())
    password2 = forms.CharField(max_length = 200,
                                    label='Confirm password',
                                    widget = forms.PasswordInput())



        # Customizes form validation for properties that apply to more
        # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
            # Calls our parent (forms.Form) .clean function, gets a dictionary
            # of cleaned data as a result
        cleaned_data = super(EditForm, self).clean()

        # Confirms that the two password fields match
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")

            # We must return the cleaned data we got from our parent.
        return cleaned_data

class ChangePasswordForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ('person','username', 'first_name','last_name','email','groups','user_permissions','is_staff','is_active','is_superuser',\
            'last_login','date_joined','password',)
    oldPassword = forms.CharField(max_length = 200, label= 'Old Password', widget = forms.PasswordInput())
    password1 = forms.CharField(max_length = 200, label= 'New Password', widget = forms.PasswordInput())
    password2 = forms.CharField(max_length = 200, label= 'Confirm New Password', widget = forms.PasswordInput())
    def clean(self):
        cleaned_data =super(ChangePasswordForm,self).clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        oldPassword = cleaned_data.get('oldPassword')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")
        return cleaned_data
class SetPasswordForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ('person','username', 'first_name','last_name','email','groups','user_permissions','is_staff','is_active','is_superuser',\
            'last_login','date_joined','password',)
    password1 = forms.CharField(max_length = 200, label= 'New Password', widget = forms.PasswordInput())
    password2 = forms.CharField(max_length = 200, label= 'Confirm New Password', widget = forms.PasswordInput())
    def clean(self):
        cleaned_data =super(ChangePasswordForm,self).clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")
        return cleaned_data

class GrumblForm(forms.ModelForm):
    class Meta:
        model = Grumbl
        exclude =('person','date','dislikes','comments')
    def clean(self):
        cleaned_data=super(GrumblForm,self).clean()
        return cleaned_data
