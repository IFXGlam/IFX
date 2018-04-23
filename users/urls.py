from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("my-profile/",
         views.MyProfileView.as_view(), name='my_profile'),
    path("oauth/",
         views.WikidataAuthView.as_view(), name='oauth'),
    path("oauth-callback/", views.WikidataAuthCallbackView.as_view(),
         name='oauth_callback'),
    path("oauth/delete/",
         views.WikidataLogoutAuthView.as_view(), name='oauth_logout'),
]
