from django.contrib import admin

from .models import Genre, Movie


# custom class used to display different fields
class GenreAdmin(admin.ModelAdmin):
    # fields to display
    list_display = ("id", "name")


class MovieAdmin(admin.ModelAdmin):
    # fields to display
    # fields = ("title", "genre")
    # fields to exclude
    exclude = ("date_created",)
    list_display = ("title", "numbers_in_stock", "daily_rate")


# Register your models here.
admin.site.register(Genre, GenreAdmin)
admin.site.register(Movie, MovieAdmin)
