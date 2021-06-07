from django.db import models

from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from ticket.models import Ticket
from django.db.models import CharField, Value
from follow.models import UserFollows
from django.db.models import Subquery

# Create your models here.


class ReviewManager(models.Manager):
    def get_by_user(self, username):
        reviews_by_user = self.filter(user=username)
        reviews_by_user = reviews_by_user.annotate(
            content_type=Value("REVIEW", CharField())
        )

        return reviews_by_user

    def get_user_flux(self, username):
        reviews_by_user = self.get_by_user(username)

        users_followed = UserFollows.objects.filter(user=username)

        reviews_by_followed_users = self.filter(
            user__in=Subquery(users_followed.values("followed_user"))
        )
        reviews_by_followed_users = reviews_by_followed_users.annotate(
            content_type=Value("REVIEW", CharField())
        )

        tickets_by_user = Ticket.objects.get_by_user(username)
        reviews_reply = self.filter(ticket__in=Subquery(tickets_by_user.values("id")))
        reviews_reply = reviews_reply.annotate(
            content_type=Value("REVIEW", CharField())
        )

        reviews = reviews_by_user.union(reviews_by_followed_users)
        reviews = reviews.union(reviews_reply)

        return reviews


class Review(models.Model):
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        # validates that rating must be between 0 and 5
        validators=[MinValueValidator(0), MaxValueValidator(5)],
    )
    headline = models.CharField(max_length=128)
    body = models.TextField(max_length=8192, blank=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)
    objects = ReviewManager()
