from django.db import models

# Create your models here.
from admin_account.models import *
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


class Project_Master(models.Model):
    pm_id = models.AutoField(auto_created=True, primary_key=True,)
    pm_project_name = models.TextField(max_length=5000, default=None)
    pm_project_client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_project_client')
    pm_district = models.CharField(max_length=300, default=None, null=True)
    pm_state = models.CharField(max_length=300, default=None, null=True)
    pm_city = models.CharField(max_length=300, default=None, null=True)
    pm_description = models.TextField(blank=True, null=True)
    pm_is_active = models.BooleanField(default=True)
    pm_all_product_available = models.BooleanField(default=False)
    pm_is_complete = models.BooleanField(default=False)
    pm_created_at = models.DateTimeField(auto_now_add=True)
    pm_last_modified_on = models.DateTimeField(auto_now=True)
    pm_last_modified_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='%(class)s_last_modified_by')


class Projects_Product(models.Model):
    pp_id = models.AutoField(auto_created=True, primary_key=True,)
    pp_project_master_id = models.ForeignKey(Project_Master, on_delete=models.CASCADE,)
    pp_product_id = models.ForeignKey(product_transaction, on_delete=models.CASCADE,)   # foreign
    pp_product_amount = models.PositiveIntegerField( default=None, null=True)
    pp_is_active = models.BooleanField(default=True)
    pp_created_at = models.DateTimeField(auto_now_add=True)
    pp_last_modified_on = models.DateTimeField(auto_now=True)
    pp_last_modified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_last_modified_by')


'''
class product_transaction(models.Model):
    pt_id = models.AutoField(auto_created=True, primary_key=True)
    pt_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_user')
    pt_product_name = models.CharField(max_length=255,default=None)
    pt_product_unit = models.CharField(max_length=255, default=None, null=True)
    pt_product_amount = models.PositiveIntegerField( default=None, null=True)
    pt_description = models.TextField(blank=True, null=True)
    pt_product_catagory = models.ForeignKey(product_catagory, on_delete=models.CASCADE,)
    pt_created_at = models.DateTimeField(auto_now_add=True)
    pt_is_active = models.BooleanField(default=True)
    pt_last_modified_on = models.DateTimeField(auto_now=True)
    pt_last_modified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_last_modified_by')
'''




class Projects_Product_Assigned(models.Model):
    ppa_id = models.AutoField(auto_created=True, primary_key=True,)
    ppa_project_master_id = models.ForeignKey(Project_Master, on_delete=models.CASCADE,)

    ppa_product_id = models.ForeignKey(product_master, on_delete=models.CASCADE,)   # ForeignKey

    ppa_product_qr_detais = models.ForeignKey(product_qr_master, on_delete=models.CASCADE,)

    ppa_last_scaned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_last_scaned_by')

    ppa_last_scaned_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_last_scaned_from')

    ppa_product_amount = models.CharField(max_length=255, default=None, null=True)
    ppa_is_active = models.BooleanField(default=True)
    ppa_is_faulty = models.BooleanField(default=False)
    ppa_created_at = models.DateTimeField(auto_now_add=True)
    ppa_last_modified_on = models.DateTimeField(auto_now=True)
    ppa_last_modified_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='%(class)s_last_modified_by')

class Projects_Product_Installed(models.Model):
    ppi_id = models.AutoField(auto_created=True, primary_key=True,)
    ppi_project_master_id = models.ForeignKey(Project_Master, on_delete=models.CASCADE,related_name='%(class)s_project_id')
    ppi_product_qr_detais = models.ForeignKey(product_qr_master, on_delete=models.CASCADE,)
    ppi_installed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_installed_by')
    ppi_amount =  models.PositiveIntegerField( default=None, null=True)
    ppi_install_image_path = models.CharField(max_length=255, default=None, null=True)
    ppi_install_image_name = models.CharField(max_length=255, default=None, null=True)
    ppi_description = models.TextField(blank=True, null=True)
    ppi_is_active = models.BooleanField(default=True)
    ppi_created_at = models.DateTimeField(auto_now_add=True)
    ppi_last_modified_on = models.DateTimeField(auto_now=True)
    ppi_last_modified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_last_modified_by')


