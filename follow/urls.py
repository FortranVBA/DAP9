from django.conf.urls import url

from . import views  # import views so we can use them in urls.


urlpatterns = [
    url(r"^$", views.follow, name="follow"),
    url(r"^unfollow/(?P<userfollows>[0-9]+)$", views.unfollow, name="unfollow"),
]
