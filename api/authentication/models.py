from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    This model allows you to customize User objects if needed.
    """
    def __str__(self):
        return str(self.username)