class Projects_Users(models.Model):
    pu_id = models.AutoField(auto_created=True, primary_key=True,)
    pu_project_master_id = models.ForeignKey(
        Project_Master, on_delete=models.CASCADE,)

    pu_user = models.ForeignKey(User, on_delete=models.CASCADE,)
    pu_group_id = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='projects_users_user_type')

    pu_is_active = models.BooleanField(default=True)
    pu_created_at = models.DateTimeField(auto_now_add=True)
    pu_last_modified_on = models.DateTimeField(auto_now=True)
    pp_last_modified_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='%(class)s_last_modified_by')

class CustomerDetails(models.Model):
    #type direct or project
    cd_id = models.AutoField(auto_created=True, primary_key=True,)
    cd_company_name = models.CharField(max_length=300, default=None, null=True)
    cd_vat_gst_number = models.CharField(max_length=300, default=None, null=True)
    cd_order_number = models.CharField(max_length=300, default=None, null=True)
    cd_is_active = models.BooleanField(default=True)
    cd_created_at = models.DateTimeField(auto_now_add=True)
    cd_last_modified_on = models.DateTimeField(auto_now=True)
    cd_last_modified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_last_modified_by')


class DirectSell(models.Model):
    #type direct or project
    ds_id = models.AutoField(auto_created=True, primary_key=True,)
    ds_customer_details = models.ForeignKey(CustomerDetails, on_delete=models.CASCADE, related_name='%(class)s_customer_details')
    ds_type = models.CharField(max_length=300, default=None, null=True)
    ds_is_active = models.BooleanField(default=True)
    ds_is_complete = models.BooleanField(default=False)
    ds_created_at = models.DateTimeField(auto_now_add=True)
    ds_last_modified_on = models.DateTimeField(auto_now=True)
    ds_last_modified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_last_modified_by')

class CustomerProducts(models.Model):
    #type direct or project
    cp_id = models.AutoField(auto_created=True, primary_key=True,)
    cp_product_qr_detais = models.ForeignKey(product_qr_master, on_delete=models.CASCADE,related_name='%(class)s_products_qrdetails')
    cp_direct_sell = models.ForeignKey(DirectSell, on_delete=models.CASCADE, related_name='%(class)s_direct_sell')
    cp_amount = models.PositiveIntegerField( default=None, null=True)
    cp_is_active = models.BooleanField(default=True)
    cp_created_at = models.DateTimeField(auto_now_add=True)
    cp_last_modified_on = models.DateTimeField(auto_now=True)
    cp_last_modified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_last_modified_by')


class purchase_order (models.Model):
    acpo_id = models.AutoField(auto_created=True, primary_key=True,)
    acpo_project_master = models.ForeignKey(Project_Master, on_delete=models.CASCADE,default=1)
    acpo_order_submited = models.BooleanField(default=False)
    acpo_order_purchased = models.BooleanField(default=False)
    acpo_created_at = models.DateTimeField(auto_now_add=True)
    acpo_is_active = models.BooleanField(default=True)
    acpo_last_modified_on = models.DateTimeField(auto_now=True)
    acpo_last_modified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_last_modified_by')


class purchase_order_product (models.Model):
    acpop_id = models.AutoField(auto_created=True, primary_key=True,)
    acpop_purchase_order = models.ForeignKey(purchase_order, on_delete=models.CASCADE,)
    acpop_product_name = models.TextField(blank=True, null=True)
    acpop_product_catagory = models.CharField(max_length=255, default=None, null=True)
    acpop_product_unit = models.CharField(max_length=255, default=None, null=True)
    acpop_product_amount = models.CharField(max_length=255, default=None, null=True)
    acpop_product_purchased = models.BooleanField(default=False)
    acpop_created_at = models.DateTimeField(auto_now_add=True)
    acpop_is_active = models.BooleanField(default=True)
    acpop_last_modified_on = models.DateTimeField(auto_now=True)
    acpop_last_modified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_last_modified_by')
