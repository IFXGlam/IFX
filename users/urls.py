from django.urls import path

from . import views

app_name = "user_profiles"

urlpatterns = [
    path("my-profile/",
         views.MyProfileView.as_view(), name='my_profile'),
]
