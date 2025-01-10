from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib import messages

from admin_dashboard.models import Projects_Users,Project_Master,Projects_Product,Projects_Product_Assigned
from admin_account.models import product_qr_master
from admin_account.utils import product_transection_fun
from django.contrib.auth.decorators import login_required





# def site_create(request):
#     if request.method == "GET":
#         context = {"data":"data"}
#         return render(request, 'site_app/site_create_index.html', context)
#     else:
#         context = {"data":"data"}
#         return render(request, 'site_app/site_create_index.html', context)


def create_site_user(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':

        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")

        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "confirm password miss match.")
            form={'first_name': first_name,'last_name':last_name,'username':username,'email':email}

            return render(request, 'site_user/create_site_user_form.html',form )


        if User.objects.filter(email=email.lower()).exists():
            messages.error(request, "email alredy exist use another email.")
            form={'first_name': first_name,'last_name':last_name,'username':username,'email':email}

            return render(request, 'site_user/create_site_user_form.html',form )

        if User.objects.filter(username=username).exists():
            messages.error(request, "username alredy exist use another username.")
            form={'first_name': first_name,'last_name':last_name,'username':username,'email':email}

            return render(request, 'site_user/create_site_user_form.html',form )

        user = User.objects.create_user(
                                            first_name=first_name,
                                            last_name=last_name,
                                            username = username,
                                            password = password,
                                            email = email,
                                            is_active = True
                                        )
        user.save()


        profile_user = User.objects.get(username=username)
        print(profile_user.id)

        my_group = Group.objects.get(name='project_user')
        profile_user.groups.add(my_group)

        return redirect('view_site_user')

        #return redirect('view_siteuser')


    # if a GET (or any other method) we'll create a blank form
    else:
        form={'first_name': '','last_name':'','username':'','email':''}

    return render(request, 'site_user/create_site_user_form.html', {'form': form})


def create_direct_sell_user(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':

        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")

        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "confirm password miss match.")
            form={'first_name': first_name,'last_name':last_name,'username':username,'email':email}

            return render(request, 'site_user/create_direct_sell_user_form.html',form )
            #return render(request, 'site_user/create_site_user_form.html',form )


        if User.objects.filter(email=email.lower()).exists():
            messages.error(request, "email alredy exist use another email.")
            form={'first_name': first_name,'last_name':last_name,'username':username,'email':email}

            return render(request, 'site_user/create_direct_sell_user_form.html',form )
            #return render(request, 'site_user/create_site_user_form.html',form )

        if User.objects.filter(username=username).exists():
            messages.error(request, "username alredy exist use another username.")
            form={'first_name': first_name,'last_name':last_name,'username':username,'email':email}

            return render(request, 'site_user/create_direct_sell_user_form.html',form )
            #return render(request, 'site_user/create_site_user_form.html',form )

        user = User.objects.create_user(
                                            first_name=first_name,
                                            last_name=last_name,
                                            username = username,
                                            password = password,
                                            email = email,
                                            is_active = True
                                        )
        user.save()


        profile_user = User.objects.get(username=username)
        print(profile_user.id)

        my_group = Group.objects.get(name='direct_sell_user')
        profile_user.groups.add(my_group)

        return redirect('view_direct_sell_user')

        #return redirect('view_siteuser')


    # if a GET (or any other method) we'll create a blank form
    else:
        form={'first_name': '','last_name':'','username':'','email':''}

    return render(request, 'site_user/create_direct_sell_user_form.html', {'form': form})

def view_site_user(request):
    if request.method =='GET':
        #query_results = site_master.objects.all()
        curent_page = 1
        pagedata_starting = 0
        pagedata_ending = pagedata_starting + 20

        prev_pagenumber = 1
        next_page_number = 2
        totaldata = users = User.objects.filter(
            groups__name='project_user').count()

        query_results = User.objects.filter(
            groups__name='project_user').order_by('date_joined')[:pagedata_ending]
        showingdata = query_results.count()


        context = {"query_results":query_results,
                   'totaldata':totaldata,
                   'curent_page':curent_page,
                   'pagedata_starting':pagedata_starting,
                   'prev_pagenumber':prev_pagenumber,
                   'next_page_number':next_page_number,
                   'showingdata':showingdata

                   }
        return render(request, 'site_user/site_user_view.html', context)






def site_user_pagination(request,page_number):
    if request.method =='GET':

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

        totaldata = users = User.objects.filter(
            groups__name='project_user').count()

        query_results = User.objects.filter(groups__name='project_user').order_by(
            'date_joined')[pagedata_starting:pagedata_ending]
        showingdata = query_results.count()



        context = {"query_results":query_results,
                   'totaldata':totaldata,
                   'curent_page':curent_page,
                   'pagedata_starting':pagedata_starting,
                   'prev_pagenumber':prev_pagenumber,
                   'next_page_number':next_page_number,
                   'showingdata':showingdata

                   }
        return render(request, 'site_user/site_user_view.html', context)

