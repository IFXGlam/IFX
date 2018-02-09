from builtins import super

from django.db.models import Q, Count
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, TemplateView, DetailView

from movies.forms import MovieForm, CollectionForm, SearchByYearForm
from movies.models import Movie, Collection, Tag, Field, MovieTagField, \
    Person, MovieRolePerson


class HomePage(TemplateView):
    template_name = 'movies/homePage.html'

    def get_context_data(self, **kwargs):
        d = super().get_context_data(**kwargs)
        d['set_jumbotron'] = 1
        return d


def about(request):
    return render(request, "movies/about.html", {'set_jumbotron': 2})


def searchresult(request):
    return render(request, "movies/searchresult.html", {'set_jumbotron': 3})


def movie_details(request):
    return render(request, "movies/movie_details.html", {'set_jumbotron': 3})


def movies_json(request):
    qs = Movie.objects.all()
    data = {
        'movies': [
            {
                'id': o.id,
                'title': o.title,
                'year': o.year,
                'lang': o.lang,
                'bid': o.bid,
            }
            for o in qs]
    }

    return JsonResponse(data)


MOVIE_ORDER_FIELDS = {
    'title_he',
    'title_en',
    'year',
}


class MovieListView(ListView):
    model = Movie
    paginate_by = 10

    def get_ordering(self):
        k = self.request.GET.get('order', None)
        if k not in MOVIE_ORDER_FIELDS:
            k = "title_he"
        return k


# def search_query(request):
#     q = request.GET.get('q', None)
#     selection = request.GET.get('idselect', None)
#
#     if selection == 'all':  # Select All
#         return search_all(request, q)
#     elif selection == 'title':  # Title
#         return search_title(request, q)
#     elif selection == 'year':  # Year/s
#         return search_year(request, q)
#     elif selection == 'director':  # Director
#         return search_director(request, q)
#

class MoviesSearchListView(MovieListView):
    def get_queryset(self):
        qs = super(MoviesSearchListView, self).get_queryset()
        query = self.request.GET.get('q')
        search_type = self.request.GET.get('idselect')
        q = self.get_filters(query, search_type)
        qs = qs.filter(q)

        return qs

    def get_filters(self, query, search_type):
        q = (
                Q(title_he__icontains=query) |
                Q(title_en__icontains=query) |
                Q(summary_he__icontains=query) |
                Q(summary_en__icontains=query)
        )
        if query.isdigit():
            q |= Q(year=int(query))
        return q

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class MovieDetailView(DetailView):
    model = Movie

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['set_jumbotron'] = 3
        return context


def movie_create(request):
    if request.method == "POST":
        form = MovieForm(request.POST)
        if form.is_valid():
            o = form.save()
            return redirect("movies:movie_detail", id=o.id)
    else:
        # method = GET
        form = MovieForm()

    d = {
        'form': form,
        'set_jumbotron': 3
    }
    return render(request, "movies/movie_form.html", d)


def collections_list(request):
    qs = Collection.objects.all()
    d = {
        'objects': qs,
    }
    return render(request, "movies/collections_list.html", d)


def collection_detail(request, id):
    c = get_object_or_404(Collection, id=id)
    d = {
        'collection': c,
    }
    return render(request, "movies/collection_detail.html", d)


def collection_create(request):
    if request.method == "POST":
        form = CollectionForm(request.POST)
        if form.is_valid():
            o = form.save()
            return redirect("movies:collection_detail", id=o.id)
    else:
        # method = GET
        form = CollectionForm()

    d = {
        'form': form,
    }
    return render(request, "movies/collection_form.html", d)


def search_by_year(request):
    print('search_by_year')
    print('request={}'.format(request))
    search_query = request.POST.get('q', None)
    print('search_query={}'.format(search_query))
    id_select = request.POST.get('idselect', None)
    print('id_select={}'.format(id_select))
    if request.method == "POST":
        form = SearchByYearForm(request.POST)
        if form.is_valid():
            o = form.save(commit=False)
            qs = Movie.objects.filter(year=o.year)
            d = {
                'objects': qs,
                'count': len(qs),
                'query': 'year={}'.format(str(o.year)),
            }
            return render(request, "movies/search_result.html", d)
    else:
        form = SearchByYearForm()

    d = {
        'form': form,
    }
    return render(request, "movies/search_form.html", d)


