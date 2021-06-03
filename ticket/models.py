from django.db import models

from django.conf import settings
from django.db.models import CharField, Value
from follow.models import UserFollows
from django.db.models import Subquery

# Create your models here.


class TicketManager(models.Manager):
    def get_by_user(self, username):
        tickets_by_user = self.filter(user=username)
        tickets_by_user = tickets_by_user.annotate(
            content_type=Value("TICKET", CharField())
        )
        return tickets_by_user

    def get_user_flux(self, username):
        # Get tickets to be included
        tickets_by_user = self.get_by_user(username)

        users_followed = UserFollows.objects.filter(user=username)
        tickets_by_followed_users = self.filter(
            user__in=Subquery(users_followed.values("followed_user"))
        )
        tickets_by_followed_users = tickets_by_followed_users.annotate(
            content_type=Value("TICKET", CharField())
        )

        tickets = tickets_by_user.union(tickets_by_followed_users)
        return tickets


class Ticket(models.Model):
    # Your Ticket model definition goes here
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    objects = TicketManager()
