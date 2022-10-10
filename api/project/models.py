from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL

# ==================================== CONSTANTS

TYPE = (
        ("Back-end", "Back-End"),
        ("Front-end", "Front-End"),
        ("IOS", "IOS"),
        ("Android", "Android")
    )

ROLE = (
        ("Author", "Author"),
        ("Manager", "Manager"),
        ("Contributor", "Contributor")
    )

PERMISSION = (
        ("All", "All"),
        ("Restricted", "Restricted")
    )

# =================================================== PROJECT MODEL


class Project(models.Model):

    title = models.CharField(max_length=50, blank=False, unique=True)
    description = models.CharField(max_length=500)
    type = models.CharField(max_length=9, choices=TYPE)
    author_user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    constraints = [models.UniqueConstraint(fields=['author_user_id', 'title'], name="unique_contributor")]

    class Meta:
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'

    def __str__(self):
        return self.title

# =================================================== CONTRIBUTOR MODEL


class Contributor(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    permission = models.CharField(max_length=12, choices=PERMISSION, default="Restricted", editable=False)
    role = models.CharField(max_length=12, choices=ROLE, default="Contributor", editable=False)

    class Meta:
        verbose_name = 'Contributor'
        verbose_name_plural = 'Contributors'

    def __str__(self) -> str:
        return f"{self.user} - {self.role} - {self.project_id}"