def search_year(request, q):
    if q.find('-') != -1:
        q_list = q.split('-')
        year1 = q_list[0]
        year2 = q_list[1]
        if year1.isdigit() and year2.isdigit():
            if year1 >= year2:
                results = Movie.objects.filter(year__gte=int(year2)).exclude(
                    year__gt=year1)
                query_str = 'Years={}-{}'.format(year2, year1)
                return search_results(request, results, query_str)
            elif year1 < year2:
                results = Movie.objects.filter(year__gte=int(year1)).exclude(
                    year__gt=year2)
                query_str = 'Years={}-{}'.format(year1, year2)
                return search_results(request, results, query_str)
    elif q.isdigit():
        results = Movie.objects.filter(year=int(q))
        query_str = 'Year={}'.format(q)
        return search_results(request, results, query_str)

    # If we are here, error occurred
    error = '"{}" - Error in format'.format(q)
    print(error)
    return search_results(request, [], error)


def search_results(request, results, query_str):
    d = {
        'objects': results,
        'count': len(results),
        'query': query_str,
        'set_jumbotron': 3,
    }
    return render(request, "movies/searchresult.html", d)


def search_title(request, query):
    qs = Movie.objects.filter(
        Q(title_he__icontains=query) | Q(title_en__icontains=query)
    )
    query_str = 'Title="{}"'.format(query)
    return search_results(request, qs, query_str)


def search_director(request, query):
    fields = Field.objects.filter(
        Q(title__icontains='במאי') | Q(title__icontains='director')
    )
    tags = Tag.objects.filter(title__icontains=query)
    qs = MovieTagField.objects.filter(Q(field__in=fields) & Q(tag__in=tags))
    results = []
    for item in qs:
        results.append(item.movie)

    query_str = 'Director="{}"'.format(query)
    return search_results(request, results, query_str)


def search_all(request, query):
    results = []

    q = (
            Q(title_he__icontains=query) |
            Q(title_en__icontains=query) |
            Q(summary_he__icontains=query) |
            Q(summary_en__icontains=query)
    )
    movies = Movie.objects.filter(q)
    for item in movies:
        results.append(item)

    tags = Tag.objects.filter(title__icontains=query)
    if tags:
        qs = MovieTagField.objects.filter(tag__in=tags)
        for item in qs:
            results.append(item.movie)

    if query.isdigit():
        qs = Movie.objects.filter(year=int(query))
        for item in qs:
            results.append(item)

    query_str = 'Search All="{}"'.format(query)
    return search_results(request, results, query_str)


def field_list(request):
    qs = Field.objects.annotate(movie_count=Count('movietagfield')).filter(
        movie_count__gt=0
    )
    d = {
        'objects': qs,
        'count': len(qs)
    }
    return render(request, "movies/field_list.html", d)


def field_detail(request, id):
    o = get_object_or_404(Field, id=id)
    qs = Tag.objects.filter(movietagfield__field=o).annotate(
        count=Count('movietagfield')).order_by('title')
    d = {
        'o': o,
        'tags': qs,
    }
    return render(request, "movies/field_detail.html", d)


TAG_ORDER_FIELDS = {
    'title',
    'lang',
    'type_id',
}


class TagListView(ListView):
    model = Tag
    paginate_by = 10

    def get_ordering(self):
        k = self.request.GET.get('order', None)
        if k not in TAG_ORDER_FIELDS:
            k = "title"
        return k


def tag_detail(request, id):
    o = get_object_or_404(Tag, id=id)
    d = {
        'o': o,
    }
    return render(request, "movies/tag_detail.html", d)


PERSON_ORDER_FIELDS = {
    'name_he',
    'name_en',
    'first_name_he',
    'first_name_en',
    'last_name_he',
    'last_name_en',
}


class PersonListView(ListView):
    model = Person
    paginate_by = 10

    def get_ordering(self):
        k = self.request.GET.get('order', None)
        if k not in PERSON_ORDER_FIELDS:
            k = "name_he"
        return k


def person_detail(request, id):
    o = get_object_or_404(Person, id=id)

    r = MovieRolePerson.objects.filter(person=o)
    d = {
        'o': o,
        'r': r,
    }
    return render(request, "movies/person_detail.html", d)
