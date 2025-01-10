from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from .models import *
from django.contrib import messages
from admin_account.models import *
from django.contrib.auth.models import User,Group
from django.utils import timezone
from admin_account.utils import product_transection_fun,save_filewc,allowed_file_image
from django.db.models import Q
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
import os

@login_required(login_url='/login/')
def admin_dashboard(request):
    if request.method == "GET":

        current_user = request.user

        groupid = current_user.groups.values_list('id', flat=True).first()
        groupname = current_user.groups.values_list('name', flat=True).first()
        # 'groupid':groupid,
        # 'groupname':groupname
        context = {"data": "data",
                    'groupid':groupid,
                    'groupname':groupname
                      }
        return render(request, 'index.html', context)
    else:
        context = {"data": "data"}
        return render(request, 'index.html', context)

@login_required(login_url='/login/')
def admin_login(request):
    if request.method == "GET":
        context = {"data": "data"}
        return render(request, 'login.html', context)
    else:
        context = {"data": "data"}
        return render(request, 'login.html', context)

@login_required(login_url='/login/')
def create_new_project(request):
    if request.method == "GET":
        context = {"data": "data"}
        return render(request, 'admin_dashboard/create_new_project.html', context)
    else:
        now = timezone.localtime(timezone.now())
        current_user = request.user
        user_id = current_user.id

        project_name = request.POST.get("project_name")
        project_district = request.POST.get("project_district")
        project_city = request.POST.get("project_city")
        project_state = request.POST.get("project_state")
        if project_state == '0':
            messages.error(request, "please select a valid state")
            context = {"data": "data"}
            return render(request, 'admin_dashboard/create_new_project.html', context)

        project_name_exist = Project_Master.objects.filter(
            pm_project_name=project_name).exists()
        if project_name_exist:
            messages.error(request, "project name:" + str(project_name) +
                           "              already exist chose a diffrent name")
            context = {"data": "data"}
            return render(request, 'admin_dashboard/create_new_project.html', context)

        else:


            username_projectuser = "project_" + project_name
            email_project_user = username_projectuser+"@inventory.com"

            username_exists = User.objects.filter(username = username_projectuser).exists()
            email_exists = User.objects.filter(email = email_project_user).exists()
            if (username_exists or email_exists) :

                messages.error(request, "project name:" + str(project_name) +
                               "              already exist chose a diffrent name")
                context = {"data": "data"}
                return render(request, 'admin_dashboard/create_new_project.html', context)
            else:
                project_user = User.objects.create_user(
                                            first_name=project_name,
                                            last_name=project_district,
                                            username = username_projectuser,
                                            password = "Qwerty@1234",
                                            email = email_project_user,
                                            is_active = True
                                        )
                project_user.save()

                profile_user = User.objects.get(username = username_projectuser)
                my_group = Group.objects.get(name='project_client')
                profile_user.groups.add(my_group)


                b = Project_Master(
                    pm_project_name=project_name,
                    pm_project_client = profile_user,
                    pm_district=project_district,
                    pm_state=project_state,
                    pm_city=project_city,
                    pm_description = "project created by("+str(current_user.username) +")--"+str(now)+".\n",
                    pm_last_modified_by=current_user)
                b.save()

                messages.success(request, "project name:" + str(project_name) +" created successfully please add some product")

                context = {"data": "data"}
                return redirect('project_view')

@login_required(login_url='/login/')
def project_view(request):
    if request.method == 'GET':
        # query_results = site_master.objects.all()
        curent_page = 1
        pagedata_starting = 0
        pagedata_ending = pagedata_starting + 20

        prev_pagenumber = 1
        next_page_number = 2
        totaldata = Project_Master.objects.all().order_by('pm_created_at').count()

        query_results = Project_Master.objects.all().order_by('-pm_created_at')[
            :pagedata_ending]
        showingdata = query_results.count()

        context = {"query_results": query_results,
                   'totaldata': totaldata,
                   'curent_page': curent_page,
                   'pagedata_starting': pagedata_starting,
                   'prev_pagenumber': prev_pagenumber,
                   'next_page_number': next_page_number,
                   'showingdata': showingdata

                   }
        return render(request, 'admin_dashboard/project_view.html', context)

@login_required(login_url='/login/')
def project_view_pagination(request, page_number):
    if request.method == 'GET':

        # query_results = site_master.objects.all()
        if page_number != 1:
            curent_page = int(page_number)
            page_number = page_number-1
            prev_pagenumber = curent_page - 1
            pagedata_starting = page_number * 20
            pagedata_ending = pagedata_starting + 20
        else:
            curent_page = 1
            page_number = 1
            prev_pagenumber = 1
            pagedata_starting = 0
            pagedata_ending = pagedata_starting + 20

        next_page_number = curent_page + 1

        totaldata = Project_Master.objects.all().order_by('pm_created_at').count()

        query_results = Project_Master.objects.all().order_by(
            'pm_created_at')[pagedata_starting:pagedata_ending]
        showingdata = query_results.count()

        context = {"query_results": query_results,
                   'totaldata': totaldata,
                   'curent_page': curent_page,
                   'pagedata_starting': pagedata_starting,
                   'prev_pagenumber': prev_pagenumber,
                   'next_page_number': next_page_number,
                   'showingdata': showingdata

                   }
        return render(request, 'admin_dashboard/project_view.html', context)

@login_required(login_url='/login/')
def details_of_project(request, project_id):
    if request.method == 'GET':
        # if not request.user.is_authenticated:
        #     return redirect('main_login')

        project_exist = Project_Master.objects.filter(
            pm_id=project_id).exists()
        if project_exist:
            project_details_by_id = Project_Master.objects.filter(
                pm_id=project_id).filter(pm_is_active=True)

            Projects_Product_by_id = Projects_Product.objects.filter(
                pp_project_master_id=project_details_by_id[0], pp_is_active=True).exists()
            Projects_Product_data = {}
            if Projects_Product_by_id:
                Projects_Product_data = Projects_Product.objects.filter(
                    pp_project_master_id=project_details_by_id[0], pp_is_active=True)

            Projects_Users_by_id = Projects_Users.objects.filter(
                pu_project_master_id=project_details_by_id[0], pu_is_active=True).exists()

            Projects_Users_data = {}
            if Projects_Users_by_id:
                Projects_Users_data = Projects_Users.objects.filter(
                    pu_project_master_id=project_details_by_id[0], pu_is_active=True)

            project_details_obj = Project_Master.objects.get(pm_id=project_id)
            projects_po_exists = purchase_order.objects.filter(acpo_project_master=project_details_obj).exists()
            projects_po={}
            if projects_po_exists:
                projects_po = purchase_order.objects.filter(acpo_project_master=project_details_obj)

            user = request.user
            groupid = user.groups.values_list('id', flat=True).first()
            groupname = user.groups.values_list('name', flat=True).first()

            context = {"project_id": project_details_by_id,
                       'Projects_Product_data': Projects_Product_data,
                       'Projects_Users_data': Projects_Users_data,
                       'projects_po':projects_po,
                       'groupid':groupid,
                       'groupname':groupname}
            #print(context)
            return render(request, 'admin_dashboard/details_of_project_view.html', context)
        else:
            messages.error(
                request, "Project not found for this id.")

            return render(request, '404.html')

