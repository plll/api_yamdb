from django.contrib import admin

from .models import Genre, Category, Title


@admin.register(Genre)
class PostAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    list_editable = ('slug',)


@admin.register(Category)
class PostAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    list_editable = ('slug',)


@admin.register(Title)
class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year', 'description')
    search_fields = ('name',)
    list_editable = ('description',)
