# Here are Serializers - classes that take certain model (or bject) that we want to serialize AND it will turned into JSON format(?). I.e. Python Obj will be converted into JSON Obj. Then we can return this object.

from rest_framework.serializers import ModelSerializer
from base.models import Room


class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'