@login_required(login_url='/login/')
def project_report(request, project_id):
    if request.method == 'GET':
        # if not request.user.is_authenticated:
        #     return redirect('main_login')

        project_exist = Project_Master.objects.filter(
            pm_id=project_id,pm_is_active=True).exists()
        if project_exist:
            project_details_by_id = Project_Master.objects.get(
                pm_id=project_id)

            Projects_Product_by_id = Projects_Product.objects.filter(
                pp_project_master_id=project_details_by_id, pp_is_active=True).exists()
            Projects_Product_data = {}
            if Projects_Product_by_id:
                Projects_Product_data = Projects_Product.objects.filter(
                    pp_project_master_id=project_details_by_id, pp_is_active=True)

            Projects_Users_by_id = Projects_Users.objects.filter(
                pu_project_master_id=project_details_by_id, pu_is_active=True).exists()

            Projects_Users_data = {}
            if Projects_Users_by_id:
                Projects_Users_data = Projects_Users.objects.filter(
                    pu_project_master_id=project_details_by_id, pu_is_active=True)

            assigned_product = {}
            project_product_assignment = Projects_Product_Assigned.objects.filter(ppa_project_master_id=project_details_by_id).exists()
            if project_product_assignment:
                assigned_product = Projects_Product_Assigned.objects.filter(ppa_project_master_id=project_details_by_id)


            Projects_Product_Installed_product={}
            Projects_Product_Installed_exists = Projects_Product_Installed.objects.filter(ppi_project_master_id=project_details_by_id).exists()
            if Projects_Product_Installed_exists:
                Projects_Product_Installed_product = Projects_Product_Installed.objects.filter(ppi_project_master_id=project_details_by_id)

            projects_po_exists = purchase_order.objects.filter(acpo_project_master=project_details_by_id).exists()

            projects_po_dict={}
            if projects_po_exists:
                projects_po = purchase_order.objects.filter(acpo_project_master=project_details_by_id)
                for each_po in projects_po:

                    po_id_key = each_po.acpo_id
                    #print('checkpo exist----',po_id_key)
                    po_product_exists = purchase_order_product.objects.filter(acpop_purchase_order=each_po).exists()
                    if po_product_exists:
                        po_products = purchase_order_product.objects.filter(acpop_purchase_order=each_po)
                        po_products_dict={}
                        for  each_product in po_products:
                            product_key = each_product.acpop_id

                            po_products_dict[product_key]=each_product
                            projects_po_dict[po_id_key]=po_products_dict
                        del po_products_dict

                    else:
                        print('product_key not ')
            else:
                projects_po_dict={}

            user = request.user
            groupid = user.groups.values_list('id', flat=True).first()
            groupname = user.groups.values_list('name', flat=True).first()

            context = {"project_id": Project_Master.objects.filter(pm_id=project_id,pm_is_active=True),
                       'Projects_Product_data': Projects_Product_data,
                       'Projects_Users_data': Projects_Users_data,
                       'assigned_product': assigned_product,
                       'Projects_Product_Installed_product': Projects_Product_Installed_product,
                       'projects_po_dict':projects_po_dict,
                       'projects_po':projects_po,
                       'groupid':groupid,
                       'groupname':groupname}
            return render(request, 'admin_dashboard/project_report_view.html', context)
        else:
            messages.error(
                request, "Project not found for this id.")

            return render(request, '404.html')


@login_required(login_url='/login/')
def add_product_to_project(request, project_id):
    if request.method == 'GET':
        current_user = request.user

        project_exist = Project_Master.objects.filter(
            pm_id=project_id).filter(pm_is_active=True).exists()
        if project_exist:
            project_details_by_id = Project_Master.objects.filter(pm_id=project_id,pm_is_active=True)

            all_product = product_transaction.objects.filter(pt_is_active=True,pt_user=current_user)

            Projects_Product_by_id = Projects_Product.objects.filter(pp_project_master_id=project_details_by_id[0], pp_is_active=True).exists()
            Projects_Product_data = {}
            if Projects_Product_by_id:
                Projects_Product_data = Projects_Product.objects.filter(pp_project_master_id=project_details_by_id[0], pp_is_active=True)

            context = {"project_id_details": project_details_by_id,
                       "products_of_project": Projects_Product_data,
                       "all_product": all_product}

            return render(request, 'admin_dashboard/add_product_to_project_view.html', context)
        else:
            messages.error(
                request, "Project not found for this id.")
            return redirect('project_view')
    else:
        now = timezone.localtime(timezone.now())
        current_user = request.user

        product_id = request.POST.get("product_id")
        if product_id == '0':
            messages.error(
                request, "please select a valid product")
            return redirect('add_product_to_project', project_id=project_id)

        product_amount = request.POST.get("product_amount")

        project_details_by_id = Project_Master.objects.get(
            pm_id=project_id, pm_is_active=True)

        selected_product = product_transaction.objects.get(
            pt_id=product_id, pt_is_active=True)


        # where admin can add product


        # check productid abd projectid if same fetch amount and add then update

        project_product_exist = Projects_Product.objects.filter(
            pp_project_master_id=project_details_by_id, pp_product_id=selected_product).exists()

        if project_product_exist:

            project_product = Projects_Product.objects.get(
                pp_project_master_id=project_details_by_id, pp_product_id=selected_product)

            if project_product.pp_is_active == False:
                project_product.pp_is_active = True
                project_product.pp_product_amount = int(product_amount)
                project_product.save()

                messages.success(request, "product added successfully")

                project_details_by_id.pm_description = str(project_details_by_id.pm_description)+" added product ("+str(selected_product.pt_product_name)+") catagory  ("+str(selected_product.pt_product_catagory.acpc_catagory_name)+") amount-("+str(product_amount)+")-- "+str(now)+".\n"
                project_details_by_id.save()

                return redirect('add_product_to_project', project_id=project_id)
            else:
                totalamount = int(project_product.pp_product_amount) + int(product_amount)
                project_product.pp_product_amount = totalamount
                project_product.save()

                messages.success(request, "product sumed and added successfully")

                project_details_by_id.pm_description = str(project_details_by_id.pm_description)+" added product ("+str(selected_product.pt_product_name)+") catagory  ("+str(selected_product.pt_product_catagory.acpc_catagory_name)+") added amount-("+str(product_amount)+") total amount-("+str(totalamount)+")-- "+str(now)+".\n"
                project_details_by_id.save()

                return redirect('add_product_to_project', project_id=project_id)

        else:

            c = Projects_Product(pp_project_master_id=project_details_by_id,
                                 pp_product_id=selected_product,
                                 pp_product_amount=int(product_amount),
                                 pp_last_modified_by=current_user,
                                 )
            c.save()
            messages.success(request, "new product added successfully")

            project_details_by_id.pm_description = str(project_details_by_id.pm_description)+"added product ("+str(selected_product.pt_product_name)+") catagory  ("+str(selected_product.pt_product_catagory.acpc_catagory_name)+") amount- ("+str(product_amount)+") -- "+str(now)+".\n"
            project_details_by_id.save()
            return redirect('add_product_to_project', project_id=project_id)



