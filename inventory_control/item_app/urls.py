from django.urls import path
from . import views

urlpatterns = [
    path('item_create/', views.item_create, name='item_create'),  
    path('item_view/', views.item_view, name='item_view'),   
    path('item_view_pagination/<int:page_number>', views.item_view_pagination, name='item_view_pagination'),  
     
]
