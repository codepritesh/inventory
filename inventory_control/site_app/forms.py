from django import forms

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from .models  import  site_master




class  site_form (forms.ModelForm):
  class Meta():
    model = site_master
    fields = (         
                       'site_name',
                       'address_line1',
                       'address_line2',
                       'address_line3',
                       'pincode',
                       'city',
                       'district',
                       'state',
                       'country',
                       'site_manager_name',
                       'site_manager_contact_number',
                       'last_modified_by')     # you can change the tuple element position to show it diffrently.
            
    labels = {  

                 #below label  is for changing labes as showin in forms
                
                'site_name': 'site_name',
                'address_line1':'address_line1',
                'address_line2': 'address_line2',
                'address_line3': 'address_line3',
                'pincode': 'pincode',
                'city': 'city',
                'district':'district',
                'state':'state',
                'country':'country', 
                'site_manager_name':'site_manager_name', 
                'site_manager_contact_number':'site_manager_contact_number',
                'last_modified_by':'last_modified_by'}
  
    # def __init__(self,*args, **kwargs):
    #     super(UserBotInstancesRunningForm,self).__init__(*args, **kwargs)
    #      #below code is for not showing a empty label
    #     self.fields['user_name'].empty_label = "select"
    #      #below code is for not showing a mandatory field
    #     self.fields['user_name'].required = False
