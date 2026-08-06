from django.db import models
from projects.models import Task
from django.conf import settings

class Timelog(models.Model):

    task = models.ForeignKey(
        Task,
        on_delete = models.CASCADE,
        related_name = "timelogs")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
        related_name = "timelogs")
    hours_spent = models.FloatField()
    work_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add = True)





