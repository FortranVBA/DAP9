"""Project OC DAP 9 - Account url file."""

from django.conf.urls import url

from . import views  # import views so we can use them in urls.


urlpatterns = [
    url(r"^login/", views.get_login_view, name="login"),
    url(r"^register/", views.register_user, name="register"),
]
