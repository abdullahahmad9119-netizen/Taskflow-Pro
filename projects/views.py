from django.shortcuts import render
from rest_framework.views import APIView
from organizations.models import Membership, Organization
from .serializers import ProjectSerializer
from .models import Project
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
