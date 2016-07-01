from django import forms
from django.contrib.auth import authenticate,get_user_model

User = get_user_model()

class UserForm(forms.Form):
    username=forms.CharField(max_length=120)
    password=forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        username=self.cleaned_data.get('username')
        password=self.cleaned_data.get('password')

        if username and password:
            user=authenticate(username=username,password=password)
            if not user:
                raise forms.ValidationError('this user not exists')
            if not user.is_staff:
                raise forms.ValidationError('you should confirm your email first')
        return super(UserForm,self).clean()



# register form

class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField()
    password=forms.CharField(widget=forms.PasswordInput,label='password')
    password2=forms.CharField(widget=forms.PasswordInput,label='confirm password')
    class Meta:
        model=User
        fields=['username','email','password','password2']

    def clean_password2(self):
        password=self.cleaned_data.get('password')
        password2=self.cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError('password not match')
        return password