@login_required(login_url='/login/')
def validate_po(request,project_id):
    if request.method == "GET":
        current_user = request.user

        project_exists = Project_Master.objects.filter(pm_id=project_id, pm_is_active=True).exists()
        if project_exists:
            project_details_by_id = Project_Master.objects.get(pm_id=project_id, pm_is_active=True)
        else:
            messages.success(request,"no project available with this id")
            return redirect('add_product_to_project',project_id=project_id)


        project_product_exist = Projects_Product.objects.filter(pp_project_master_id=project_details_by_id,pp_is_active=True).exists()
        if project_product_exist:
            project_product = Projects_Product.objects.filter(pp_project_master_id=project_details_by_id,pp_is_active=True)

            pass
        else:
            messages.error(request,"No product added to validate.")
            return redirect('add_product_to_project',project_id=project_id)





        is_po_created = False
        lattest_po = False
        for i, c in enumerate(project_product):
            #print (i, c, type(c))
            product_available_amount = c.pp_product_id.pt_product_amount
            product_name = c.pp_product_id.pt_product_name
            product_cat_name = c.pp_product_id.pt_product_catagory.acpc_catagory_name
            product_unit = c.pp_product_id.pt_product_unit
            amount_selected = c.pp_product_amount
            if amount_selected > product_available_amount:
                #print("if")
                if is_po_created == False:
                    #create a new po
                    d = purchase_order(acpo_last_modified_by=current_user,acpo_project_master=project_details_by_id)
                    d.save()
                    is_po_created=True

                if lattest_po == False:
                    lattest_po_data = purchase_order.objects.latest('acpo_id')
                    #print(lattest_po_data,'lattest_po_data')
                    lattest_po=True


                amount_selected_int=int(amount_selected)
                amount_available_int=int(product_available_amount)

                po_amount= amount_selected_int - amount_available_int
                str_po_amount = str(po_amount)

                #print(amount_selected_int,'amount_selected_int')
                #print(amount_available_int,'amount_available_int')
                #print(str_po_amount,'str_po_amount')


                c = purchase_order_product(acpop_purchase_order=lattest_po_data,
                                           acpop_product_name=product_name,
                                           acpop_product_catagory=product_cat_name,
                                           acpop_product_unit=product_unit,
                                           acpop_product_amount=str_po_amount,
                                           acpop_last_modified_by=current_user,
                                           )
                c.save()





        messages.success(request,"success")
        return redirect('details_of_project',project_id=project_id)


@login_required(login_url='/login/')
def add_user_to_project(request, project_id):
    if request.method == 'GET':
        project_exist = Project_Master.objects.filter(
            pm_id=project_id).filter(pm_is_active=True).exists()
        if project_exist:
            project_details_by_id = Project_Master.objects.filter(
                pm_id=project_id).filter(pm_is_active=True)

            all_user = User.objects.filter(is_active=True).filter(Q(groups__name='project_user') | Q(groups__name='project_manager'))

            Projects_Users_by_id = Projects_Users.objects.filter(
                pu_project_master_id=project_details_by_id[0], pu_is_active=True).exists()

            Projects_Users_data = {}
            if Projects_Users_by_id:
                Projects_Users_data = Projects_Users.objects.filter(
                    pu_project_master_id=project_details_by_id[0], pu_is_active=True)

            context = {"project_id_details": project_details_by_id,
                       "users_of_project": Projects_Users_data,
                       "all_user": all_user}

            return render(request, 'admin_dashboard/add_user_to_project_view.html', context)

        else:
            messages.error(
                request, "Project not found for this id.")
            return redirect('project_view')
    else:
        now = timezone.localtime(timezone.now())

        current_user = request.user
        user_id = request.POST.get("user_id")
        if user_id == "0":
            messages.error(
                request, "Please choose a valid user")
            return redirect('add_user_to_project', project_id=project_id)

        project_details_by_id = Project_Master.objects.get(
            pm_id=project_id, pm_is_active=True)

        selected_user = User.objects.get(
            pk=user_id, is_active=True)

        groupid = selected_user.groups.values_list('id', flat=True).first()
        #2 project site_manager
        #3 project user

        project_user_exist = Projects_Users.objects.filter(
            pu_project_master_id=project_details_by_id, pu_user=selected_user).exists()



        #check if any project manager present
        any_project_manager_exist = Projects_Users.objects.filter(
                pu_project_master_id=project_details_by_id, pu_group_id__name='project_manager',pu_is_active=True).exists()
        if any_project_manager_exist and (groupid == 2):

            messages.error(
                        request, "already added a Project Manager, to add new one remove present project manager.")
            return redirect('add_user_to_project', project_id=project_id)


        #check if manager exist , if exist
        project_manager_exist = Projects_Users.objects.filter(
                pu_project_master_id=project_details_by_id, pu_user=selected_user,pu_group_id__name='project_manager').exists()

        #if exist
        #project_manager_exist

        if project_manager_exist and (groupid == 2):
            project_manager_exist = Projects_Users.objects.get(
                    pu_project_master_id=project_details_by_id, pu_user=selected_user, pu_group_id__name='project_manager')
            if project_manager_exist.pu_is_active == True:
                messages.error(
                    request, "Already added a project manager, to add new one remove present project manager.")
                return redirect('add_user_to_project', project_id=project_id)
            else:
                project_manager_exist.pu_is_active= True
                project_manager_exist.save()
                messages.success(
                    request, "project mnager added to project successfully.")
                project_details_by_id.pm_description = str(project_details_by_id.pm_description)+"project manager ("+str(selected_user.username)+") added by ("+str(current_user.username)+") --- "+str(now)+".\n"
                project_details_by_id.save()
                return redirect('add_user_to_project', project_id=project_id)

        if (not project_manager_exist) and (groupid == 2):

            group_name=Group.objects.get(pk=groupid)


            c = Projects_Users(pu_project_master_id=project_details_by_id,
                               pu_user=selected_user,
                               pp_last_modified_by=current_user,
                               pu_group_id = group_name,
                               )
            c.save()

            project_details_by_id.pm_description = str(project_details_by_id.pm_description)+" project manager ( "+str(selected_user.username)+") added by("+str(current_user.username)+")---"+str(now)+".\n"
            project_details_by_id.save()

            messages.success(request, "project manager added  to project successfully.")
            return redirect('add_user_to_project', project_id=project_id)



        if project_user_exist and (groupid == 3):
            project_user = Projects_Users.objects.get(
                pu_project_master_id=project_details_by_id, pu_user=selected_user)
            if project_user.pu_is_active == False:
                project_user.pu_is_active = True
                project_user.save()

                project_details_by_id.pm_description = str(project_details_by_id.pm_description)+" user ( "+str(selected_user.username)+") added by ("+str(current_user.username)+") ---"+str(now)+".\n"
                project_details_by_id.save()

                messages.success(request, "User added to project successfully.")
                return redirect('add_user_to_project', project_id=project_id)
            else:

                messages.error(request, "User alredy added to project.")
                return redirect('add_user_to_project', project_id=project_id)

        else:
            group_name=Group.objects.get(pk=groupid)


            c = Projects_Users(pu_project_master_id=project_details_by_id,
                               pu_user=selected_user,
                               pp_last_modified_by=current_user,
                               pu_group_id = group_name
                               )
            c.save()

            project_details_by_id.pm_description = str(project_details_by_id.pm_description)+" user ( "+str(selected_user.username)+") added by ("+str(current_user.username)+") --- "+str(now)+".\n"
            project_details_by_id.save()

            messages.success(request, "user added to project successfully.")
            return redirect('add_user_to_project', project_id=project_id)

@login_required(login_url='/login/')
def remove_user_from_project(request, user_id):
    if request.method == 'POST':
        now = timezone.localtime(timezone.now())

        project_id = request.POST.get("project_id")

        current_user = request.user

        project_details_by_id = Project_Master.objects.get(
            pk=project_id)

        project_user_exist = Projects_Users.objects.filter(
            pu_project_master_id=project_details_by_id, pk=user_id).exists()

        if project_user_exist:
            project_user = Projects_Users.objects.get(
                pu_project_master_id=project_details_by_id, pk=user_id)

            project_user.pu_is_active = False
            project_user.save()

            messages.success(
                request, "successfully removed user from this project.")
            project_details_by_id.pm_description = str(project_details_by_id.pm_description)+" user ( "+str(project_user.pu_user.username)+") removed by ("+str(current_user.username)+") --- "+str(now)+".\n"
            project_details_by_id.save()
            return redirect('add_user_to_project', project_id=project_id)

        else:

            messages.error(request, "For this id, user is not present.")
            return redirect('add_user_to_project', project_id=project_id)

