from django.urls import path
from . import views

urlpatterns = [
    path('create_site_user/', views.create_site_user, name='create_site_user'),
    path('view_site_user/', views.view_site_user, name='view_site_user'),
    path('site_user_pagination/<int:page_number>', views.site_user_pagination, name='site_user_pagination'),
    path('project_user_view_projects/',views.project_user_view_projects, name='project_user_view_projects'),
    path('project_user_view_projects_pagination/<int:page_number>',views.project_user_view_projects_pagination, name='project_user_view_projects_pagination'),
    path('pru_scan_and_receive/<int:project_id>',views.pru_scan_and_receive, name='pru_scan_and_receive'),
    path('create_direct_sell_user/', views.create_direct_sell_user, name='create_direct_sell_user'),
    path('view_direct_sell_user/', views.view_direct_sell_user, name='view_direct_sell_user'),
    path('view_direct_sell_user_pagination/<int:page_number>', views.view_direct_sell_user_pagination, name='view_direct_sell_user_pagination'),




]