def view_direct_sell_user(request):
    if request.method =='GET':
        #query_results = site_master.objects.all()
        curent_page = 1
        pagedata_starting = 0
        pagedata_ending = pagedata_starting + 20

        prev_pagenumber = 1
        next_page_number = 2
        totaldata = users = User.objects.filter(
            groups__name='project_user').count()

        query_results = User.objects.filter(
            groups__name='direct_sell_user').order_by('date_joined')[:pagedata_ending]
        showingdata = query_results.count()


        context = {"query_results":query_results,
                   'totaldata':totaldata,
                   'curent_page':curent_page,
                   'pagedata_starting':pagedata_starting,
                   'prev_pagenumber':prev_pagenumber,
                   'next_page_number':next_page_number,
                   'showingdata':showingdata

                   }
        return render(request, 'site_user/direct_sell_user_view.html', context)

def view_direct_sell_user_pagination(request,page_number):
    if request.method =='GET':

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

        totaldata = users = User.objects.filter(
            groups__name='project_user').count()

        query_results = User.objects.filter(groups__name='direct_sell_user').order_by(
            'date_joined')[pagedata_starting:pagedata_ending]
        showingdata = query_results.count()



        context = {"query_results":query_results,
                   'totaldata':totaldata,
                   'curent_page':curent_page,
                   'pagedata_starting':pagedata_starting,
                   'prev_pagenumber':prev_pagenumber,
                   'next_page_number':next_page_number,
                   'showingdata':showingdata

                   }
        return render(request, 'site_user/direct_sell_user_view.html', context)


@login_required(login_url='/login/')
def project_user_view_projects(request):
    if request.method =='GET':
        current_user = request.user
        print(current_user.id)

        groupid = current_user.groups.values_list('id', flat=True).first()
        groupname = current_user.groups.values_list('name', flat=True).first()

        curent_page = 1
        pagedata_starting = 0
        pagedata_ending = pagedata_starting + 20

        prev_pagenumber = 1
        next_page_number = 2
        totaldata = Projects_Users.objects.filter(pu_user=current_user).count()

        query_results = Projects_Users.objects.filter(pu_user=current_user).order_by('-pu_created_at')[
            :pagedata_ending]
        showingdata = query_results.count()

        context = {"query_results": query_results,
                   'totaldata': totaldata,
                   'curent_page': curent_page,
                   'pagedata_starting': pagedata_starting,
                   'prev_pagenumber': prev_pagenumber,
                   'next_page_number': next_page_number,
                   'showingdata': showingdata,
                   'groupid':groupid,
                    'groupname':groupname

                   }
        print(context)
        return render(request, 'site_user/project_view.html', context)
    else:
        pass
@login_required(login_url='/login/')
def project_user_view_projects_pagination(request,page_number):
    if request.method =='GET':
        current_user = request.user
        print(current_user.id)

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

        totaldata = users = Projects_Users.objects.filter(pu_user=current_user).count()

        query_results = Projects_Users.objects.filter(pu_user=current_user).order_by('-pu_created_at')[pagedata_starting:pagedata_ending]
        showingdata = query_results.count()


        groupid = current_user.groups.values_list('id', flat=True).first()
        groupname = current_user.groups.values_list('name', flat=True).first()



        context = {"query_results":query_results,
                   'totaldata':totaldata,
                   'curent_page':curent_page,
                   'pagedata_starting':pagedata_starting,
                   'prev_pagenumber':prev_pagenumber,
                   'next_page_number':next_page_number,
                   'showingdata':showingdata,
                    'groupid':groupid,
                    'groupname':groupname

                   }
        return render(request, 'site_user/project_view.html', context)

