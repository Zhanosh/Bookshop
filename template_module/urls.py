from django.urls import path
from . import views
from Acount_module.views import LoginView, RegisterView, LogoutView, ForgotPass

urlpatterns = (
    path('', views.HomePageView.as_view(), name='index-page'),
    path('contact-us/', views.ContactUs.as_view(), name='contact-us-page'),
    path('about/', views.About.as_view(), name='about-page'),
    path('shop/', views.ShopList.as_view(), name='shop-page'),
    path('cat/<cat>', views.ShopList.as_view(), name='book-category'),
    path('shop-/<slug:slug>/', views.ShopDetail.as_view(), name='shop-detail-page'),
    path('login/', LoginView.as_view(), name='login-page'),
    path('register/', RegisterView.as_view(), name='register-page'),
    path('forgot-pass/', ForgotPass.as_view(), name='forgot-pass-page'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('search-page', views.searchView, name='search-page'),
)
