
from django.db import models

class product_catagory(models.Model):
    id = models.AutoField(auto_created = True,primary_key = True,)
    catagory_name = models.CharField(max_length=255,default=None)    
    catagory_description= models.CharField(max_length=255,default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    last_modified_on = models.DateTimeField(auto_now=True)
    last_modified_by = models.CharField(max_length=255,default=None)
    #comment