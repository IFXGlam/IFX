from django.urls import path

from . import views

app_name = "people"

urlpatterns = [
    path("", views.PersonListView.as_view(), name='list'),
    path("<int:pk>/", views.PersonDetailView.as_view(), name='detail'),
    path("<int:pk>/edit/", views.PersonUpdateView.as_view(), name='edit'),
    path("<int:pk>/upload/", views.PostPersonToWikiDataView.as_view(),
         name='upload'),

    path("<int:pk>/merge-into/<int:other>/", views.MergeIntoView.as_view(),
         name='merge'),
]