@login_required(login_url='/login/')
def pru_scan_and_receive(request,project_id):
    if request.method =='GET':
        current_user = request.user
        groupid = current_user.groups.values_list('id', flat=True).first()
        groupname = current_user.groups.values_list('name', flat=True).first()

        context = { 'groupid':groupid,
                     'project_id':project_id,
                    'groupname':groupname
                   }

        return render(request, 'site_user/scann_and_recive_product.html', context)

    else:
        current_user = request.user
        product_qr_code = request.POST.get("product_qr_code")
        product_receiving_location = request.POST.get("product_receiving_location")
        qrcode_details_exists = product_qr_master.objects.filter(acpqm_uniq_id=product_qr_code).exists()
        if not qrcode_details_exists:

            messages.error(request, "no product found with this qr code")
            return redirect('pru_scan_and_receive',project_id=project_id )
        else:
            qrcode_details = product_qr_master.objects.get(acpqm_uniq_id=product_qr_code)

        project_details_exists = Project_Master.objects.filter(pk=project_id).exists()
        if not project_details_exists:

            messages.error(request, "no projects exist with this id")
            return redirect('pru_scan_and_receive',project_id=project_id )
        else:
            project_details = Project_Master.objects.get(pk=project_id)



        #check if product exist in projects_product table of coresponding project id
        product_name_exist_in_project = Projects_Product.objects.filter(pp_project_master_id = project_details, pp_product_id__pt_product_name = qrcode_details.acpqm_product_master_id.acpm_product_name).exists()
        if product_name_exist_in_project:
            #enter product to assigned
            #check if already asigned
            already_asigned = Projects_Product_Assigned.objects.filter(ppa_project_master_id=project_details,
                                                        ppa_product_qr_detais=qrcode_details,
                                                        ppa_product_id = qrcode_details.acpqm_product_master_id,
                                                        ppa_last_scaned_by=current_user).exists()
            if already_asigned :
                messages.error(request, "alredy recived ")
                return redirect('pru_scan_and_receive',project_id=project_id )

            else:
                any_project_manager_exist = Projects_Users.objects.filter(pu_project_master_id=project_details, pu_group_id__name='project_manager',pu_is_active=True).exists()
                if any_project_manager_exist:
                    project_manager_userdata = Projects_Users.objects.get(pu_project_master_id=project_details, pu_group_id__name='project_manager',pu_is_active=True)
                    superusers = project_manager_userdata.pu_user
                else:
                    messages.error(request, " No project manager found in this project, operation can not be done")
                    return redirect('pru_scan_and_receive',project_id=project_id )

                product_assigned = Projects_Product_Assigned(ppa_project_master_id=project_details,
                                                            ppa_product_qr_detais=qrcode_details,
                                                            ppa_product_id = qrcode_details.acpqm_product_master_id,
                                                            ppa_last_scaned_by=current_user,
                                                            ppa_last_scaned_from=superusers,
                                                            ppa_product_amount = qrcode_details.acpqm_product_master_id.acpm_product_amount,
                                                            ppa_last_modified_by = current_user
                                                            )
                #product_assigned.save() this is afer successfull transection
                qrcode_details.acpqm_product_movment_details = str(qrcode_details.acpqm_product_movment_details) + ",from project manager("+ str(superusers.username)+") to user("+ str(current_user.username)+") "
                qrcode_details.acpqm_last_scaned_from = superusers
                qrcode_details.acpqm_last_scaned_by = current_user
                qrcode_details.acpqm_product_location = qrcode_details.acpqm_product_location + "(" +product_receiving_location +" :by: "+ str(current_user.username)+") "
                qrcode_details.acpqm_last_modified_by = current_user
                #qrcode_details.save()   this is afer successfull transection

                #debit from admin
                user = superusers
                qrcode_number = product_qr_code
                amount = str(qrcode_details.acpqm_product_master_id.acpm_product_amount)
                trans_with = current_user
                credit_or_debit = "debit"
                transection_status_admin= product_transection_fun(user,qrcode_number,amount,trans_with,credit_or_debit)
                print('transection_status_admin------------------',transection_status_admin )
                if transection_status_admin['status'] == 1:

                    #credit to scaner
                    user = current_user
                    qrcode_number = product_qr_code
                    amount = str(qrcode_details.acpqm_product_master_id.acpm_product_amount)
                    trans_with = superusers
                    credit_or_debit = "credit"
                    transection_status_project_manager = product_transection_fun(user,qrcode_number,amount,trans_with,credit_or_debit)
                    print('transection_status_project_manager------------------------',transection_status_project_manager)
                    if transection_status_project_manager['status'] == 1:
                        product_assigned.save()
                        qrcode_details.save()

                        messages.success(request, "product received successfully")
                        return redirect('pru_scan_and_receive',project_id=project_id )
                    else:
                        error_msg = "product recived failed and transection failed due to "+str(transection_status_admin)+" "+str(transection_status_project_manager)
                        messages.error(request, error_msg)
                        return redirect('pru_scan_and_receive',project_id=project_id )
                else:

                    error_msg = "transection failed due to "+ str(transection_status_admin)
                    messages.error(request, error_msg)
                    return redirect('pru_scan_and_receive',project_id=project_id )

        else:

            messages.error(request, "no product exist with this id .")
            return redirect('pru_scan_and_receive',project_id=project_id )
