from django.contrib import admin
from . import models


class ArticleModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'create_date', 'author']


admin.site.register(models.Article, ArticleModelAdmin)
