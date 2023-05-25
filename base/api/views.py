from rest_framework.decorators import api_view  # Dj Rest framework
from rest_framework.response import Response
from base.models import Room
from .serializers import RoomSerializer

# Views can be either Class based or Function based.


@api_view(['GET'])  # Specifying http requests that are allowed
# Will list all the endpoints
def getRoutes(request):
    routes = [
        # To get API home page
        'GET /api',
        # Will give JSON array of objects of all the rooms in the database
        'GET /api/rooms',
        # Will give data/info about specific room
        'GET /api/rooms/:id'
    ]

    return Response(routes)


@api_view(['GET'])
# To get all the existing rooms
def getRooms(request):
    rooms = Room.objects.all()
    # !!! We are getting here Python query set and we can't return that. !! Python Objects can't be converted automatically to JSON objects. Therefore we will use here Serializer.
    # 'many=True' -> indicates if serializing multiple objects. In our case we are serializing query set, so there are many objects.
    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getRoom(request, pk):
    room = Room.objects.get(id=pk)
    serializer = RoomSerializer(room, many=False)
    return Response(serializer.data)
