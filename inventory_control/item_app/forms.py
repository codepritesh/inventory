from django import forms

from django.contrib.auth import get_user_model
#from django.contrib.auth.models import User
from .models  import  item_master


class  item_form (forms.ModelForm):
  class Meta():
    model = item_master
    fields = (         
                       'item_name',
                       'item_company_name',
                       'item_model_name',
                       'item_price',
                       'item_serial_number',
                       'item_description',
                       'last_modified_by')     # you can change the tuple element position to show it diffrently.
            
    labels = {  

                 #below label  is for changing labes as showin in forms
                
                'item_name': 'item_name',
                'item_company_name':'item_company_name',
                'item_model_name': 'item_model_name',
                'item_price': 'item_price',
                'item_serial_number': 'item_serial_number',
                'item_description': 'item_description',
                'last_modified_by':'last_modified_by'}
  
    # def __init__(self,*args, **kwargs):
    #     super(UserBotInstancesRunningForm,self).__init__(*args, **kwargs)
    #      #below code is for not showing a empty label
    #     self.fields['user_name'].empty_label = "select"
    #      #below code is for not showing a mandatory field
    #     self.fields['user_name'].required = False
