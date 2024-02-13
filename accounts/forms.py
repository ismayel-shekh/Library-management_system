from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import UserLibraryAccount

GENDER_TYPE = (
    ('Male', 'Male'),
    ('Female', 'Female'),
)
class UserLibraryForm(UserCreationForm):
    Name = forms.CharField(widget=forms.TextInput(attrs={'id': 'requeired'}))
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    gender = forms.ChoiceField(choices=GENDER_TYPE)

    class Meta:
        model = User
        fields =['username', 'Name','email','password1', 'password2', 'birth_date', 'gender',]
        # forms.save()
    def save(self, commit=True):
        our_user = super().save(commit=False)
        if commit == True:
            our_user.save()
            Name = self.cleaned_data.get('Name')
            birth_date = self.cleaned_data.get('birth_date')
            gender = self.cleaned_data.get('gender')
            UserLibraryAccount.objects.create(
                user = our_user,
                Name = Name,
                gender = gender,
                birth_date = birth_date,
                account_no = 1000+our_user.id
            )
        return our_user


class UserUpdateForm(forms.ModelForm):
    Name = forms.CharField(widget=forms.TextInput(attrs={'id': 'requeired'}))
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    gender = forms.ChoiceField(choices=GENDER_TYPE)

    class Meta:
        model = User
        fields =['Name','email', 'birth_date', 'gender',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        

        if self.instance:
            try:
                user_account = self.instance.account
            except UserLibraryAccount.DoesNotExist:
                user_account = None
            if user_account:
                self.fields['Name'].initial = user_account.Name
                self.fields['birth_date'].initial = user_account.birth_date
                self.fields['gender'].initial = user_account.gender
                print(user_account.Name)


    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            user_account, created = UserLibraryAccount.objects.get_or_create(user=user)
            user_account.Name = self.cleaned_data['Name']
            user_account.birth_date = self.cleaned_data['birth_date']
            user_account.gender = self.cleaned_data['gender']

            user_account.save()
        return user

