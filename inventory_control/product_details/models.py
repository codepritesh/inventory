
from django.db import models

class item_master(models.Model):
    id = models.AutoField(auto_created = True,primary_key = True,)
    product_name = models.TextField(blank=True, null=True)
    product_catagory = models.IntegerField(blank=True, null=True)
    waranty_info = models.TextField(blank=True, null=True)
    serial_number = models.CharField(max_length=255,default=None)
    brand_details = models.TextField(blank=True, null=True)
    vender_details = models.TextField(blank=True, null=True)
    po_details = models.TextField(blank=True, null=True)
    product_types = models.CharField(max_length=255,default=None)
    product_unit = models.CharField(max_length=255,default=None)
    product_amount = models.CharField(max_length=255,default=None)    
    product_description = models.CharField(max_length=255,default=None)
    qrcode_details = models.CharField(max_length=255,default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    last_modified_on = models.DateTimeField(auto_now=True)
    last_modified_by = models.CharField(max_length=255,default=None)
    #comment