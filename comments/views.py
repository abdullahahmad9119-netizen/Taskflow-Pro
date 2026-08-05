from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Comment
from .serializer import CommentSerializer

class CommentListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, task_id):

        comments = Comment.objects.filter(task_id=task_id, parent_comment__isnull=True)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, task_id):

        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, task_id, pk):

        try :
            comment = Comment.objects.get(task_id=task_id, pk=pk)
        except :
            return Response("comment does not exists", status=status.HTTP_404_NOT_FOUND)


        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def put(self, request, task_id, pk):

        try :
            comment = Comment.objects.get(task_id=task_id, pk=pk)
        except Comment.DoesNotExist:
            return Response("comment does not exists", status=status.HTTP_404_NOT_FOUND)

        if request.user != comment.author:
            return Response("you cannot edit someone else's comment", status=status.HTTP_403_FORBIDDEN)
        serializer = CommentSerializer(data=request.data, instance=comment, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response("comment edited", status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, task_id, pk):

        try:
            comment = Comment.objects.get(task_id=task_id, pk=pk)
        except:
            return Response("comment does not exists", status=status.HTTP_404_NOT_FOUND)

        if request.user != comment.author:
            return Response("you cannot delete someone else's comment", status=status.HTTP_403_FORBIDDEN)

        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
