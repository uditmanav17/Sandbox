from django.db import models
from movies.models import Movie
from tastypie.resources import ModelResource


# Create your models here.
class MovieResource(ModelResource):
    # use tastypie documentation to check classes it looks for
    class Meta:
        queryset = Movie.objects.all()
        resource_name = "movies"
        excludes = ["date_created"]
