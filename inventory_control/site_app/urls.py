from django.urls import path
from . import views

urlpatterns = [
    path('site_create/', views.site_create, name='site_create'),  
    path('site_view/', views.site_view, name='site_view'),   
    path('site_view_pagination/<int:page_number>', views.site_view_pagination, name='site_view_pagination'),  
     
]
