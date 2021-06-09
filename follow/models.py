"""Project OC DAP 9 - Follow models file."""

from django.db import models

from django.contrib.auth.models import User

# Create your models here.


class UserFollowsManager(models.Manager):
    """UserFollows model manager."""

    def follow_user(self, user, follow_user):
        """Create a follow relation between user and follow_user.

        Return the success/failure message.
        """
        if not User.objects.filter(username=follow_user).exists():
            return "Utilisateur inconnu."

        if str(follow_user) == str(user):
            return "Vous ne pouvez pas vous suivre vous-même."

        get_follow_user = User.objects.get(username=follow_user)
        if self.filter(user=user, followed_user=get_follow_user).exists():
            return "Vous suivez déjà cette personne."

        new_follow = UserFollows(user=user, followed_user=get_follow_user)
        new_follow.save()
        return "Abonnement ajouté"


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
    objects = UserFollowsManager()

    class Meta:
        """Form meta properties."""

        unique_together = (
            "user",
            "followed_user",
        )
