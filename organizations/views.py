from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Organization,Membership
from .serializers import OrganizationSerializer,MembershipSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOrganizationMember

class OrganizationListCreateAPIview(APIView):
    def get(self, request):
        user = request.user
        organizations = Organization.objects.filter(owner=user)
        serialzier = OrganizationSerializer(organizations ,many=True)
        return Response(serialzier.data, status=status.HTTP_200_OK)


    def post(self, request):
        serializer=OrganizationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class OrganizationDetailView(APIView):
    # PERMISSIOINS
    permission_classes = [IsAuthenticated,IsOrganizationMember]

    def get(self,request , pk):
        organization = get_object_or_404(Organization,pk=pk)
        self.check_object_permissions( request, organization)
        serializer = OrganizationSerializer(organization)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def put(self, request, pk):
        organization = get_object_or_404(Organization, pk=pk)
        self.check_object_permissions(request, organization)
        serializer = OrganizationSerializer(organization, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        organization = get_object_or_404(Organization, pk=pk)
        self.check_object_permissions(request, organization)
        organization.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# ........................................................................................................
class MembershipListCreateAPIView(APIView):
    def get(self, request):
        user = request.user
        membership = Membership.objects.filter(user=user)
        serializer = MembershipSerializer(membership , many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = MembershipSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MembershipDetailView(APIView):
    def get(self, request, pk):
        membership = get_object_or_404(Membership, pk=pk)
        serializer = MembershipSerializer(membership)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        membership = get_object_or_404(Membership, pk=pk)
        serializer = MembershipSerializer(membership, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,pk):
        membership = get_object_or_404(Membership, pk=pk)
        membership.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
