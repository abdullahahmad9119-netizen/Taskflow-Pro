from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from .filters import TaskFilter
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from organizations.models import Membership, Organization
from .serializers import ProjectSerializer, TaskSerializer, BulkTaskCreateSerializer, TaskAttachmentSerializer
from .models import Project, Task, TaskAttachment
from .permissions import IsProjectManagerOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.parsers import FormParser,MultiPartParser

# ....................................PROJECT VIEWS...................................................


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
            return Response("not a member of the organization", status=status.HTTP_403_FORBIDDEN)

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

#.............................................TASK VIEWS..................................................


class TaskListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, project_id):
        project = get_object_or_404(Project, pk=project_id)
        tasks = Task.objects.filter(project=project, parent_task__isnull=True)
        serializer = TaskSerializer(instance= tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, project_id):
        project = get_object_or_404(Project, pk=project_id)
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(project=project)
            return Response (serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        serializer = TaskSerializer(instance=task)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        task.delete()
        return Response( status=status.HTTP_204_NO_CONTENT)


class BulkTaskCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self,request):
        serializer = BulkTaskCreateSerializer(data=request.data, many=True )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BulkStatusUpdateView(APIView):

    permission_classes = [IsAuthenticated]

    def patch(self, request):

        task_ids = request.data.get("tasks_ids", [])
        is_completed = request.data.get("is_completed")

        if task_ids or is_completed is None:
            return Response("both id and status are required", status=status.HTTP_400_BAD_REQUEST)

        updated_count = Task.objects.filter(id__in=task_ids).update(is_completed=is_completed)
        return Response(f"successfully updated {updated_count} tasks", status=status.HTTP_200_OK)


class TaskMarkDoneView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        task = get_object_or_404(Task,pk=pk)
        task.is_completed=True
        task.save()
        return Response(status=status.HTTP_200_OK)


class TaskAssignToMeView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        task.assignee=request.user
        task.save()
        return Response("task has been assigned to you", status=status.HTTP_200_OK)


class TaskMoveToProjectView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):

        task = get_object_or_404(Task, pk=pk)

        new_project_id = request.data.get("project_id")
        if not new_project_id:
            return Response("project id is required", status=status.HTTP_400_BAD_REQUEST)
        task.project_id = new_project_id
        task.save()
        return Response(status=status.HTTP_200_OK)


class MyTaskListView(ListAPIView):

    queryset = Task.objects.select_related("project","assignee").all()
    serializer_class = TaskSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,]
    filterset_class = TaskFilter

    search_fields = ["title", "description"]
    ordering_fields = ["due_date", "priority", "created_at"]
    ordering = ["due_date" ]



 # ......................................TaskAttachmentViews...................................................



class TaskAttachmentListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    parser_classes = [FormParser, MultiPartParser]

    def get(self, request, task_id):
        attachemnts = TaskAttachment.objects.filter(task_id=task_id)
        serializer = TaskAttachmentSerializer(attachemnts, many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)

    def post(self, request, task_id):
        # task = get_object_or_404(Task, pk=task_id)
        serializer = TaskAttachmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskAttachmentDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, task_id, pk):

        try:
            attachment = TaskAttachment.objects.get(task_id=task_id, pk=pk)
        except TaskAttachment.DoesNotExist:
            return Response("attachment does not exists", status=status.HTTP_404_NOT_FOUND)

        serializer = TaskAttachmentSerializer(attachment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, task_id, pk):

        try :
            attachment = TaskAttachment.objects.get(task_id=task_id, pk=pk)
        except TaskAttachment.DoesNotExist:
            return Response("attachment does not exists", status=status.HTTP_404_NOT_FOUND)

        if request.user != attachment.uploaded_by:
            return Response("you cannot delete this attachment as you are not the author", status=status.HTTP_403_FORBIDDEN)

        attachment.delete()
        return Response("attachment deleted",status=status.HTTP_200_OK )

