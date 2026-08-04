from django.shortcuts import render
from rest_framework.views import APIView
from organizations.models import Membership, Organization
from .serializers import ProjectSerializer
from .models import Project
from .permissions import IsProjectManagerOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

class OrganizationProjectsListCreateView(APIView):

    def get(self, request, org_id):
        if not (request.user == Membership.objects.filter(user=request.user , organization_id = org_id )):
            return Response("not a memeber of the organization", status=status.HTTP_403_FORBIDDEN)
        projects = Project.objects.filter(
            organization_id = org_id, is_archived=False)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, org_id):
        if not (request.user == Membership.objects.filter(user=request.user , organization_id = org_id )):
            return Response("not a memeber of the organization", status=status.HTTP_403_FORBIDDEN)

        if Membership.role not in ['ADMIN', 'MANAGER']:
            return Response("only admins and managers can create projects", status=status.HTTP_403_FORBIDDEN)

        organization = get_object_or_404(Organization, id=org_id)
        serializer = ProjectSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("project created", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectDetailView(APIView):

    permission_classes = [IsAuthenticated,IsProjectManagerOrReadOnly]

    def get_object(self, pk):
        project = get_object_or_404(Project, pk= pk)
        self.check_object_permissions(self.request, project)
        return project

    def patch(self, request, pk):
        project = self.get_object(pk = pk)
        serializer = ProjectSerializer(project, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request, pk):
        project = self.get_object(pk)
        serializer = ProjectSerializer(instance = project)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        project = self.get_object(pk)
        project.delete()
        return Response("project deleted successfully", status=status.HTTP_200_OK)
class ProjectArchiveView(APIView):

     permission_classes = [IsAuthenticated, IsProjectManagerOrReadOnly]

     def get_object(self, pk):
         project = get_object_or_404(Project, pk=pk)
         self.check_object_permissions(self.request, project)
         return project
     def post(self, request, pk):
         project = self.get_object(pk=pk)
         project.is_archived = not project.is_archived
         project.save()
         return Response("archived", status=status.HTTP_200_OK)

