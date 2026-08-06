from django.urls import path
from .views import *

urlpatterns=[
    path('tasks/<int:task_id>/comments/',CommentListCreateView.as_view(),name='comment-list-create',),
    path('tasks/<int:task_id>/comments/<int:pk>/',CommentDetailView.as_view(),name='comment-detail',),
]



