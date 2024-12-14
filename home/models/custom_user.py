from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # determine if this is the firt login for the user or not
    default_password = models.BooleanField(default=True)  # Track if password needs changing

    # users and sub-user relation
    parent = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True, related_name='sub_users'
    )

    def __str__(self):
        return self.username

    @property
    def is_master(self):
        return self.parent is None

    def save(self, *args, **kwargs):
        # Prevent a master user from being added as a sub-user
        if self.parent and self.parent.parent is not None:
            raise ValueError("A master user cannot be added as a sub-user.")
        super().save(*args, **kwargs)

