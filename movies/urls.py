from django.conf.urls import url

from . import views

app_name = "movies"
urlpatterns = [
    url(r"^movies/$", views.movies_list, name='movies_list'),
    url(r"^movies/as-json/$", views.movies_json, name='movies_list_json'),
    url(r"^movies/add/$", views.movie_create, name='movie_create'),
    url(r"^movies/(?P<id>[0-9]+)/$", views.movie_detail, name='movie_detail'),
    url(r"^collections/$", views.collections_list, name='collections_list'),
    url(r"^collections/add/$", views.collection_create, name='collection_create'),
    url(r"^collections/(?P<id>[0-9]+)/$", views.collection_detail, name='collection_detail'),
    url(r"^homepage/$", views.homePage, name='homePage'),
    url(r"^about/$", views.about, name='about'),
    #url(r"^searchresult/$", views.MoviesSearchListView.as_view(), name='searchresult'),
    url(r"^searchresult/$", views.searchresult, name='searchresult'),
    url(r"^movie_details/$", views.movie_details, name='movie_details'),
    url(r"^search/year/$", views.search_by_year, name='search_by_year'),

]