@login_required(login_url='/login/')
def remove_product_from_project(request, pp_id):
    if request.method == 'POST':
        now = timezone.localtime(timezone.now())

        project_id = request.POST.get("project_id")

        current_user = request.user

        project_details_by_id = Project_Master.objects.get(
            pm_id=project_id, pm_is_active=True)

        project_product_exist = Projects_Product.objects.filter(
            pp_project_master_id=project_details_by_id, pp_id=pp_id).exists()
        if project_product_exist:
            project_product = Projects_Product.objects.get(
                pp_project_master_id=project_details_by_id, pp_id=pp_id)

            project_product.pp_is_active = False
            project_product.save()

            messages.success(request, "successfully removed product from this project.")

            project_product.pp_product_id.pt_product_name
            project_product.pp_product_id.pt_product_catagory.acpc_catagory_name
            project_product.pp_product_amount

            project_details_by_id.pm_description = str(project_details_by_id.pm_description)+" removed product ("+str(project_product.pp_product_id.pt_product_name)+") catagory  ("+str(project_product.pp_product_id.pt_product_catagory.acpc_catagory_name)+") amount- ("+str(project_product.pp_product_amount)+") -- "+str(now)+".\n"
            project_details_by_id.save()


            return redirect('add_product_to_project', project_id=project_id)

        else:

            messages.error(request, "For this id, product is not present.")
            return redirect('add_product_to_project', project_id=project_id)


@login_required(login_url='/login/')
def receive_unused_product(request):
    if request.method == 'GET':
        data = product_catagory.objects.filter(acpc_is_active=True)

        context = {"product_cat": data}
        return render(request, 'admin_dashboard/receive_unused_product.html',context)
    else:
        current_user = request.user

        qr_code_number = request.POST.get("barcode_details")    #e7c18d33e17c11ebb6a157968fde45e <class 'str'>

        qrrcode_exists = product_qr_master.objects.filter(
            acpqm_uniq_id=qr_code_number).exists()
        if qrrcode_exists:  # when barcode data exist
            product_qr_master_row = product_qr_master.objects.get(
                acpqm_uniq_id=qr_code_number)
            last_scaned_by_asigned = product_qr_master_row.acpqm_last_scaned_by

            if (product_qr_master_row.acpqm_last_scaned_by == current_user and product_qr_master_row.acpqm_is_defective == True):
                messages.error(request, "Product already received")
                return redirect('receive_unused_product')


            product_master_row = product_qr_master_row.acpqm_product_master_id
            lastscaned_from = product_qr_master_row.acpqm_last_scaned_by

            product_qr_master_row.acpqm_last_modified_by = current_user
            product_qr_master_row.acpqm_last_scaned_from = lastscaned_from
            product_qr_master_row.acpqm_last_scaned_by = current_user
            product_qr_master_row.acpqm_product_movment_details = str(product_qr_master_row.acpqm_product_movment_details) + ",from ("+ str(lastscaned_from.username)+") to admin("+ str(current_user.username)+"):status=unused "


            product_assigned_exist = Projects_Product_Assigned.objects.filter(
                ppa_product_qr_detais=product_qr_master_row).exists()

            if product_assigned_exist:
                product_assigned = Projects_Product_Assigned.objects.get(
                    ppa_product_qr_detais=product_qr_master_row,ppa_last_scaned_by = last_scaned_by_asigned)

                product_assigned.ppa_last_scaned_by = current_user
                product_assigned.ppa_last_scaned_from = lastscaned_from
                product_assigned.ppa_last_modified_by = current_user

                # product_assigned.save()
                # product_qr_master_row.save()


                #debit from sender(user/manager)
                user = lastscaned_from
                qrcode_number = qr_code_number
                amount = str(product_qr_master_row.acpqm_product_master_id.acpm_product_amount)
                trans_with = current_user
                credit_or_debit = "debit"
                transection_status_admin= product_transection_fun(user,qrcode_number,amount,trans_with,credit_or_debit)
                #print('transection_status_admin------------------',transection_status_admin )
                if transection_status_admin['status'] == 1:

                    #credit to receiver(admin)
                    user = current_user
                    qrcode_number = qr_code_number
                    amount = str(product_qr_master_row.acpqm_product_master_id.acpm_product_amount)
                    trans_with = lastscaned_from
                    credit_or_debit = "credit"
                    transection_status_project_manager = product_transection_fun(user,qrcode_number,amount,trans_with,credit_or_debit)
                    #print('transection_status_project_manager------------------------',transection_status_project_manager)
                    if transection_status_project_manager['status'] == 1:

                        product_assigned.save()
                        product_qr_master_row.save()

                        messages.success(request, "product receive successfull")
                        return redirect('receive_unused_product')
                    else:
                        error_msg = "product recived failed and transection failed due to "+str(transection_status_admin)+" "+str(transection_status_project_manager)
                        messages.error(request, error_msg)
                        return redirect('receive_unused_product')
                else:

                    error_msg = "transection failed due to "+ str(transection_status_admin)
                    messages.error(request, error_msg)
                    return redirect('receive_unused_product')
            else:

                messages.error(request, "Product not assigned to any user or project manager")
                return redirect('receive_unused_product')
        else:
            messages.error(request, "QR Data not found in inventory.")
            return redirect('receive_unused_product')

@login_required(login_url='/login/')
def receive_faulty_product(request):
    if request.method == 'GET':
        data = product_catagory.objects.filter(acpc_is_active=True)

        context = {"product_cat": data}
        return render(request, 'admin_dashboard/receive_faulty_product.html',context)
    else:
        current_user = request.user

        qr_code_number = request.POST.get("barcode_details")    #e7c18d33e17c11ebb6a157968fde45e <class 'str'>

        qrrcode_exists = product_qr_master.objects.filter(
            acpqm_uniq_id=qr_code_number).exists()
        if qrrcode_exists:  # when barcode data exist
            product_qr_master_row = product_qr_master.objects.get(
                acpqm_uniq_id=qr_code_number)

            if (product_qr_master_row.acpqm_last_scaned_by == current_user and product_qr_master_row.acpqm_is_defective == True):
                messages.error(request, "Product already received")
                return redirect('receive_faulty_product')


            product_master_row = product_qr_master_row.acpqm_product_master_id
            last_scaned_by_asigned = product_qr_master_row.acpqm_last_scaned_by

            product_qr_master_row.acpqm_is_defective=True
            lastscaned_from = product_qr_master_row.acpqm_last_scaned_by

            product_qr_master_row.acpqm_last_modified_by = current_user
            product_qr_master_row.acpqm_last_scaned_from = lastscaned_from
            product_qr_master_row.acpqm_last_scaned_by = current_user
            product_qr_master_row.acpqm_product_movment_details = str(product_qr_master_row.acpqm_product_movment_details) + ",from ("+ str(lastscaned_from.username)+") to admin("+ str(current_user.username)+")status:faulty "


            product_assigned_exist = Projects_Product_Assigned.objects.filter(
                ppa_product_qr_detais=product_qr_master_row).exists()

            if product_assigned_exist:
                product_assigned = Projects_Product_Assigned.objects.get(
                    ppa_product_qr_detais=product_qr_master_row, ppa_last_scaned_by = last_scaned_by_asigned)

                product_assigned.ppa_last_scaned_by = current_user
                product_assigned.ppa_last_scaned_from = lastscaned_from
                product_assigned.ppa_last_modified_by = current_user

                # product_assigned.save()
                # product_qr_master_row.save()

                #debit from sender
                user = lastscaned_from
                qrcode_number = qr_code_number
                amount = str(product_qr_master_row.acpqm_product_master_id.acpm_product_amount)
                trans_with = current_user
                credit_or_debit = "debit"
                transection_status_admin= product_transection_fun(user,qrcode_number,amount,trans_with,credit_or_debit)
                #print('transection_status_admin------------------',transection_status_admin )
                if transection_status_admin['status'] == 1:

                    #credit to receiver
                    user = current_user
                    qrcode_number = qr_code_number
                    amount = str(product_qr_master_row.acpqm_product_master_id.acpm_product_amount)
                    trans_with = lastscaned_from
                    credit_or_debit = "credit"
                    transection_status_project_manager = product_transection_fun(user,qrcode_number,amount,trans_with,credit_or_debit)
                    #print('transection_status_project_manager------------------------',transection_status_project_manager)
                    if transection_status_project_manager['status'] == 1:

                        product_assigned.save()
                        product_qr_master_row.save()

                        messages.success(request, "product receive successfull")
                        return redirect('receive_faulty_product')
                    else:
                        error_msg = "product recived failed and transection failed due to "+str(transection_status_admin)+" "+str(transection_status_project_manager)
                        messages.error(request, error_msg)
                        return redirect('receive_faulty_product')
                else:

                    error_msg = "transection failed due to "+ str(transection_status_admin)
                    messages.error(request, error_msg)
                    return redirect('receive_faulty_product')


            else:

                messages.error(request, "product not assigned to any user or project manager")
                return redirect('receive_faulty_product')
        else:
            messages.error(request, "QR Data not found in inventory.")
            return redirect('receive_faulty_product')

        return redirect('receive_faulty_product')


