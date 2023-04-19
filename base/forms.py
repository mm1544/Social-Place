from django.forms import ModelForm
from .models import Room


class RoomForm(ModelForm):
    class Meta:
        model = Room
        # All fields of Room obj. will be included in the AUTO-generated form
        fields = '__all__'