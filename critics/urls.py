from django.conf.urls import url

from . import views  # import views so we can use them in urls.


urlpatterns = [
    url(r"^$", views.flux, name="flux"),
    url(r"^create_review/", views.create_review, name="create_review"),
    url(r"^review/(?P<ticket>[0-9]+)$", views.reply_review, name="review"),
    url(r"^myposts/", views.myposts, name="myposts"),
    url(r"^delete_review/(?P<review>[0-9]+)$", views.review_delete, name="del_review"),
    url(r"^delete_ticket/(?P<ticket>[0-9]+)$", views.ticket_delete, name="del_ticket"),
    url(
        r"^update_review/(?P<pk>[0-9]+)$",
        views.ReviewUpdateView.as_view(),
        name="update_review",
    ),
]