@login_required(login_url='/login/')
def view_faulty_product(request):
    if request.method == 'GET':
        #query_results = site_master.objects.all()
        curent_page = 1
        pagedata_starting = 0
        pagedata_ending = pagedata_starting + 20

        prev_pagenumber = 1
        next_page_number = 2
        totaldata = product_qr_master.objects.filter(acpqm_is_defective=True).order_by('acpqm_created_at').count()

        query_results = product_qr_master.objects.filter(acpqm_is_defective=True).order_by('acpqm_created_at')[:pagedata_ending]
        showingdata = query_results.count()

        product_name_list = product_master.objects.order_by().values('acpm_product_name').distinct()
        product_cat_list = product_catagory.objects.order_by().values('acpc_catagory_name').distinct()
        product_qr_list = product_qr_master.objects.order_by().values('acpqm_uniq_id').distinct()
        product_print_list = product_qr_master.objects.order_by().values('acpqm_print_uniq_id').distinct()



        context = {"query_results": query_results,
                   'totaldata': totaldata,
                   'curent_page': curent_page,
                   'pagedata_starting': pagedata_starting,
                   'prev_pagenumber': prev_pagenumber,
                   'next_page_number': next_page_number,
                   'showingdata': showingdata,
                   "product_name_list":product_name_list,
                   "product_cat_list":product_cat_list,
                   "product_qr_list":product_qr_list,
                   "product_print_list":product_print_list
                   }
        return render(request, 'admin/inventory_view_faulty.html', context)



@login_required(login_url='/login/')
def view_faulty_product_pagination(request, page_number):
    if request.method == 'GET':
        #query_results = site_master.objects.all()
        if page_number != 1:
            curent_page = int(page_number)
            page_number = page_number-1
            prev_pagenumber = curent_page - 1
            pagedata_starting = page_number * 20
            pagedata_ending = pagedata_starting + 20
        else:
            curent_page = 1
            page_number = 1
            prev_pagenumber = 1
            pagedata_starting = 0
            pagedata_ending = pagedata_starting + 20

        next_page_number = curent_page + 1

        totaldata = product_qr_master.objects.filter(acpqm_is_defective=True).order_by('acpqm_created_at').count()

        query_results = product_qr_master.objects.filter(acpqm_is_defective=True).order_by('acpqm_created_at')[pagedata_starting:pagedata_ending]
        showingdata = query_results.count()

        product_name_list = product_master.objects.order_by().values('acpm_product_name').distinct()
        product_cat_list = product_catagory.objects.order_by().values('acpc_catagory_name').distinct()
        product_qr_list = product_qr_master.objects.order_by().values('acpqm_uniq_id').distinct()
        product_print_list = product_qr_master.objects.order_by().values('acpqm_print_uniq_id').distinct()

        context = {"query_results": query_results,
                   'totaldata': totaldata,
                   'curent_page': curent_page,
                   'pagedata_starting': pagedata_starting,
                   'prev_pagenumber': prev_pagenumber,
                   'next_page_number': next_page_number,
                   'showingdata': showingdata,
                   "product_name_list":product_name_list,
                   "product_cat_list":product_cat_list,
                   "product_qr_list":product_qr_list,
                   "product_print_list":product_print_list
                   }
        return render(request, 'admin/inventory_view.html', context)
    else:

        product_name_search = request.POST.get("product_name_search")
        Product_catagory_search = request.POST.get("Product_catagory_search")
        Product_qr_code_availale = request.POST.get("Product_qr_code_availale")
        Product_print_code_availale = request.POST.get("Product_print_code_availale")

        page_number = request.POST.get("page_number")
        page_number= int(page_number)

        from_date = request.POST.get("from_date")
        to_date = request.POST.get("to_date")

        # print(type(product_name_search),'product_name_search')
        # print(Product_catagory_search,'Product_catagory_search')
        # print(Product_qr_code_availale,'Product_qr_code_availale')
        # print(Product_print_code_availale,'Product_print_code_availale')
        #print(from_date,'from_date')
        #print(to_date,'to_date')


        if page_number != 1:
            curent_page = int(page_number)
            page_number = page_number-1
            prev_pagenumber = curent_page - 1
            pagedata_starting = page_number * 20
            pagedata_ending = pagedata_starting + 20
        else:
            curent_page = 1
            page_number = 1
            prev_pagenumber = 1
            pagedata_starting = 0
            pagedata_ending = pagedata_starting + 20

        next_page_number = curent_page + 1

        if from_date=='' or to_date =='':


            totaldata = product_qr_master.objects.filter(acpqm_product_master_id__acpm_product_name__contains=product_name_search,
                                                         acpqm_product_master_id__acpm_product_catagory__acpc_catagory_name__contains=Product_catagory_search,
                                                         acpqm_uniq_id__contains=Product_qr_code_availale,
                                                         acpqm_print_uniq_id__contains=Product_print_code_availale,
                                                         acpqm_is_defective=True).order_by('acpqm_created_at').count()

            #query_results = product_qr_master.objects.all().order_by('acpqm_created_at')[pagedata_starting:pagedata_ending]


            query_results = product_qr_master.objects.filter(acpqm_product_master_id__acpm_product_name__contains=product_name_search,
                                                         acpqm_product_master_id__acpm_product_catagory__acpc_catagory_name__contains=Product_catagory_search,
                                                         acpqm_uniq_id__contains=Product_qr_code_availale,
                                                         acpqm_print_uniq_id__contains=Product_print_code_availale,
                                                         acpqm_is_defective=True).order_by('acpqm_created_at')[pagedata_starting:pagedata_ending]
        else:


            totaldata = product_qr_master.objects.filter(acpqm_product_master_id__acpm_product_name__contains=product_name_search,
                                                         acpqm_product_master_id__acpm_product_catagory__acpc_catagory_name__contains=Product_catagory_search,
                                                         acpqm_uniq_id__contains=Product_qr_code_availale,
                                                         acpqm_print_uniq_id__contains=Product_print_code_availale,
                                                         acpqm_is_defective=True,
                                                         acpqm_created_at__range=[from_date, to_date]).order_by('acpqm_created_at').count()

            #query_results = product_qr_master.objects.all().order_by('acpqm_created_at')[pagedata_starting:pagedata_ending]


            query_results = product_qr_master.objects.filter(acpqm_product_master_id__acpm_product_name__contains=product_name_search,
                                                         acpqm_product_master_id__acpm_product_catagory__acpc_catagory_name__contains=Product_catagory_search,
                                                         acpqm_uniq_id__contains=Product_qr_code_availale,
                                                         acpqm_print_uniq_id__contains=Product_print_code_availale,
                                                         acpqm_is_defective=True,
                                                         acpqm_created_at__range=[from_date, to_date]).order_by('acpqm_created_at')[pagedata_starting:pagedata_ending]

        showingdata = query_results.count()

        product_name_list = product_master.objects.order_by().values('acpm_product_name').distinct()
        product_cat_list = product_catagory.objects.order_by().values('acpc_catagory_name').distinct()
        product_qr_list = product_qr_master.objects.order_by().values('acpqm_uniq_id').distinct()
        product_print_list = product_qr_master.objects.order_by().values('acpqm_print_uniq_id').distinct()

        context = {"query_results": query_results,
                   'totaldata': totaldata,
                   'curent_page': curent_page,
                   'pagedata_starting': pagedata_starting,
                   'prev_pagenumber': prev_pagenumber,
                   'next_page_number': next_page_number,
                   'showingdata': showingdata,
                   "product_name_list":product_name_list,
                   "product_cat_list":product_cat_list,
                   "product_qr_list":product_qr_list,
                   "product_print_list":product_print_list,

                   "product_name_search":product_name_search,
                   "Product_catagory_search":Product_catagory_search,
                   "Product_qr_code_availale":Product_qr_code_availale,
                   "Product_print_code_availale":Product_print_code_availale,
                   "from_date":from_date,
                   "to_date":to_date,

                   }
        return render(request, 'admin/inventory_view_faulty.html', context)


