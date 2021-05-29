from django.conf.urls import url

from . import views  # import views so we can use them in urls.


urlpatterns = [
    url(r"^login/", views.login_view, name = "login"),
    url(r"^register/", views.register, name = "register"),
]
