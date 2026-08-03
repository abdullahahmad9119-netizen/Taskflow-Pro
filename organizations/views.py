from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Organization,Membership,Invitations
from .serializers import OrganizationSerializer,MembershipSerializer, InvitaionCreateSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOrganizationMember

# ....................................ORGANIZATION VIEWS............................................

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

# ...........................................MEMBERSHIP VIEWS.............................................................
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


# .........................................INVITATION VIEW..............................................

class CreateInvitationView(APIView):
    def post(self, request, org_id):
        try:
            organization = Organization.objects.get(pk=org_id)
        except:
            return Response("organization doesnot exist")

        serializer = InvitaionCreateSerializer(
            data = request.data,
            context = {"org_id" : org_id,"request" : request }
        )
        if serializer.is_valid():
            serializer.save(organization = organization)
            return Response("invitations has been created", status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AcceptInvitationView(APIView):

    def post(self, request ,token):
        try :
            invite = Invitations.objects.get(token = token)
        except:
            return Response("invalid invite", status=status.HTTP_404_NOT_FOUND)

        if invite.is_accepted:
            return Response("invitation has already been used", status=status.HTTP_400_BAD_REQUEST)

        if not request.user.is_authenticated:
            return Response("you have to login to accept invitation " , status=status.HTTP_401_UNAUTHORIZED)
        if request.user.emails != invite.email:
            return Response("this invitation was sent to a different email", status=status.HTTP_403_FORBIDDEN)

        membership, created = Membership.objects.get_or_create(
            user = request.user,
            organizations = invite.organization,
            defaults = {"role" : invite.roll}
        )
        invite.is_accepted = True
        invite.save()

        return Response({
            "message": f"Successfully joined {invite.organization.name}!"
        }, status=status.HTTP_200_OK)

class ListInvitationsView(APIView):
    def get(self, request, org_id):
        try:
            organization = Organization.objects.get(org_id)
        except:
            return Response("organization doesnot exists", status=status.HTTP_404_NOT_FOUND)

        if not request.user.is_authenticated:
            return Response("you have to login to view invites", status=status.HTTP_401_UNAUTHORIZED)
        invitations = Invitations.objects.filter(organization_id = org_id )
        serializer = InvitaionCreateSerializer(invitations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class DeleteReviewInvitationView(APIView):
    def delete(self, request, invite_id):
        try:
            invite = Invitations.objects.get(invite_id)
        except:
            return Response("invitation not found", status=status.HTTP_404_NOT_FOUND )

        if not request.user.is_authenticated:
            return Response("unauthenticated", status=status.HTTP_401_UNAUTHORIZED)
        org = request.organization
        is_owner = (org.owner==request.user)
        is_Admin = Membership.objects.filter(
            user=request.user,
            organizations=org,
            role="admin"
        ).exists()
        if (is_owner and is_admin):
            return Response("you cannot revoke the invitations", status=status.HTTP_403_FORBIDDEN)

        invite.delete()
        return Response("invitation deleted", status=status.HTTP_204_NO_CONTENT)




