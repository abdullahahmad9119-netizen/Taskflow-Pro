from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from logs.models import Timelog
from .serializer import TimeLogSerializer
from rest_framework.response import Response
from rest_framework import status

class TimeLogListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, task_id):
        timelogs = Timelog.objects.filter(task_id=task_id)
        serializer = TimeLogSerializer(timelogs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, task_id):
        serializer = TimeLogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)




