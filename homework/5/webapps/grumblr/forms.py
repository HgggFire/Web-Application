from django import forms
from django.contrib.auth.models import User
from models import *

class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length = 40)
    last_name = forms.CharField(max_length = 40)
    username = forms.CharField(max_length = 40)
    password = forms.CharField(max_length = 100)
    confirm_password = forms.CharField(max_length = 100)
    email = forms.CharField(max_length = 100)

    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(RegisterForm, self).clean()

        # Confirms that the andrewId is not already present in the
        # Student model database.
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('confirm_password')
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')

        # Checks the validity of the form data
        if not first_name:
            raise forms.ValidationError("First name is required.")
        if not last_name:
            raise forms.ValidationError("Last name is required.")
        if not email:
            raise forms.ValidationError("Email is required.")
        if not password:
            raise forms.ValidationError("Password is required.")
        if not password2:
            raise forms.ValidationError("Password confirmation is required.")
        if password != password2:
            raise forms.ValidationError('Passwords did not match.')
        if User.objects.filter(username=username):
            raise forms.ValidationError("Username is already taken.")

        # Generally return the cleaned data we got from our parent.
        return cleaned_data

# class EditProfForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         exclude = ('user', )

class EditProfileForm(forms.Form):
    # class Meta:
    #     widgets = {'picture' : forms.fileInput() }
    first_name = forms.CharField(max_length = 100)
    last_name = forms.CharField(max_length = 100)
    age = forms.IntegerField()
    bio = forms.CharField(max_length = 420)
    picture = forms.ImageField(required=False)

    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(EditProfileForm, self).clean()

        # Confirms that the andrewId is not already present in the
        # Student model database.
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        age = self.cleaned_data.get('age')
        bio = self.cleaned_data.get('bio')

        # Checks the validity of the form data
        if not first_name:
            raise forms.ValidationError("First name is required.")
        if not last_name:
            raise forms.ValidationError("Last name is required.")
        if not type(age) is int:
            raise forms.ValidationError("Age must be an integer.")
        if not age >= 0:
            raise forms.ValidationError("Age must be a positive integer.")
        if not bio:
            raise forms.ValidationError("Bio length is invalid.")

        # Generally return the cleaned data we got from our parent.
        return cleaned_data

class ChangePasswordForm(forms.Form):
    password = forms.CharField(max_length = 100)
    confirm_password = forms.CharField(max_length = 100)

    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(ChangePasswordForm, self).clean()

        # Confirms that the andrewId is not already present in the
        # Student model database.
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('confirm_password')

        # Checks the validity of the form data
        if not password:
            raise forms.ValidationError("Password is required.")
        if not password2:
            raise forms.ValidationError("Password confirmation is required.")
        if password != password2:
            raise forms.ValidationError('Passwords do not match.')

        # Generally return the cleaned data we got from our parent.
        return cleaned_data

class EmailResetForm(forms.Form):
    email = forms.CharField(max_length = 100)

    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(EmailResetForm, self).clean()

        # Confirms that the andrewId is not already present in the
        # Student model database.
        email = self.cleaned_data.get('email')

        # Checks the validity of the form data
        if not email:
            raise forms.ValidationError("Email is required.")
        if not User.objects.filter(email=email):
            raise forms.ValidationError("Email not registered.")

        # Generally return the cleaned data we got from our parent.
        return cleaned_data