from django.http import HttpResponse
from django.http.response import Http404
from django.shortcuts import get_object_or_404, render

from .models import Movie


# Create your views here.
def index(request):
    # select * from movies_movie
    # Movie.objects.all()
    # select * from movies_movie where
    # Movie.objects.filter(release_year=1994)
    # fetch one object
    # Movie.objects.get(id=1)
    movies = Movie.objects.all()
    titles = ", ".join([m.title for m in movies])
    # return HttpResponse(titles)
    return render(request, "movies/index.html", context={"movies": movies})


def detail(request, movie_id):
    # pk is primary key
    # movie = Movie.objects.get(pk=movie_id)
    movie = get_object_or_404(Movie, pk=movie_id)
    return render(request, "movies/detail.html", context={"movie": movie})
