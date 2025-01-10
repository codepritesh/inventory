from django.urls import path
from . import views

urlpatterns = [
    path('started_project/<int:po_id>', views.started_project, name='started_project'),
    path('project_manager_dashboard/', views.project_manager_dashboard, name='project_manager_dashboard'),
    path('project_user_dashboard/', views.project_user_dashboard, name='project_user_dashboard'),
    path('inventory_dashboard/', views.inventory_dashboard, name='inventory_dashboard'),
    path('project_dashboard/', views.project_dashboard, name='project_dashboard'),
    path('product_management_dash/', views.product_management_dash, name='product_management_dash'),
]
