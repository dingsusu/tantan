from django.forms import ModelForm
from django import forms
from user.models import User
from user.models import Profile


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['nickname','gender','birthday','location']


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'

    def clean_max_distance(self):
        cleaned_data = self.clean()
        max_distance = cleaned_data.get('max_distance')
        min_distance = cleaned_data.get('min_distance')

        if max_distance < min_distance:
            raise forms.ValidationError('max_distance 必须大雨min_distance')
        return max_distance

    def clean_max_dating_age(self):
        clean_data = self.clean()
        max_dating_age = clean_data.get('max_dating_age')
        min_dating_age = clean_data.get('min_dating_age')

        if max_dating_age < min_dating_age:
            raise forms.ValidationError('max_dating_age 必须大雨Min')
        return max_dating_age


