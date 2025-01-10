from django.urls import path
from . import views

urlpatterns = [
    path('vender_create/', views.vender_create, name='vender_create'),  
    path('vender_view/', views.vender_view, name='vender_view'),   
    path('vender_view_pagination/<int:page_number>', views.vender_view_pagination, name='vender_view_pagination'),  
     
]
