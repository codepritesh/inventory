from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.admin_login, name='admin_login'),
    path('logout_view/', views.logout_view, name='logout_view'),
    path('add_new_product/', views.add_new_product, name='add_new_product'),
    
    path('add_new_product_fractional/', views.add_new_product_fractional,name='add_new_product_fractional'),
    path('chckproduct_presence/', views.chckproduct_presence,name='chckproduct_presence'),

    path('inventory_view/', views.inventory_view, name='inventory_view'),
    path('inventory_view_pagination/<int:page_number>',views.inventory_view_pagination, name='inventory_view_pagination'),

    path('product_view/', views.product_view, name='product_view'),
    path('product_view_pagination/<int:page_number>',views.product_view_pagination, name='product_view_pagination'),
    path('view_product_by_id/<int:product_id>',views.view_product_by_id, name='view_product_by_id'),

    path('purchase_order_view',views.purchase_order_view, name='purchase_order_view'),
    path('purchase_order_view_pagination/<int:page_number>',views.purchase_order_view_pagination, name='purchase_order_view_pagination'),
    path('create_purchase_order',views.create_purchase_order, name='create_purchase_order'),

    path('po_details_view/<int:po_id>',views.po_details_view, name='po_details_view'),
    path('remove_product_from_po/<int:product_id>',views.remove_product_from_po, name='remove_product_from_po'),

    path('add_product_to_po/<int:po_id>',views.add_product_to_po, name='add_product_to_po'),

    path('lattes_qrcode/<str:print_id>',views.lattes_qrcode, name='lattes_qrcode'),


    path('product_transection_view/<str:user_id>',views.product_transection_view, name='product_transection_view'),

    path('product_transection_pagination_view/<int:page_number>/<str:user_id>',views.product_transection_pagination_view, name='product_transection_pagination_view'),

    path('product_trans_by_id/<int:pt_id>/<str:user_id>',views.product_trans_by_id, name='product_trans_by_id'),
    path('product_trans_by_id_pagination/<int:pt_id>/<int:page_number>/<str:user_id>',views.product_trans_by_id_pagination, name='product_trans_by_id_pagination'),

    path('all_product_transaction_view/<str:user_id>',views.all_product_transaction_view, name='all_product_transaction_view'),
    path('all_product_transaction_pagination_view/<int:page_number>/<str:user_id>',views.all_product_transaction_pagination_view, name='all_product_transaction_pagination_view'),
    path('fra_product_from_invent',views.fra_product_from_invent, name='fra_product_from_invent'),
    path('add_new_product_if_not_available',views.add_new_product_if_not_available, name='add_new_product_if_not_available'),

    path('inventory_report',views.inventory_report, name='inventory_report'),

    path('product_trans_by_product_id/<int:product_id>',views.product_trans_by_product_id, name='product_trans_by_product_id'),



    path('main_catagory_name_view/', views.main_catagory_name_view, name='main_catagory_name_view'),
    path('main_catagory_name_by_id/<int:main_cat_id>', views.main_catagory_name_by_id, name='main_catagory_name_by_id'),    
    path('main_catagory_name_view_pagination/<int:page_number>',views.main_catagory_name_view_pagination, name='main_catagory_name_view_pagination'),


    path('sub_catagory_name_view/', views.sub_catagory_name_view, name='sub_catagory_name_view'),
    path('sub_catagory_name_by_id/<int:sub_cat_id>', views.sub_catagory_name_by_id, name='sub_catagory_name_by_id'),   
    path('sub_catagory_name_view_pagination/<int:page_number>',views.sub_catagory_name_view_pagination, name='sub_catagory_name_view_pagination'),
    

    path('product_name_view/', views.product_name_view, name='product_name_view'),
    path('product_name_by_id/<int:prod_name_id>', views.product_name_by_id, name='product_name_by_id'),  
    path('product_name_view_pagination/<int:page_number>',views.product_name_view_pagination, name='product_name_view_pagination'),
   

    


]
