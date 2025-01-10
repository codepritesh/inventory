from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('', views.admin_login, name='admin_login'),
    path('create_new_project/',views.create_new_project, name='create_new_project'),
    path('project_view/', views.project_view, name='project_view'),
    path('project_view_pagination/<int:page_number>',views.project_view_pagination, name='project_view_pagination'),
    path('details_of_project/<int:project_id>',views.details_of_project, name='details_of_project'),
    path('add_user_to_project/<int:project_id>',views.add_user_to_project, name='add_user_to_project'),
    path('add_product_to_project/<int:project_id>',views.add_product_to_project, name='add_product_to_project'),
    path('remove_user_from_project/<int:user_id>',views.remove_user_from_project, name='remove_user_from_project'),
    path('remove_product_from_project/<int:pp_id>',views.remove_product_from_project, name='remove_product_from_project'),
    path('start_project/<int:project_id>',views.start_project, name='start_project'),
    path('product_assigned_to/<int:project_id>',views.product_assigned_to, name='product_assigned_to'),
    path('install_product_toproject/<int:project_id>',views.install_product_toproject, name='install_product_toproject'),
    path('install_one_product_toproject/<int:project_id>',views.install_one_product_toproject, name='install_one_product_toproject'),

    path('receive_faulty_product/',views.receive_faulty_product, name='receive_faulty_product'),
    path('view_faulty_product/',views.view_faulty_product, name='view_faulty_product'),
    path('view_faulty_product_pagination/<int:page_number>',views.view_faulty_product_pagination, name='view_faulty_product_pagination'),

    path('receive_unused_product/',views.receive_unused_product, name='receive_unused_product'),
    path('details_of_project_history/<int:project_id>',views.details_of_project_history, name='details_of_project_history'),
    path('product_sold_directly/',views.product_sold_directly, name='product_sold_directly'),
    path('admin_watching_user/',views.admin_watching_user, name='admin_watching_user'),
    path('admin_watching_project_manager/',views.admin_watching_project_manager, name='admin_watching_project_manager'),
    path('add_direct_customer/',views.add_direct_customer, name='add_direct_customer'),
    path('view_sell/',views.view_sell, name='view_sell'),
    path('scan_and_check/',views.scan_and_check, name='scan_and_check'),
    path('view_sell_pagination/<int:page_number>',views.view_sell_pagination, name='view_sell_pagination'),
    path('details_of_sell/<int:sell_id>',views.details_of_sell, name='details_of_sell'),
    path('scan_and_add_product_to_sell/<int:ds_id>',views.scan_and_add_product_to_sell, name='scan_and_add_product_to_sell'),
    path('remove_product_from_sell/<int:ds_id>/<int:cp_id>',views.remove_product_from_sell, name='remove_product_from_sell'),
    path('submit_direct_sell/<int:sell_id>',views.submit_direct_sell, name='submit_direct_sell'),
    path('validate_po/<int:project_id>',views.validate_po, name='validate_po'),
    path('project_report/<int:project_id>',views.project_report, name='project_report'),

]
