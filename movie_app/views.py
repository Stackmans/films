from django.shortcuts import render, get_object_or_404
from .models import Movie
from django.db.models import F, Sum, Max, Min, Count, Avg, Value

# Create your views here.


def show_all_movie(request):
    movies = Movie.objects.all()
    agg = movies.aggregate(Avg('budget'), Min('rating'), Max('rating'), Count('id'))

    return render(request, 'movie_app/all_movies.html', {
        'movies': movies,
        'agg': agg
    })


def show_one_movie(request, slug_movie: str):
    movie = get_object_or_404(Movie, slug=slug_movie)
    return render(request, 'movie_app/one_movie.html', {
        'movie': movie
    })
