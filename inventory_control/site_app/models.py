
from django.db import models

class site_master(models.Model):
    id = models.AutoField(auto_created = True,primary_key = True,)
    site_name = models.CharField(max_length=255,default=None)
    address_line1 = models.CharField(max_length=255,default=None)
    address_line2= models.CharField(max_length=255,default=None)
    address_line3 = models.CharField(max_length=255,default=None)
    pincode = models.CharField(max_length=255,default=None)
    city = models.CharField(max_length=255,default=None)
    district = models.CharField(max_length=255,default=None)
    state = models.CharField(max_length=255,default=None)
    country = models.CharField(max_length=255,default=None)
    site_manager_name= models.CharField(max_length=255,default=None)
    site_manager_contact_number = models.CharField(max_length=255,default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    last_modified_on = models.DateTimeField(auto_now=True)
    last_modified_by = models.CharField(max_length=255,default=None)


    
