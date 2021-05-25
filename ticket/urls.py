from django.conf.urls import url

from . import views  # import views so we can use them in urls.


urlpatterns = [
    url(r"^create_ticket", views.CreateTicket.as_view()),
]