@login_required(login_url='/login/')
def product_assigned_to(request, project_id):
    user = request.user
    groupid = user.groups.values_list('id', flat=True).first()
    groupname = user.groups.values_list('name', flat=True).first()

    if request.method == 'GET':
        project_exist = Project_Master.objects.filter(pm_id=project_id).exists()
        if project_exist:
            project_master_id = Project_Master.objects.get(pm_id=project_id)
            project_product_assignment = Projects_Product_Assigned.objects.filter(ppa_project_master_id=project_master_id).exists()
            if project_product_assignment:
                assigned_data = Projects_Product_Assigned.objects.filter(ppa_project_master_id=project_master_id)

                context = {'assigned_data': assigned_data,
                           'project_details': Project_Master.objects.filter(pm_id=project_id),
                           'groupid':groupid,
                           'groupname':groupname}

                return render(request, 'admin_dashboard/details_of_project_product_assigned.html', context)
            else:
                messages.error(request, "Till now no product assigned to any user for this project.")
                return redirect('details_of_project', project_id=project_id)

        else:
            messages.error(request, "Project not found for this id.")

            return render(request, '404.html')


@login_required(login_url='/login/')
def install_product_toproject(request, project_id):
    user = request.user
    groupid = user.groups.values_list('id', flat=True).first()
    groupname = user.groups.values_list('name', flat=True).first()

    if request.method == 'GET':
        project_exist = Project_Master.objects.filter(pm_id=project_id).exists()
        if project_exist:
            project_master_id = Project_Master.objects.get(pm_id=project_id)
            Projects_Product_Installed_exists = Projects_Product_Installed.objects.filter(ppi_project_master_id=project_master_id).exists()

            if Projects_Product_Installed_exists:
                Projects_Product_Installed_product = Projects_Product_Installed.objects.filter(ppi_project_master_id=project_master_id)

                context = {'installed_product': Projects_Product_Installed_product,
                           'project_details': Project_Master.objects.filter(pm_id=project_id),
                           'groupid':groupid,
                           'groupname':groupname,
                           'project_id':project_id,
                           "status":1}

                return render(request, 'admin_dashboard/install_product_toproject_view.html', context)
            else:

                context = {'installed_product':{},
                           'project_details': Project_Master.objects.filter(pm_id=project_id),
                           'groupid':groupid,
                           'groupname':groupname,
                           'project_id':project_id,
                           "status":0}

                return render(request, 'admin_dashboard/install_product_toproject_view.html', context)

        else:
            messages.error(request, "Project not found for this id.")

            return render(request, '404.html')


def install_one_product_toproject(request,project_id):
    if request.method =='GET':
        current_user = request.user
        groupid = current_user.groups.values_list('id', flat=True).first()
        groupname = current_user.groups.values_list('name', flat=True).first()

        context = { 'groupid':groupid,
                     'project_id':project_id,
                    'groupname':groupname
                   }

        return render(request,'admin_dashboard/install_one_product_toproject.html', context)

    else:
        #print("post enterrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr")

        file_content = request.FILES['imagewc']
        # vars(file_content)
        # print(vars(file_content),'varsssssssss')
        # {'file': <_io.BytesIO object at 0x7fc266d750e0>,
        # '_name': '0b948a00f9cd11ebb46b0998520a31ff.png',
        #  'size': 734, 'content_type': 'image/png',
        #   'charset': None, 'content_type_extra': {},
        #    'field_name': 'imagewc'}
        if allowed_file_image(file_content.name):
            pass
        else:
            messages.error(request, "image should be 'png', 'jpg', 'jpeg'type")
            return redirect('install_one_product_toproject',project_id=project_id)


        current_user = request.user
        product_qr_code = request.POST.get("product_qr_code")
        product_quantity = request.POST.get("product_quantity")
        qrcode_details_exists = product_qr_master.objects.filter(acpqm_uniq_id=product_qr_code,acpqm_last_scaned_by=current_user).exists()
        if not qrcode_details_exists:
            #check qr code exists

            messages.error(request, "No product found with this qr code in your stock.")
            return redirect('install_one_product_toproject',project_id=project_id )
        else:
            qrcode_details = product_qr_master.objects.get(acpqm_uniq_id=product_qr_code)

        project_details_exists = Project_Master.objects.filter(pk=project_id).exists()
        if not project_details_exists:
            #check product exists

            messages.error(request, "no projects exist with this id")
            return redirect('install_one_product_toproject',project_id=project_id )
        else:
            project_details = Project_Master.objects.get(pk=project_id)


        #check product name exist
        product_name_exist_in_project = Projects_Product.objects.filter(pp_project_master_id = project_details, pp_product_id__pt_product_name = qrcode_details.acpqm_product_master_id.acpm_product_name).exists()
        if product_name_exist_in_project:
            product_name = qrcode_details.acpqm_product_master_id.acpm_product_name
        else:
            messages.error(request, "This product name not present in this project.")
            return redirect('install_one_product_toproject',project_id=project_id )


        #check user present in this project
        curentuser_is_a_project_user = Projects_Users.objects.filter( pu_user=current_user, pu_project_master_id=project_details ).exists()
        if curentuser_is_a_project_user:
            #this user is authenticated
            pass

        else:
            messages.error(request, "This user is not a user of this pproject")
            return redirect('install_one_product_toproject',project_id=project_id)

        #check amount is available in user transections
        product_name_exists = product_transaction.objects.filter( pt_user = current_user, pt_product_name = product_name).exists()
        if product_name_exists:
            product_name_obj = product_transaction.objects.get( pt_user = current_user, pt_product_name = product_name)
            available_product_amount = product_name_obj.pt_product_amount

            product_quantity = int(product_quantity)
            available_product_amount = int(available_product_amount)

            if product_quantity <= available_product_amount:
                pass
            else:
                messages.error(request, "Product quantity is greater then you have.")
                return redirect('install_one_product_toproject',project_id=project_id)
        else:
            messages.error(request, "User dont have this product.")
            return redirect('install_one_product_toproject',project_id=project_id)


        projectcliest_user = project_details.pm_project_client


        user = current_user
        qrcode_number = product_qr_code
        amount = str(product_quantity)
        trans_with = projectcliest_user
        credit_or_debit = "debit"
        transection_status_user = product_transection_fun(user,qrcode_number,amount,trans_with,credit_or_debit)

        if transection_status_user['status'] == 1:

            c = Projects_Product_Installed(ppi_project_master_id=project_details,
                                           ppi_product_qr_detais=qrcode_details,
                                           ppi_installed_by= current_user,
                                           ppi_amount=product_quantity,
                                           ppi_last_modified_by = current_user
                                           )
            c.save()

            ppi_data = Projects_Product_Installed.objects.latest('ppi_id')
            ppi_id = ppi_data.ppi_id


            split_tup = os.path.splitext(file_content.name)
            file_name = split_tup[0]
            file_extension = split_tup[1]


            path_ex = "static/assets/instalation_img/"
            img_file_name = "Instaled_img_" + str(ppi_id) + file_extension

            complete_imagepath=path_ex+img_file_name


            fs = FileSystemStorage()
            filename = fs.save(complete_imagepath, file_content)

            ppi_data.ppi_install_image_path= path_ex
            ppi_data.ppi_install_image_name = img_file_name
            ppi_data.save()


            messages.success(request, "product installed successfully")
            return redirect('install_one_product_toproject',project_id=project_id)
        else:
            messages.error(request, "something went wrong:"+ transection_status_user['status']+" ")
            return redirect('install_one_product_toproject',project_id=project_id)


