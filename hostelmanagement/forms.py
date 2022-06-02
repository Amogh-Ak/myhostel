from django import forms
from django.contrib.auth.forms import   PasswordResetForm, UserCreationForm,AuthenticationForm, UsernameField,UsernameField,PasswordChangeForm, SetPasswordForm
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _
from django.forms import ValidationError, fields, widgets
from django.contrib.auth import password_validation

from .models import CustomUser, Facilities, Hostel, HostelDetail, OwnerDetail, Room

class HostelForm(forms.ModelForm):
    hostelimage = forms.ImageField()
    class Meta:
        model = Hostel
        fields= ["name","location","zipcode","type_of_hostel","description","hostelimage","food_facility"]
        exclude = ["slug","usr","views","status","details","facilities","room"]
        widgets = {'type_of_hostel':forms.Select(),'food_facility':forms.Select()}

class RoomForm(forms.ModelForm):
    room_imgs = forms.ImageField()
    class Meta:
        model = Room
        fields= ["room_number","number_of_students","status","room_cost","room_imgs"]
        exclude = ["usr","hostel_name"]

    def clean_room_number(self):
        room_number = self.cleaned_data["room_number"]
        roomNo = str(room_number)

        if not roomNo.isdecimal():
            raise forms.ValidationError("Room Number can only be Numbers.")
        return room_number

    def clean_number_of_students(self):
        number_of_students = self.cleaned_data["number_of_students"]
        noOfStudent = str(number_of_students)

        if not noOfStudent.isdecimal():
            raise forms.ValidationError("Invalid Input.")
        return number_of_students

    def clean_room_cost(self):
        room_cost = self.cleaned_data["room_cost"]
        roomCost = str(room_cost)

        if not roomCost.isdecimal():
            raise forms.ValidationError("Room Cost can only be Numbers")
        return room_cost

class HostelDetailsForm(forms.ModelForm):
    class Meta:
        model = HostelDetail
        fields = "__all__"
        exclude = ["usr"]

class FacilityForm(forms.ModelForm):
    class Meta:
        model = Facilities
        fields = "__all__"

class OwnerForm(forms.ModelForm):
    profilePic = forms.ImageField()
    class Meta:
        model = OwnerDetail
        fields = "__all__"
        exclude = ["usr"]
        widgets = {'name':forms.TextInput(attrs={'class':'cust-form-control'})}


class UserRegisterForm(UserCreationForm):
    
    password1 = forms.CharField(label="Password",widget=forms.PasswordInput(attrs={'class':'form-control'})) #passing bootstrap class name to attrs to design in custom way.
    password2 = forms.CharField(label="Confirm Password (again)",widget=forms.PasswordInput(attrs={'class':'form-control'}))
    email = forms.CharField(required=True,widget=forms.EmailInput(attrs={'class':'form-control'}))
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ['username','email','password1','password2','is_Owner','is_Student']
        labels = {'email':'Email'}
        widgets = {'username':forms.TextInput(attrs={'class':'form-control'}),'is_Owner':forms.CheckboxInput(attrs={'class':'form-check-input'}),'is_Student':forms.CheckboxInput(attrs={'class':'form-check-input'})}

class LoginForm(AuthenticationForm):

    username = UsernameField(widget=forms.TextInput(attrs={'autofocus':True}))
    password = forms.CharField(label=_("Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'current-password'}))


class ChangePasswordForm(PasswordChangeForm):

    old_password = forms.CharField(label=_("Old Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus':True,  'class':'form-control'}))
    new_password1 = forms.CharField(label=_("New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class':'form-control'}), help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_("Confirm New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','class':'form-control'}))


class ResetPasswordForm(PasswordResetForm):

    email = forms.EmailField(label=("Email"),max_length=254,widget=forms.EmailInput(attrs={'autocomplete':'email','class':'form-control'}))

class SetPasswordForm(SetPasswordForm):

    new_password1 = forms.CharField(label=_("New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class':'form-control'}), help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_("Confirm New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','class':'form-control'}))


# class CustomerProfileForm(forms.ModelForm):

#     class Meta:
#         model = Customer
#         fields = ['name','locality','city','state','zipcode']
#         widgets = {'name':forms.TextInput(attrs={'class':'form-control'}),'locality':forms.TextInput(attrs={'class':'form-control'}), 'city':forms.TextInput(attrs={'class':'form-control'}), 
#     'state':forms.Select(attrs={'class':'form-control'}),
#     'zipcode':forms.NumberInput(attrs={'class':'form-control'})}