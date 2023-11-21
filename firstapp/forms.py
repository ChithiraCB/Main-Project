from django import forms
from .models import CustomUser, UserProfile1

class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('fullName','email' ,'phone')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class UserProfileForm(forms.ModelForm):
    
    class Meta:
        model = UserProfile1
        fields = ('address_line_1', 'address_line_2', 'city', 'state', 'country', 'pincode')

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'