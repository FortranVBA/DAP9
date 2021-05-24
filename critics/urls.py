from django.conf.urls import url

from . import views  # import views so we can use them in urls.


urlpatterns = [
    #    url(r"^register/", views.register),
    url(r"^register/", views.register),
    url(r"^reg_success/", views.reg_success, name="registration_success"),
]
