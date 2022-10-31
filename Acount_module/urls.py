from django.urls import path
from . import views
from order_module.views import add_product_to_order, RemoveOrderDetailCount

urlpatterns = [
    path('', views.UserProfileView.as_view(), name='user-panel'),
    path('change-pass/', views.ChangePassView.as_view(), name='change-pass-page'),
    path('cart-detail/', views.CartDetailView, name='cart-detail-page'),
    path('add-to-order/', add_product_to_order, name='add_product_to_order'),
    path('change-order-detail', RemoveOrderDetailCount, name='change_order_detail_count'),
    path('add-fav/<int:id>', views.AddtoFavBookView, name='add-to-fav'),
    path('fav-list/', views.FavListView, name='fav-list'),
]