@login_required(login_url='/login/')
def details_of_project_history(request, project_id):

    if request.method == 'GET':        #start project  and update all product available if alredy exit through message do nothing
        project_details_by_id_exists = Project_Master.objects.filter(
                    pk=project_id, pm_is_active=True).exists()

        if project_details_by_id_exists:
            project_details_by_id = Project_Master.objects.filter(pk=project_id, pm_is_active=True)

            context = {'query_results': project_details_by_id,
                         }

            return render(request, 'admin_dashboard/details_of_project_history.html', context)
        else:
            messages.error(request, "no project found in this id")
            return redirect('details_of_project', project_id=project_id)



@login_required(login_url='/login/')
def start_project(request, project_id):
    if request.method == 'GET':
        now = timezone.localtime(timezone.now())
        current_user = request.user
        project_details_by_id = Project_Master.objects.get(
                    pk=project_id, pm_is_active=True)
        if project_details_by_id.pm_all_product_available == True:
            messages.error(request, "Project alredy started")
            return redirect('details_of_project', project_id=project_id)
        else:
            project_details_by_id.pm_all_product_available= True
            project_details_by_id.save()

            messages.success(request, "project started successfully ")

            project_details_by_id.pm_description = str(project_details_by_id.pm_description)+"project started by("+str(current_user.username) +")-- "+str(now)+".\n"
            project_details_by_id.save()

            return redirect('details_of_project', project_id=project_id)

    else:
        pass


@login_required(login_url='/login/')
def product_sold_directly(request):
    if request.method == 'GET':
        customer_data = CustomerDetails.objects.filter(cd_is_active=True)
        context = {"customer_data": customer_data}
        return render(request, 'admin_dashboard/product_sold_directly_view.html',context)
    else:
        current_user = request.user

        customer_id = request.POST.get("customer_id")
        customer_data_present= CustomerDetails.objects.filter(pk=customer_id,cd_is_active=True).exists()
        if customer_data_present :
            customer_data_present = CustomerDetails.objects.get(pk=customer_id,cd_is_active=True)

            c = DirectSell(ds_customer_details = customer_data_present,
                               ds_type = "direct",
                               ds_last_modified_by = current_user
                               )
            c.save()

            messages.success(request, "Direct sell created, please add product .")
            return redirect('view_sell')
        else:
            messages.error(request, "Select a valid customer. ")
            return redirect('product_sold_directly')




@login_required(login_url='/login/')
def scan_and_check(request):
    if request.method == 'GET':
        current_user = request.user
        groupid = current_user.groups.values_list('id', flat=True).first()
        groupname = current_user.groups.values_list('name', flat=True).first()

        context = { 'groupid':groupid,
                    'groupname':groupname
                   }
        return render(request, 'admin_dashboard/scan_and_check.html',context)

@login_required(login_url='/login/')
def admin_watching_user(request):
    if request.method == 'GET':
        total_manager_count = User.objects.filter(groups__name='project_user').count()

        total_manager_data = User.objects.filter(groups__name='project_user')
        context = {"total_manager_data": total_manager_data,
                   "total_manager_count":total_manager_count,
                   "usertype":'user'}
        return render(request, 'admin/admin_watching_user.html',context)
    else:
        current_user = request.user
        user_id = request.POST.get("user_id")
        user_id = str(user_id)
        if user_id == '0':
            messages.error(request, "Select a valid user. ")
            return redirect('admin_watching_user')

        user_id=int(user_id)


        userexists = User.objects.filter(groups__name='project_user',id=user_id).exists()
        if userexists :
            user_data = User.objects.filter(id=user_id)
            #print(user_data,'userdata')
        else:
            messages.error(request, "project user not exists ")
            return redirect('admin_watching_user')




        total_manager_count = User.objects.filter(groups__name='project_user').count()
        total_manager_data = User.objects.filter(groups__name='project_user')
        context = {"total_manager_data": total_manager_data,
                   "total_manager_count":total_manager_count,
                   "usertype":'user',
                   "user_data":user_data,
                    }
        return render(request, 'admin/admin_watching_user.html',context)

@login_required(login_url='/login/')
def admin_watching_project_manager(request):
    if request.method == 'GET':
        total_manager_count = User.objects.filter(groups__name='project_manager').count()

        total_manager_data = User.objects.filter(groups__name='project_manager')
        context = {"total_manager_data": total_manager_data,
                   "total_manager_count":total_manager_count,
                   "usertype":'manager'}
        return render(request, 'admin/admin_watching_user.html',context)
    else:
        current_user = request.user
        user_id = request.POST.get("user_id")
        user_id = str(user_id)
        if user_id == '0':
            messages.error(request, "Select a valid user. ")
            return redirect('admin_watching_project_manager')

        user_id=int(user_id)


        userexists = User.objects.filter(groups__name='project_manager',id=user_id).exists()
        if userexists :
            user_data = User.objects.filter(id=user_id)
            #print(user_data,'userdata')
        else:
            messages.error(request, "project manager not exists ")
            return redirect('admin_watching_project_manager')




        total_manager_count = User.objects.filter(groups__name='project_manager').count()
        total_manager_data = User.objects.filter(groups__name='project_manager')
        context = {"total_manager_data": total_manager_data,
                   "total_manager_count":total_manager_count,
                   "user_data":user_data,
                   "usertype":'manager'
                    }
        return render(request, 'admin/admin_watching_user.html',context)

@login_required(login_url='/login/')
def add_direct_customer(request):
    if request.method == 'GET':
        customer_data = CustomerDetails.objects.filter(cd_is_active=True)
        context = {"customer_data": customer_data}
        return render(request, 'admin_dashboard/add_direct_customer_view_form.html',context)
    else:
        current_user = request.user
        '''

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
        '''

        company_name = request.POST.get("company_name")
        contact_name = request.POST.get("contact_name")
        contact_number = request.POST.get("contact_number")
        gst_vat_number = request.POST.get("gst_vat_number")
        order_number = request.POST.get("order_number")

        customer_exists = CustomerDetails.objects.filter(cd_company_name= str(company_name),
                                                         cd_vat_gst_number= str(gst_vat_number),
                                                         ).exists()

        if customer_exists:
            messages.error(request, "Customer already exists. ")
            return redirect('add_direct_customer')
        else:
            c = CustomerDetails(cd_company_name = str(company_name),
                               cd_vat_gst_number = str(gst_vat_number),
                               cd_order_number = str(order_number),
                               cd_last_modified_by = current_user
                               )
            c.save()

            messages.success(request, "Customer added successfully .")
            return redirect('add_direct_customer')
