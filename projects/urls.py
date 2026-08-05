from django.urls import path
from .views import *
urlpatterns=[
    path('organizations/<int:org_id>/projects/',OrganizationProjectsListCreateView.as_view(), name="list-create-projects" ),
    path('projects/<int:pk>/', ProjectDetailView.as_view(), name="project-detail"),
    path('projects/<int:pk>/archive/',ProjectArchiveView.as_view(), name="project-archive"),

    path('projects/<int:project_id>/tasks/',TaskListCreateView.as_view(),name='task-list-create',),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('tasks/bulk-create/', BulkTaskCreateView.as_view(), name='task-bulk-create',),
    path('tasks/bulk-update-status/',BulkStatusUpdateView.as_view(),name='task-bulk-update-status'),
    path('tasks/<int:pk>/mark-done/', TaskMarkDoneView.as_view(), name='task-mark-done'),
    path('tasks/<int:pk>/assign-to-me/', TaskAssignToMeView.as_view(), name='task-assign-to-me'),
    path('tasks/<int:pk>/move-to-project/', TaskMoveToProjectView.as_view(), name='task-move-to-project'),
    path('me/tasks/', MyTaskListView.as_view(), name='my-tasks-list')
]