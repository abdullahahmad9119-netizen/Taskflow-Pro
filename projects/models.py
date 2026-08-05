from django.db import models
from organizations.models import Organization
from django.conf import settings
from users.models import User
class Project(models.Model):
    STATUS_CHOICES=[
        ("planning", "Planning"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("on_hold", "On Hold")
    ]
    PRIORITY_CHOICES=[
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("urgent", "Urgent")
    ]
    #ATTRIBUTES
    name = models.CharField(max_length = 40)
    description = models.TextField(blank=True ,null=True )
    status = models.CharField(choices = STATUS_CHOICES, default = "planning")
    priority = models.CharField(choices = PRIORITY_CHOICES, default = "medium")
    organization = models.ForeignKey(
        Organization,
        on_delete = models.CASCADE,
        related_name = "projects"
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        related_name = "created_projects",
        null = True
    )
    created_at = models.DateTimeField(auto_now_add = True)
    is_archived = models.BooleanField(default = False)

    def __str__(self):
        return self.name


class Tag(models.Model):

    name =  models.CharField(max_length=20)
    organization = models.ForeignKey(
        Organization,
        on_delete = models.CASCADE,
        related_name = "tags"
    )

class Task(models.Model):

    project = models.ForeignKey(
        Project,
        on_delete = models.CASCADE,
        related_name = "tasks")
    parent_task = models.ForeignKey(
        'self',
        blank = True,
        null = True,
        on_delete = models.CASCADE,
        related_name = 'subtasks')
    title = models.CharField(max_length = 100 )
    description = models.TextField(blank = True,  null = True)
    is_completed = models.BooleanField(default=False)
    tag = models.ManyToManyField(
        Tag,
        related_name = "tags")
    assignee = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
        blank = True,
        null = True,
        related_name = "tasks"
    )







