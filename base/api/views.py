from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import *
from .serializers import RoomSerializer
from django.http import JsonResponse

@api_view(['GET', 'POST'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/room/:id'
    ]
    return Response(routes)

@api_view(['GET', 'POST'])
def getRooms(request):
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
def getRoom(request, pk):
    room = Room.objects.get(id=pk)
    serializer = RoomSerializer(room)
    return Response(serializer.data)