@login_required(login_url='/login/')
def view_sell(request):
    if request.method == 'GET':
        # query_results = site_master.objects.all()
        curent_page = 1
        pagedata_starting = 0
        pagedata_ending = pagedata_starting + 20

        prev_pagenumber = 1
        next_page_number = 2
        totaldata = DirectSell.objects.all().order_by('ds_created_at').count()

        query_results = DirectSell.objects.all().order_by('-ds_created_at')[
            :pagedata_ending]
        showingdata = query_results.count()

        context = {"query_results": query_results,
                   'totaldata': totaldata,
                   'curent_page': curent_page,
                   'pagedata_starting': pagedata_starting,
                   'prev_pagenumber': prev_pagenumber,
                   'next_page_number': next_page_number,
                   'showingdata': showingdata

                   }
        return render(request, 'admin_dashboard/sell_view.html', context)

@login_required(login_url='/login/')
def view_sell_pagination(request, page_number):
    if request.method == 'GET':

        # query_results = site_master.objects.all()
        if page_number != 1:
            curent_page = int(page_number)
            page_number = page_number-1
            prev_pagenumber = curent_page - 1
            pagedata_starting = page_number * 20
            pagedata_ending = pagedata_starting + 20
        else:
            curent_page = 1
            page_number = 1
            prev_pagenumber = 1
            pagedata_starting = 0
            pagedata_ending = pagedata_starting + 20

        next_page_number = curent_page + 1

        totaldata = DirectSell.objects.all().order_by('ds_created_at').count()

        query_results = DirectSell.objects.all().order_by(
            'ds_created_at')[pagedata_starting:pagedata_ending]
        showingdata = query_results.count()

        context = {"query_results": query_results,
                   'totaldata': totaldata,
                   'curent_page': curent_page,
                   'pagedata_starting': pagedata_starting,
                   'prev_pagenumber': prev_pagenumber,
                   'next_page_number': next_page_number,
                   'showingdata': showingdata

                   }
        return render(request, 'admin_dashboard/sell_view.html', context)


@login_required(login_url='/login/')
def details_of_sell(request, sell_id):
    if request.method == 'GET':

        sell_exist = DirectSell.objects.filter(pk=sell_id).exists()
        if sell_exist:
            sell_details_by_id = DirectSell.objects.get(pk=sell_id)

            direct_sell_product_exist = CustomerProducts.objects.filter(cp_direct_sell=sell_details_by_id, cp_is_active=True).exists()
            direct_sell_product = {}
            if direct_sell_product_exist:
                direct_sell_product = CustomerProducts.objects.filter(cp_direct_sell=sell_details_by_id, cp_is_active=True)


            sell_details = DirectSell.objects.filter(pk=sell_id)
            direct_sell_user = User.objects.filter(groups__name='direct_sell_user',is_active=True).order_by('date_joined')


            context = {"sell_details": sell_details,
                       'direct_sell_product': direct_sell_product,
                       'sell_id':sell_id,
                       'direct_sell_user':direct_sell_user
                       }
            #print(context)
            return render(request, 'admin_dashboard/details_of_sell_view.html', context)
        else:
            messages.error(request, "Sell not found for this id.")
            return redirect('view_sell')


@login_required(login_url='/login/')
def scan_and_add_product_to_sell(request,ds_id):
    if request.method == 'GET':
        data = product_catagory.objects.filter(acpc_is_active=True)

        context = {"product_cat": data,'ds_id':ds_id}
        return render(request, 'admin_dashboard/scan_add_product_to_sell.html',context)
    else:
        current_user = request.user

        qr_code_number = request.POST.get("barcode_details")
        sell_id = request.POST.get("sell_id")
        amount = request.POST.get("product_quantity")




        #check direct sell id exis or not
        sell_id_exists = DirectSell.objects.filter(
            ds_id=sell_id).exists()
        if sell_id_exists:  # when barcode data exist
            sell_id_row = DirectSell.objects.get(
                ds_id=sell_id)
        else:
            messages.error(request, "no sell id exist for tis id")
            return redirect('scan_and_add_product_to_sell',ds_id=sell_id)




        #check product with qr details exis or not
        qrrcode_exists = product_qr_master.objects.filter(
            acpqm_uniq_id=qr_code_number).exists()
        if qrrcode_exists:  # when barcode data exist
            product_qr_master_row = product_qr_master.objects.get(
                acpqm_uniq_id=qr_code_number)
        else:
            messages.error(request, "no product exis in this qr code number")
            return redirect('scan_and_add_product_to_sell',ds_id=sell_id)



        #check product alredy added
        customer_product_exist = CustomerProducts.objects.filter(cp_product_qr_detais = product_qr_master_row,
                    cp_direct_sell = sell_id_row).exists()
        if customer_product_exist:
            messages.error(request, "Product alredy added to this ")
            return redirect('scan_and_add_product_to_sell',ds_id=sell_id)

        else:
            #insert data to table customerProducts
            ds = CustomerProducts(cp_product_qr_detais = product_qr_master_row,
                               cp_direct_sell = sell_id_row,
                               cp_amount = int(amount),
                               cp_last_modified_by = current_user
                               )
            ds.save()

        messages.success(request, "product added to sell id successfully")
        return redirect('scan_and_add_product_to_sell',ds_id=sell_id)

@login_required(login_url='/login/')
def remove_product_from_sell(request,ds_id,cp_id):
    if request.method == 'GET':
        customer_product_exist = CustomerProducts.objects.filter(cp_id = cp_id).exists()
        if customer_product_exist:
            #delete data from that table
            CustomerProducts.objects.filter(cp_id = cp_id).delete()

            messages.success(request, "successfully remove product")
            return redirect('details_of_sell', sell_id=ds_id)

        else:
            messages.error(request, "no product present to remove.")
            return redirect('details_of_sell', sell_id=ds_id)
    else:
        messages.error(request, "This method is not allowed")
        return redirect('details_of_sell', sell_id=ds_id)

@login_required(login_url='/login/')
def submit_direct_sell(request, sell_id):
    if request.method == 'POST':
        current_user = request.user

        direct_sell_user_id = request.POST.get("direct_sell_user")
        if direct_sell_user_id == "0":

            messages.error(request, "select a valid direct sell user or create.")
            return redirect('details_of_sell', sell_id=sell_id)

        sell_exist = DirectSell.objects.filter(pk=sell_id).exists()
        if sell_exist:
            sell_details_by_id = DirectSell.objects.get(pk=sell_id)

            direct_sell_product_exist = CustomerProducts.objects.filter(cp_direct_sell=sell_details_by_id, cp_is_active=True).exists()

            if direct_sell_product_exist:
                direct_sell_product = CustomerProducts.objects.filter(cp_direct_sell=sell_details_by_id, cp_is_active=True)
                #print(type(direct_sell_product))
                direc_sell_user = User.objects.get(pk=direct_sell_user_id, is_active=True)


                for i,c in enumerate(direct_sell_product):
                    #print (i, c, type(c))
                    #print(c.cp_product_qr_detais.acpqm_product_master_id.acpm_product_amount)
                    #print(c.cp_product_qr_detais.acpqm_uniq_id)
                    #print(c.cp_amount)


                    user = current_user
                    qrcode_number = str(c.cp_product_qr_detais.acpqm_uniq_id)
                    amount = str(c.cp_product_qr_detais.acpqm_product_master_id.acpm_product_amount)
                    trans_with = direc_sell_user
                    credit_or_debit = "debit"
                    transection_status_admin = product_transection_fun(user,qrcode_number,amount,trans_with,credit_or_debit)

                sell_details_by_id.ds_is_complete = True
                sell_details_by_id.save()


            return redirect('view_sell')
        else:
            messages.error(request, "Sell not found for this id.")
            return redirect('view_sell')
