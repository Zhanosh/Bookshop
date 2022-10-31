from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Article


class ArticleView(ListView):
    template_name = 'article_module/article-page.html'
    model = Article
    paginate_by = 15
    context_object_name = 'articles'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ArticleView, self).get_context_data()
        return context

    def get_queryset(self):
        query = super(ArticleView, self).get_queryset()
        return query


class ArticleDetailView(DetailView):
    template_name = 'article_module/article-detail.html'
    model = Article
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data()
        return context

    def get_queryset(self):
        query = super(ArticleDetailView, self).get_queryset()
        return query
