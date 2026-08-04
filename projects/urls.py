from django.urls import path
from .views import *
urlpatterns=[
    path('organizations/<int:org_id>/projects/',OrganizationProjectsListCreateView.as_view(), name="list-create-projects" ),
    path('projects/<int:pk>/', ProjectDetailView.as_view(), name="project-detail"),
    path('projects/<int:pk>/archive/',ProjectArchiveView.as_view(), name="project-archive")
]