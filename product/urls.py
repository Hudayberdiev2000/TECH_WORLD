from django.urls import path

from . import views

urlpatterns = [
    path('categories', views.CategoryList.as_view()),
    path('category_products', views.CategoryProducts.as_view()),
    path('', views.ProductList.as_view()),
    path('details', views.ProductDetails.as_view()),
    path('search', views.ProductSearchView.as_view()),
    path('favourites', views.UserFavouritesAPIView.as_view()),
]