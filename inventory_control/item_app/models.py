
from django.db import models

class item_master(models.Model):
    id = models.AutoField(auto_created = True,primary_key = True,)
    item_name = models.CharField(max_length=255,default=None)
    item_company_name = models.CharField(max_length=255,default=None)
    item_model_name= models.CharField(max_length=255,default=None)
    item_price = models.CharField(max_length=255,default=None)
    item_serial_number= models.CharField(max_length=255,default=None)
    item_description= models.CharField(max_length=255,default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    last_modified_on = models.DateTimeField(auto_now=True)
    last_modified_by = models.CharField(max_length=255,default=None)
    #comment