
from django import forms
from .models import Users, Profile,Language,Genre

class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['first_name', 'last_name', 'email', 'password']
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['PName', 'language', 'genres']

    PName = forms.CharField(max_length=255)
    language = forms.ModelChoiceField(queryset=Language.objects.all())
    genres = forms.ModelMultipleChoiceField(queryset=Genre.objects.all(), widget=forms.CheckboxSelectMultiple)


    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        # Query all languages from the database
        self.fields['language'].choices = Language.objects.all().values_list('LID', 'LName')
        # self.fields['genres'].choices = Language.objects.all().values_list('GID', 'GName')


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['PName', 'language']

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        # Query all languages from the database
        self.fields['language'].choices = Language.objects.all().values_list('LID', 'LName')

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class CreateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['PName','language']

# from django import forms
# from django.contrib.auth.forms import ReadOnlyPasswordHashField
# from .models import Users, Profile

# class UserRegistrationForm(forms.ModelForm):
#     password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
#     password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

#     class Meta:
#         model = Users
#         fields = ('first_name', 'last_name', 'email')

#     def clean_password2(self):
#         # Check that the two password entries match
#         password1 = self.cleaned_data.get("password1")
#         password2 = self.cleaned_data.get("password2")
#         if password1 and password2 and password1 != password2:
#             raise forms.ValidationError("Passwords don't match")
#         return password2

#     def clean_email(self):
#         # Check for existing email
#         email = self.cleaned_data.get("email")
#         try:
#             user = Users.objects.get(email=email)
#             raise forms.ValidationError("Email already registered")
#         except Users.DoesNotExist:
#             return email

#     def save(self, commit=True):
#         # Save the provided password in hashed format
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data["password1"])
#         if commit:
#             user.save()
#         return user
