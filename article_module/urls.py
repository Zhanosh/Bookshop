from django.urls import path
from . import views

urlpatterns = [
    path('', views.ArticleView.as_view(), name='article-page'),
    path('detail/<slug:slug>/', views.ArticleDetailView.as_view(), name='article-detail')
]
