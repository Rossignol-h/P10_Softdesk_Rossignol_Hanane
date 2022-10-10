from project.models import Project
from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL

# ==================================== CONSTANTS

TAG = (
        ("Bug", "Bug"),
        ("Improvement", "Improvement"),
        ("Task", "Task")
    )
PRIORITY = (
        ("Hight", "Hight"),
        ("Medium", "Medium"),
        ("Low", "Low")
    )
STATUS = (
        ("ToDo", "ToDo"),
        ("InProgress", "InProgress"),
        ("Completed", "Completed")
    )

# =================================================== ISSUE MODEL


class Issue(models.Model):

    priority = models.CharField(max_length=12, choices=PRIORITY)
    status = models.CharField(max_length=12, choices=STATUS)
    tag = models.CharField(max_length=12, choices=TAG)
    description = models.CharField(max_length=5000)
    title = models.CharField(max_length=50)
    assignee_user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="assignee")
    author_user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Issue'
        verbose_name_plural = 'Issues'

    def __str__(self):
        return self.title

# =================================================== COMMENT MODEL


class Comment(models.Model):

    description = models.CharField(max_length=500, blank=False)
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    author_user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    issue_id = models.ForeignKey(Issue, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.description)
