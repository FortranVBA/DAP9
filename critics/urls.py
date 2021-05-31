from django.conf.urls import url

from . import views  # import views so we can use them in urls.


urlpatterns = [
    url(r"^$", views.flux, name="flux"),
    url(r"^create_review/", views.create_review, name="create_review"),
]
