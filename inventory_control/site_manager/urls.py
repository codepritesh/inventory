from django.urls import path
from . import views

urlpatterns = [
    path('create_sitemanager/', views.create_sitemanager,
         name='create_sitemanager'),
    path('view_sitemanager/', views.view_sitemanager, name='view_sitemanager'),
    path('site_manager_pagination/<int:page_number>',
         views.site_manager_pagination, name='site_manager_pagination'),

    path('project_manager_view_projects/<str:user_id>',
         views.project_manager_view_projects, name='project_manager_view_projects'),
    path('project_manager_view_projects_pagination/<int:page_number>/<str:user_id>',
              views.project_manager_view_projects_pagination, name='project_manager_view_projects_pagination'),

    path('prm_scan_and_receive/<int:project_id>',
              views.prm_scan_and_receive, name='prm_scan_and_receive'),








]
