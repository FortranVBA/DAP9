from django.conf.urls import url

from . import views  # import views so we can use them in urls.


urlpatterns = [
    url(r"^$", views.get_follow_view, name="follow"),
    url(r"^unfollow/(?P<userfollows>[0-9]+)$", views.unfollow_user, name="unfollow"),
]
