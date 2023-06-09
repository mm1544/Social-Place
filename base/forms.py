from django.forms import ModelForm
from .models import Room
from django.contrib.auth.models import User


class RoomForm(ModelForm):
    class Meta:
        model = Room
        # All fields of Room obj. will be included in the AUTO-generated form
        fields = '__all__'
        # Those fields will not be added in autogenerated form
        exclude = ['host', 'participants']

class UserForm(ModelForm):
    class Meta:
        model = User
        # Specify the fields which you want to include in the form.
        fields = ['username', 'email']
        # fields = '__all__'