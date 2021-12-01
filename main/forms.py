from django import forms
from .models import MeetUrl,User
from django.contrib.auth.forms import UserCreationForm  
class MeetUrlModelForm(forms.ModelForm):
    class Meta:
        model = MeetUrl
        fields = '__all__'


# class CustomUserCreationForm(forms.ModelForm):
    
#     class Meta:
#         model = User
#         fields = ('username','email','password1','password2','is_staff')

class SignupForm(forms.Form):
    is_staff = forms.BooleanField(required=False,label="Staff")
    

    def signup(self, request, user):
        user.is_staff = self.cleaned_data['is_staff']

        user.save()

class CustomUserCreationForm(UserCreationForm):  
   
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)  
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)
    is_staff = forms.BooleanField() 
    
    class Meta:
        model = User
        # Note - include all *required* CustomUser fields here,
        # but don't need to include password1 and password2 as they are
        # already included since they are defined above.
        fields = ("username","email","is_staff",)

  
    def username_clean(self):  
        username = self.cleaned_data['username'].lower()  
        new = User.objects.filter(username = username)  
        if new.count():  
            raise ValidationError("User Already Exist")  
        return username  
  
    def email_clean(self):  
        email = self.cleaned_data['email'].lower()  
        new = User.objects.filter(email=email)  
        if new.count():  
            raise ValidationError(" Email Already Exist")  
        return email  
  
    def clean_password2(self):  
        password1 = self.cleaned_data['password1']  
        password2 = self.cleaned_data['password2']  
  
        if password1 and password2 and password1 != password2:  
            raise ValidationError("Password don't match")  
        return password2  
  
    def save(self, commit = True):  
        user = User.objects.create_user(  
            self.cleaned_data['username'],  
            self.cleaned_data['email'],  
            self.cleaned_data['password1'],
            self.cleaned_data['is_staff']  
        )  
        return user  