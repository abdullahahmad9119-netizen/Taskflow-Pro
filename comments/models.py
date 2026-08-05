from django.db import models
from django.conf import settings
from projects.models import Task

class Comment(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        related_name = "comments")
    task = models.ForeignKey(
        Task,
        on_delete = models.CASCADE,
        related_name = "comments")
    parent_comment= models.ForeignKey(
        "self",
        on_delete = models.CASCADE,
        related_name = "replies")
    body = models.TextField(blank = True, null = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now=True)

    def __Str__(self):
        return f"comment by {self.author} on task {self.task.title}"

