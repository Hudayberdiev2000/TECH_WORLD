from django.urls import path

from . import views


urlpatterns = [
    path('info', views.ShopDetails.as_view()),
    path('banners', views.BannerList.as_view()),
    path('rules', views.RuleList.as_view()),
]