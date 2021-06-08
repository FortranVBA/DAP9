"""Project OC DAP 9 - Follow models file."""

from django.db import models

from django.contrib.auth.models import User

# Create your models here.


class UserFollows(models.Model):
    """UserFollows model."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following",
    )
    followed_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="followed_by",
    )

    class Meta:
        """Form meta properties."""

        unique_together = (
            "user",
            "followed_user",
        )
