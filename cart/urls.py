from django.urls import path
from .views import GetItemTotalView, GetTotalView, GetItemsView, AddItemView,UpdateItemView, RemoveItemView, EmptyCartView
urlpatterns = [
    path('cart-items', GetItemsView.as_view()),
    path('add-item', AddItemView.as_view()),
    path('total_cost', GetTotalView.as_view()),
    path('number_of_items', GetItemTotalView.as_view()),
    path('update-item', UpdateItemView.as_view()),
    path('remove-item', RemoveItemView.as_view()),
    path('empty-cart', EmptyCartView.as_view()),
    # path('synch', SynchCartView.as_view()),
]