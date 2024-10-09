from django.urls import path

from . import views


urlpatterns = [
    path('', views.OrderList.as_view()),
    path('preview', views.OderpreviewView.as_view()),
]