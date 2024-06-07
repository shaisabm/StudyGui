from django.forms import ModelForm
from .models import Room, Profile
from django.contrib.auth.models import User
from django.forms.widgets import ClearableFileInput
from django.utils.html import escape, conditional_escape
from django.utils.translation import gettext_lazy as _

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host','participants']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username','email']



class CustomClearableFileInput(ClearableFileInput):
    template_name = 'django/forms/widgets/clearable_file_input.html'
    intial_text = ('Currently')
    input_text = ('Change')

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['is_initial'] = False
        return context

class UserProfile(ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic','bio']
        exclude = ['user']
        widgets = {
            'profile_pic' : CustomClearableFileInput
        }

