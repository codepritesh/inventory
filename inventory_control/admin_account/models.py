from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class product_catagory(models.Model):
    acpc_id = models.AutoField(auto_created=True, primary_key=True,)
    acpc_catagory_name = models.CharField(max_length=255, default=None)
    acpc_fra_or_single = models.CharField(max_length=255, default=None, null=True)
    acpc_catagory_description = models.CharField(max_length=255, default=None, null=True)
    acpc_is_active = models.BooleanField(default=True)
    acpc_created_at = models.DateTimeField(auto_now_add=True)
    acpc_last_modified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_last_modified_by')

class product_main_catagory(models.Model):
    pmc_id = models.AutoField(auto_created=True, primary_key=True,)
    pmc_main_catagory_name = models.CharField(max_length=255, default=None)
    pmc_main_catagory_description = models.CharField(max_length=255, default=None, null=True)
    pmc_created_at = models.DateTimeField(auto_now_add=True)
    pmc_is_active = models.BooleanField(default=True)

class product_main_catagory_maping(models.Model):
    pmcm_id = models.AutoField(auto_created=True, primary_key=True,)
    pmcm_main_catagory = models.ForeignKey(product_main_catagory, on_delete=models.CASCADE, related_name='%(class)s_main_catagory')
    pmcm_catagory = models.ForeignKey(product_catagory, on_delete=models.CASCADE, related_name='%(class)s_catagory')
    pmcm_is_active = models.BooleanField(default=True)

class product_transaction(models.Model):
    pt_id = models.AutoField(auto_created=True, primary_key=True)
    pt_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_user')
    pt_product_name = models.CharField(max_length=255,default=None)
    pt_product_unit = models.CharField(max_length=255, default=None, null=True)
    pt_product_amount = models.PositiveIntegerField( default=None, null=True)
    pt_description = models.TextField(blank=True, null=True)
    pt_product_catagory = models.ForeignKey(product_catagory, on_delete=models.CASCADE,)
    pt_product_main_catagory = models.ForeignKey(product_main_catagory, on_delete=models.CASCADE,)
    pt_created_at = models.DateTimeField(auto_now_add=True)
    pt_is_active = models.BooleanField(default=True)
    pt_last_modified_on = models.DateTimeField(auto_now=True)
    pt_last_modified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_last_modified_by')

class all_product_transaction(models.Model):

    apt_id = models.AutoField(auto_created=True, primary_key=True,)
    apt_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_user')
    apt_product_name = models.ForeignKey(product_transaction, on_delete=models.CASCADE,)
    apt_credit_amount = models.PositiveIntegerField( default=None, null=True)
    apt_debit_amount = models.PositiveIntegerField( default=None, null=True)
    apt_description = models.TextField(blank=True, null=True)
    apt_created_at = models.DateTimeField(auto_now_add=True)
    apt_is_active = models.BooleanField(default=True)
    apt_last_modified_on = models.DateTimeField(auto_now=True)
    apt_credited_or_debited_with = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_credited_or_debited_with')


class product_master(models.Model):
    acpm_id = models.AutoField(auto_created=True, primary_key=True,)
    acpm_product_name = models.TextField(blank=True, null=True)
    acpm_product_catagory = models.ForeignKey(product_catagory, on_delete=models.CASCADE,)
    acpm_product_main_catagory = models.ForeignKey(product_main_catagory, on_delete=models.CASCADE,)    
    acpm_waranty_info = models.TextField(blank=True, null=True)
    acpm_serial_number = models.CharField(max_length=255, default=None, null=True)
    acpm_brand_details = models.TextField(blank=True, null=True)
    acpm_vender_details = models.TextField(blank=True, null=True)
    acpm_po_details = models.TextField(blank=True, null=True)
    acpm_product_types = models.CharField(max_length=255, default=None, null=True)
    acpm_product_unit = models.CharField(max_length=255, default=None, null=True)
    acpm_product_amount = models.CharField(max_length=255, default=None, null=True)
    acpm_product_description = models.CharField(max_length=255, default=None, null=True)
    acpm_qrcode_details = models.CharField(max_length=255, default=None, null=True)
    acpm_uniq_id = models.CharField(max_length=255, default=None, null=True)
    acpm_created_at = models.DateTimeField(auto_now_add=True)
    acpm_is_active = models.BooleanField(default=True)
    acpm_last_modified_on = models.DateTimeField(auto_now=True)
    acpm_last_modified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_last_modified_by')


class barcode_master(models.Model):
    acbs_id = models.AutoField(auto_created=True, primary_key=True,)
    acbs_barcode_details = models.CharField(max_length=255, default=None, null=True)
    acbs_product_master_id = models.ForeignKey(product_master, on_delete=models.CASCADE,)


class product_qr_master(models.Model):
    acpqm_id = models.AutoField(auto_created=True, primary_key=True,)
    acpqm_product_master_id = models.ForeignKey(product_master, on_delete=models.CASCADE,)
    acpqm_product_location = models.CharField(max_length=255, default=None, null=True)
    acpqm_last_scaned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_last_scaned_by')
    acpqm_last_scaned_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_last_scaned_from')
    acpqm_product_movment_details = models.TextField(blank=True, null=True)
    acpqm_uniq_id = models.CharField(max_length=255, default=None, null=True,unique = True)
    acpqm_print_uniq_id = models.CharField(max_length=255, default=None, null=True)
    acpqm_qr_image_path = models.CharField(max_length=255, default=None, null=True)
    acpqm_qr_image_name = models.CharField(max_length=255, default=None, null=True)
    acpqm_created_at = models.DateTimeField(auto_now_add=True)
    acpqm_is_defective = models.BooleanField(default=False)
    acpqm_is_active = models.BooleanField(default=True)
    acpqm_last_modified_on = models.DateTimeField(auto_now=True)
    acpqm_last_modified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_last_modified_by')
