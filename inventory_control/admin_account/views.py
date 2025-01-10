from django.shortcuts import render, redirect
import json
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.forms.models import model_to_dict
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from admin_dashboard.models import *
from PIL import Image
from django.conf import settings


#from django.contrib.gis.utils import GeoIP
import qrcode
import uuid


from django.http import JsonResponse
from .utils import base64_to_barcodenumber,product_transection_fun,insert_product_qrmaster


def admin_login(request):
    if request.method == "GET":
        context = {"data": "data"}
        return render(request, 'login.html', context)
    else:
        context = {"data": "data"}
        return render(request, 'login.html', context)

def logout_view(request):
    logout(request)
    return redirect('admin_login')

    # Redirect to a success page.


@login_required(login_url='/login/')
def lattes_qrcode(request,print_id):
    if request.method == "GET":

        query_results_exists = product_qr_master.objects.filter(acpqm_print_uniq_id=print_id).order_by('acpqm_created_at').exists()
        if not query_results_exists:
            messages.error(request, "no qr code or print id exist to print")
            return redirect('inventory_view')

        query_results = product_qr_master.objects.filter(acpqm_print_uniq_id=print_id).order_by('acpqm_created_at')

        img_list=[]
        for row_data in query_results:
            img_path = row_data.acpqm_qr_image_path
            img_name = row_data.acpqm_qr_image_name
            img_list.append(img_path+img_name)
        im_list=[]
        print(img_list)
        for imagename in img_list:
            im1 = Image.open(imagename)
            im_list.append(im1)

        print(im_list)

        path = settings.STATIC_ROOT+"/assets/pdf/"
        pdf_fil_ename = path+print_id+".pdf"
        im1.save(pdf_fil_ename, "PDF" ,resolution=100.0, save_all=True, append_images=im_list)

        context = {"query_results": query_results,"print_id":print_id}
        return render(request, 'admin/lattest_qrcode.html', context)
    else:

        print_id = request.POST.get("print_code")

        query_results_exists = product_qr_master.objects.filter(acpqm_print_uniq_id=print_id).order_by('acpqm_created_at').exists()
        if not query_results_exists:
            messages.error(request, "no qr code or print id exist to print")
            return redirect('inventory_view')

        query_results = product_qr_master.objects.filter(acpqm_print_uniq_id=print_id).order_by('acpqm_created_at')


        img_list=[]
        for row_data in query_results:
            img_path = row_data.acpqm_qr_image_path
            img_name = row_data.acpqm_qr_image_name
            img_list.append(img_path+img_name)
        im_list=[]
        for imagename in img_list:
            im1 = Image.open(imagename)
            im_list.append(im1)
        path = settings.STATIC_ROOT+"/assets/pdf/"
        pdf_fil_ename = path+print_id+".pdf"
        pdfimg = im_list[0]
        pdfimg.save(pdf_fil_ename, "PDF" ,resolution=100.0, save_all=True, append_images=im_list)



        context = {"query_results": query_results,"print_id":print_id}
        return render(request, 'admin/lattest_qrcode.html', context)


@login_required(login_url='/login/')
def add_new_product(request):
    if request.method == "GET":
        current_user = request.user
        data = product_catagory.objects.filter(acpc_is_active=True,acpc_fra_or_single='single')
        main_catagory = product_main_catagory.objects.filter(pmc_is_active=True)

        #uniq_product_name = product_transaction.objects.values('pt_product_name').distinct()
        uniq_product_name = product_transaction.objects.filter(pt_product_catagory__acpc_fra_or_single = 'single')

        context = {"product_cat": data,"product_cat_main": main_catagory,"uniq_product_name":uniq_product_name}

        return render(request, 'admin/admin_add_single_product.html', context)
    else:
        current_user = request.user
        user_id = current_user.id

        input_catagory_name = request.POST.get("input_catagory_name").strip()
        catagory_id = request.POST.get("catagory_id")

        input_catagory_main = request.POST.get("input_main_catagory_name").strip()

        main_catagory_id = request.POST.get("main_catagory_id") 
        name_of_product = request.POST.get("product_names").strip()

        number_of_product = request.POST.get("number_of_product")
        number_of_product = int(number_of_product)

        # print(catagory_id, 'catagory_id')
        # print(type(catagory_id))
        # print(input_catagory_name, 'input_catagory_name')
        if catagory_id == '0':
            # check if catagory exist if not create a catagory
            data_catagory_exist = product_catagory.objects.filter(
                acpc_catagory_name=input_catagory_name).exists()
            if not data_catagory_exist:

                b = product_catagory(acpc_catagory_name=input_catagory_name,
                                     acpc_fra_or_single = 'single',
                                     acpc_last_modified_by=current_user)
                b.save()
            else:
                data_catagory = product_catagory.objects.get(acpc_catagory_name=input_catagory_name)
                if data_catagory.acpc_fra_or_single != 'single':
                    messages.error(request, "This catagory already exist in fractional catagory please choose a diffrent name for catagory ")
                    return redirect('add_new_product')
        
        if main_catagory_id == '0':
            # check if main catagory exist if not create a main catagory
            data_main_catagory_exist = product_main_catagory.objects.filter(
                pmc_main_catagory_name=input_catagory_main).exists()
            if not data_main_catagory_exist:

                bm = product_main_catagory(pmc_main_catagory_name=input_catagory_main)
                bm.save()
            else:
                pass
        

        main_catagory_fetch_id_data = product_main_catagory.objects.get(pmc_main_catagory_name=input_catagory_main)

        catagory_fetch_id_data = product_catagory.objects.get(acpc_catagory_name=input_catagory_name)

        

        catagory_maping_exist=product_main_catagory_maping.objects.filter(pmcm_main_catagory=main_catagory_fetch_id_data,pmcm_catagory=catagory_fetch_id_data).exists()
        if not catagory_maping_exist :
            cmap = product_main_catagory_maping(pmcm_main_catagory=main_catagory_fetch_id_data,
                                                pmcm_catagory=catagory_fetch_id_data,
    
                                                )
            cmap.save()


    


        uniq_id_print = uuid.uuid1()
        print_uniq_id = uniq_id_print.hex


        for x in range(number_of_product):
            print(x)
            #statforloop
            uniq_id = uuid.uuid1()
            uniq_id = uniq_id.hex
            c = product_master(acpm_product_name=name_of_product,
                               acpm_product_types='single',
                               acpm_product_amount='1',
                               acpm_product_unit='pieces',
                               acpm_product_catagory=catagory_fetch_id_data,
                               acpm_product_main_catagory=main_catagory_fetch_id_data,
                               acpm_waranty_info=request.POST.get("waranty_info").strip(),
                               acpm_serial_number=request.POST.get(
                                   "serial_number").strip(),
                               acpm_brand_details=request.POST.get(
                                   "brand_details"),
                               acpm_vender_details=request.POST.get(
                                   "brought_from"),
                               acpm_po_details=request.POST.get("po_details"),
                               acpm_uniq_id=str(uniq_id),

                               acpm_last_modified_by=current_user
                               )

            c.save()

            # get the inserted id of product master

            product_master_lattest = product_master.objects.get(acpm_uniq_id=str(uniq_id))
            product_master_id = product_master_lattest.acpm_id
            # get the inserted id of product master #

            if x==0:
                # save data to barcode
                barcode_number = request.POST.get("barcode_details")
                if barcode_number != 'not_recognised':
                    print('mainif')
                    barcode_exists = barcode_master.objects.filter(
                        acbs_barcode_details=barcode_number).exists()
                    if barcode_exists:
                        print('mainif_if')
                        barcode_master_data = barcode_master.objects.get(
                            acbs_barcode_details=barcode_number)
                        barcode_master_data.acbs_product_master_id = product_master_lattest
                        barcode_master_data.save()

                    else:
                        print('mainif_else')
                        bc = barcode_master(acbs_barcode_details=barcode_number,
                                            acbs_product_master_id=product_master_lattest,
                                            )
                        bc.save()
                # save data to barcode#





            lattitude = request.POST.get("latitude")
            longitude = request.POST.get("longitude")
            geo_location = str(lattitude) + ',' + str(longitude)

            last_scaned_by = current_user
            data_dict_qr_insert={"acpqm_product_master_id":product_master_lattest,
                                  "acpqm_product_location":geo_location,
                                  "acpqm_last_scaned_from":last_scaned_by,
                                  "acpqm_last_scaned_by":last_scaned_by,
                                  "acpqm_product_movment_details":'vender to admin',
                                  "acpqm_uniq_id":"string_qrcode",
                                  "acpqm_print_uniq_id" : str(print_uniq_id),
                                  "acpqm_qr_image_path":"QRimage_path",
                                  "acpqm_qr_image_name":"qr_image_name",
                                  "acpqm_last_modified_by":last_scaned_by}

            string_qrcode=insert_product_qrmaster(data_dict_qr_insert)


        user = current_user
        qrcode_number = string_qrcode
        amount = number_of_product
        trans_with = current_user
        credit_or_debit = "credit"
        transection_status = product_transection_fun(user,qrcode_number,amount,trans_with,credit_or_debit)
        print(transection_status)
            #endforloop

        messages.success(request, "Single product added successfully ")
        return redirect('lattes_qrcode',print_id=str(print_uniq_id))

@login_required(login_url='/login/')
def add_new_product_if_not_available(request):
    if request.method == "GET":
        context = {"product_cat": 'data',"uniq_product_name":'uniq_product_name'}
        return render(request, 'admin/add_new_product_if_not_available.html', context)
    else:
        current_user = request.user
        product_name = request.POST.get("product_name").strip()
        input_catagory_name = request.POST.get("product_catagory").strip()
        input_main_catagory_name = request.POST.get("product_main_catagory").strip()
        product_unit = request.POST.get("product_unit").strip()
        product_type = request.POST.get("product_type").strip()

        data_catagory_exist = product_catagory.objects.filter(acpc_catagory_name=input_catagory_name).exists()
        if not data_catagory_exist:

            b = product_catagory(acpc_catagory_name=input_catagory_name,
                                 acpc_fra_or_single = product_type,
                                 acpc_last_modified_by=current_user)
            b.save()

        data_catagory = product_catagory.objects.get(acpc_catagory_name = input_catagory_name)


        data_main_catagory_exist = product_main_catagory.objects.filter(pmc_main_catagory_name=input_main_catagory_name).exists()
        if not data_main_catagory_exist:

            bm = product_main_catagory(pmc_main_catagory_name=input_main_catagory_name)
            bm.save()

        data_main_catagory = product_main_catagory.objects.get(pmc_main_catagory_name = input_main_catagory_name)



        product_name_exist = product_master.objects.filter(acpm_product_name = product_name,acpm_product_catagory=data_catagory,acpm_product_main_catagory=data_main_catagory).exists()
        if product_name_exist:
            messages.error(request, "Product name already exists.")
            return redirect('add_new_product_if_not_available')
        else:
            uniq_id = uuid.uuid1()
            uniq_id = uniq_id.hex
            c = product_master(acpm_product_name= product_name,
                               acpm_product_types= product_type,
                               acpm_product_amount='0',
                               acpm_product_unit = product_unit,
                               acpm_product_catagory=data_catagory,
                               acpm_product_main_catagory=data_main_catagory,
                               acpm_uniq_id=str(uniq_id),
                               acpm_last_modified_by=current_user )

            c.save()

            d = product_transaction(pt_user = current_user,
                                   pt_product_name= product_name,
                                   pt_product_unit = product_unit,
                                   pt_product_amount = 0,
                                   pt_product_catagory=data_catagory,
                                   pt_product_main_catagory= data_main_catagory,
                                   pt_last_modified_by=current_user )

            d.save()

            messages.success(request, "Product Created Successfully")
            return redirect('add_new_product_if_not_available')



@login_required(login_url='/login/')
def add_new_product_fractional(request):
    if request.method == "GET":
        data = product_catagory.objects.filter(acpc_is_active=True,acpc_fra_or_single='fractional')
        uniq_product_name = product_transaction.objects.filter(pt_product_catagory__acpc_fra_or_single = 'fractional')
        main_catagory = product_main_catagory.objects.filter(pmc_is_active=True)

        context = {"product_cat": data,"product_cat_main": main_catagory,"uniq_product_name":uniq_product_name}
        return render(request, 'admin/admin_add_fractional_product.html', context)
    else:
        uniq_id = uuid.uuid1()
        uniq_id = uniq_id.hex

        current_user = request.user
        user_id = current_user.id

        input_catagory_name = request.POST.get("input_catagory_name")
        catagory_id = request.POST.get("catagory_id")
        print(catagory_id, 'catagory_id')
        print(type(catagory_id))
        print(input_catagory_name, 'input_catagory_name')
        print(request.POST.get("product_unit"))

        

        input_catagory_main = request.POST.get("input_main_catagory_name")
        main_catagory_id = request.POST.get("main_catagory_id") 
        product_name_post=request.POST.get("product_names")

        input_catagory_name=input_catagory_name.strip()
        input_catagory_main=input_catagory_main.strip()
        product_name_post=product_name_post.strip()


        if catagory_id == '0':
            data_catagory_exist = product_catagory.objects.filter(
                acpc_catagory_name=input_catagory_name).exists()
            if data_catagory_exist:
                data_catagory = product_catagory.objects.get(acpc_catagory_name=input_catagory_name)
                if data_catagory.acpc_fra_or_single != 'fractional':
                    messages.error(request, "this catagory already exist in single product catagory please choose a diffrent name for catagory ")
                    return redirect('add_new_product_fractional')
               # catagory_fetch_id_data.id
            else:  # incase catagory not exsist create  a catagory
                b = product_catagory(acpc_catagory_name = input_catagory_name,
                                     acpc_fra_or_single = 'fractional',
                                     acpc_last_modified_by=current_user)
                b.save()

        if main_catagory_id == '0':
            # check if main catagory exist if not create a main catagory
            data_main_catagory_exist = product_main_catagory.objects.filter(
                pmc_main_catagory_name=input_catagory_main).exists()
            if not data_main_catagory_exist:

                bm = product_main_catagory(pmc_main_catagory_name=input_catagory_main)
                bm.save()
            else:
                pass       

        main_catagory_fetch_id_data = product_main_catagory.objects.get(pmc_main_catagory_name=input_catagory_main)
        catagory_fetch_id_data = product_catagory.objects.get(acpc_catagory_name=input_catagory_name)

        catagory_maping_exist=product_main_catagory_maping.objects.filter(pmcm_main_catagory=main_catagory_fetch_id_data,pmcm_catagory=catagory_fetch_id_data).exists()
        if not catagory_maping_exist :
            cmap = product_main_catagory_maping(pmcm_main_catagory=main_catagory_fetch_id_data,
                                                pmcm_catagory=catagory_fetch_id_data,
    
                                                )
            cmap.save()

        c = product_master(acpm_product_name=product_name_post,
                           acpm_product_types='fractional',
                           acpm_product_catagory=catagory_fetch_id_data,
                           acpm_product_main_catagory=main_catagory_fetch_id_data,
                           acpm_waranty_info=request.POST.get("waranty_info").strip(),
                           acpm_serial_number=request.POST.get(
                               "serial_number").strip(),
                           acpm_brand_details=request.POST.get(
                               "brand_details").strip(),
                           acpm_vender_details=request.POST.get(
                               "brought_from").strip(),
                           acpm_po_details=request.POST.get("po_details").strip(),
                           acpm_product_unit=request.POST.get("product_unit").strip(),
                           acpm_product_amount=request.POST.get(
                               "product_quantity"),

                           acpm_uniq_id=str(uniq_id),

                           acpm_last_modified_by=current_user
                           )

        c.save()

        # get the inserted id of product master

        product_master_lattest = product_master.objects.get(
            acpm_uniq_id=str(uniq_id))

        # get the inserted id of product master #

        # save data to barcode
        barcode_number = request.POST.get("barcode_details")

        barcode_get_post = request.POST.get("barcode_type")
        if barcode_number != 'not_recognised':
            barcode_exists = barcode_master.objects.filter(
                acbs_barcode_details=barcode_number).exists()
            if barcode_exists:
                print('mainif_if')
                barcode_master_data = barcode_master.objects.get(
                    acbs_barcode_details=barcode_number)
                barcode_master_data.acbs_product_master_id = product_master_lattest
                barcode_master_data.save()

            else:
                bc = barcode_master(acbs_barcode_details=barcode_number,
                                    acbs_product_master_id=product_master_lattest,
                                    )
                bc.save()
        # save data to barcode#

        lattitude = request.POST.get("latitude")
        longitude = request.POST.get("longitude")
        geo_location = str(lattitude) + ',' + str(longitude)

        last_scaned_by = current_user

        data_dict_qr_insert={"acpqm_product_master_id":product_master_lattest,
                              "acpqm_product_location":geo_location,
                              "acpqm_last_scaned_from":last_scaned_by,
                              "acpqm_last_scaned_by":last_scaned_by,
                              "acpqm_product_movment_details":'vender to admin',
                              "acpqm_uniq_id":"string_qrcode",
                              "acpqm_print_uniq_id" : str(uniq_id),
                              "acpqm_qr_image_path":"QRimage_path",
                              "acpqm_qr_image_name":"qr_image_name",
                              "acpqm_last_modified_by":last_scaned_by}

        string_qrcode=insert_product_qrmaster(data_dict_qr_insert)

        user = current_user
        qrcode_number = string_qrcode
        amount = str(product_master_lattest.acpm_product_amount)
        trans_with = current_user
        credit_or_debit = "credit"
        transection_status = product_transection_fun(user,qrcode_number,amount,trans_with,credit_or_debit)
        print(transection_status)

        messages.success(
            request, "fractional product added successfully ")
        return redirect('lattes_qrcode',print_id=str(uniq_id))


@csrf_exempt
def chckproduct_presence(request):

    # try:
    # 'barcodeData': '123456', 'barcodeType': 'CODE128', 'image_rec_base64':

    if request.method == "GET":  # this get method will never run this is for ajax
        context = {"data": "data"}
        return render(request, 'admin/admin_add_fractional_product.html', context)
    else:
        req_data = request.POST.get("data")

        req_data = json.loads(req_data)
        imagedata = req_data['image_data']
        #print(imagedata, '===================================')

        retrun_result = base64_to_barcodenumber(imagedata)
        retrun_result['barcodeData']
        #print(retrun_result, 'return result')

        if retrun_result['barcodeData'] != 'na' and retrun_result['barcodeType'] == 'QRCODE':
            print("mainif")
            barcode_data = retrun_result['barcodeData']
            barcode_exists = product_qr_master.objects.filter(
                acpqm_uniq_id=barcode_data).exists()
            if barcode_exists:  # when barcode data exist
                print("mainif_if")
                product_qr_master_row = product_qr_master.objects.get(
                    acpqm_uniq_id=barcode_data)

                product_master_row = product_qr_master_row.acpqm_product_master_id

                retrun_result['data_table'] = model_to_dict(product_master_row, fields=[
                    field.name for field in product_master_row._meta.fields])

                retrun_result['data_table_qr'] = model_to_dict(product_qr_master_row, fields=[
                        field.name for field in product_qr_master_row._meta.fields])

                retrun_result['catagory_name'] = product_master_row.acpm_product_catagory.acpc_catagory_name
                retrun_result['main_catagory_name'] = product_master_row.acpm_product_main_catagory.pmc_main_catagory_name
            if not barcode_exists:  # when qrcode and data not exist in qrcode table
                print("mainif_else")
                barcode_data = retrun_result['barcodeData']
                barcode_exists = barcode_master.objects.filter(
                    acbs_barcode_details=barcode_data).exists()
                if barcode_exists:  # when barcode data exist
                    print("mainif_else_if")
                    barcode_master_row = barcode_master.objects.get(
                        acbs_barcode_details=barcode_data)

                    product_master_row = barcode_master_row.acbs_product_master_id

                    retrun_result['data_table'] = model_to_dict(product_master_row, fields=[
                        field.name for field in product_master_row._meta.fields])



                    retrun_result['catagory_name'] = product_master_row.acpm_product_catagory.acpc_catagory_name
                    retrun_result['main_catagory_name'] = product_master_row.acpm_product_main_catagory.pmc_main_catagory_name
                else:
                    print("mainif_else_else")
                    pass

        elif retrun_result['barcodeData'] != 'na' and retrun_result['barcodeType'] != 'QRCODE':
            print("main_elif")
            barcode_data = retrun_result['barcodeData']

            barcode_exists = barcode_master.objects.filter(
                acbs_barcode_details=barcode_data).exists()
            if barcode_exists:
                print("main_elif_if")

                barcode_master_row = barcode_master.objects.get(
                    acbs_barcode_details=barcode_data)

                product_master_row = barcode_master_row.acbs_product_master_id

                retrun_result['data_table'] = model_to_dict(product_master_row, fields=[
                                                            field.name for field in product_master_row._meta.fields])

                retrun_result['catagory_name'] = product_master_row.acpm_product_catagory.acpc_catagory_name
                retrun_result['main_catagory_name'] = product_master_row.acpm_product_main_catagory.pmc_main_catagory_name
            else:
                print("main_elif_else")
                print(
                    "pass---------------------------------------------------------------------------")
                pass
        else:
            print("main_else")
            # image not recognised
            pass

        print(retrun_result)

        return JsonResponse(retrun_result)

    # except Exception as e:
    #     return JsonResponse({'Message': 'Please check opstype.',
    #                         'Status': 0,
    #                          'error': str(e)
    #                          })

@login_required(login_url='/login/')
def inventory_view(request):
    if request.method == 'GET':
        #query_results = site_master.objects.all()
        curent_page = 1
        pagedata_starting = 0
        pagedata_ending = pagedata_starting + 20

        prev_pagenumber = 1
        next_page_number = 2
        totaldata = product_qr_master.objects.all().order_by('acpqm_created_at').count()

        query_results = product_qr_master.objects.all().order_by('acpqm_created_at')[
            :pagedata_ending]
        showingdata = query_results.count()

        product_name_list = product_master.objects.order_by().values('acpm_product_name').distinct()
        product_cat_list = product_catagory.objects.order_by().values('acpc_catagory_name').distinct()
        product_main_cat_list = product_main_catagory.objects.order_by().values('pmc_main_catagory_name').distinct()
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
                   "product_main_cat_list":product_main_cat_list,
                   "product_qr_list":product_qr_list,
                   "product_print_list":product_print_list
                   }
        return render(request, 'admin/inventory_view.html', context)

@login_required(login_url='/login/')
def inventory_view_pagination(request, page_number):
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

        totaldata = product_qr_master.objects.all().order_by('acpqm_created_at').count()

        query_results = product_qr_master.objects.all().order_by('acpqm_created_at')[pagedata_starting:pagedata_ending]
        showingdata = query_results.count()

        product_name_list = product_master.objects.order_by().values('acpm_product_name').distinct()
        product_cat_list = product_catagory.objects.order_by().values('acpc_catagory_name').distinct()
        product_main_cat_list = product_main_catagory.objects.order_by().values('pmc_main_catagory_name').distinct()
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
                   "product_main_cat_list":product_main_cat_list,
                   "product_qr_list":product_qr_list,
                   "product_print_list":product_print_list
                   }
        return render(request, 'admin/inventory_view.html', context)
    else:

        product_name_search = request.POST.get("product_name_search")
        Product_catagory_search = request.POST.get("Product_catagory_search")
        Product_main_catagory_search = request.POST.get("Product_main_catagory_search")
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
        print(from_date,'from_date')
        print(to_date,'to_date')


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
                                                         acpqm_print_uniq_id__contains=Product_print_code_availale).order_by('acpqm_created_at').count()

            #query_results = product_qr_master.objects.all().order_by('acpqm_created_at')[pagedata_starting:pagedata_ending]


            query_results = product_qr_master.objects.filter(acpqm_product_master_id__acpm_product_name__contains=product_name_search,
                                                         acpqm_product_master_id__acpm_product_catagory__acpc_catagory_name__contains=Product_catagory_search,
                                                         acpqm_uniq_id__contains=Product_qr_code_availale,
                                                         acpqm_print_uniq_id__contains=Product_print_code_availale).order_by('acpqm_created_at')[pagedata_starting:pagedata_ending]
        else:


            totaldata = product_qr_master.objects.filter(acpqm_product_master_id__acpm_product_name__contains=product_name_search,
                                                         acpqm_product_master_id__acpm_product_catagory__acpc_catagory_name__contains=Product_catagory_search,
                                                         acpqm_uniq_id__contains=Product_qr_code_availale,
                                                         acpqm_print_uniq_id__contains=Product_print_code_availale,
                                                         acpqm_created_at__range=[from_date, to_date]).order_by('acpqm_created_at').count()

            #query_results = product_qr_master.objects.all().order_by('acpqm_created_at')[pagedata_starting:pagedata_ending]


            query_results = product_qr_master.objects.filter(acpqm_product_master_id__acpm_product_name__contains=product_name_search,
                                                         acpqm_product_master_id__acpm_product_catagory__acpc_catagory_name__contains=Product_catagory_search,
                                                         acpqm_uniq_id__contains=Product_qr_code_availale,
                                                         acpqm_print_uniq_id__contains=Product_print_code_availale,
                                                         acpqm_created_at__range=[from_date, to_date]).order_by('acpqm_created_at')[pagedata_starting:pagedata_ending]

        showingdata = query_results.count()

        product_name_list = product_master.objects.order_by().values('acpm_product_name').distinct()
        product_cat_list = product_catagory.objects.order_by().values('acpc_catagory_name').distinct()
        product_main_cat_list = product_main_catagory.objects.order_by().values('pmc_main_catagory_name').distinct()        
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
                   "product_main_cat_list":product_main_cat_list,
                   "product_qr_list":product_qr_list,
                   "product_print_list":product_print_list,

                   "product_name_search":product_name_search,
                   "Product_catagory_search":Product_catagory_search,
                   "Product_main_catagory_search":Product_main_catagory_search,
                   "Product_qr_code_availale":Product_qr_code_availale,
                   "Product_print_code_availale":Product_print_code_availale,
                   "from_date":from_date,
                   "to_date":to_date,

                   }
        return render(request, 'admin/inventory_view.html', context)


@login_required(login_url='/login/')
def product_view(request):
    if request.method == 'GET':
        #query_results = site_master.objects.all()
        curent_page = 1
        pagedata_starting = 0
        pagedata_ending = pagedata_starting + 20

        prev_pagenumber = 1
        next_page_number = 2
        totaldata = product_master.objects.all().order_by('acpm_created_at').count()

        query_results = product_master.objects.all().order_by('acpm_created_at')[
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
        return render(request, 'admin/product_view.html', context)

@login_required(login_url='/login/')
def product_view_pagination(request, page_number):
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

        totaldata = product_master.objects.all().order_by('acpm_created_at').count()

        query_results = product_master.objects.all().order_by(
            'acpm_created_at')[pagedata_starting:pagedata_ending]
        showingdata = query_results.count()

        context = {"query_results": query_results,
                   'totaldata': totaldata,
                   'curent_page': curent_page,
                   'pagedata_starting': pagedata_starting,
                   'prev_pagenumber': prev_pagenumber,
                   'next_page_number': next_page_number,
                   'showingdata': showingdata

                   }
        return render(request, 'admin/product_view.html', context)



















@login_required(login_url='/login/')
def product_name_view(request):
    if request.method == 'GET':
        #query_results = site_master.objects.all()
        curent_page = 1
        pagedata_starting = 0
        pagedata_ending = pagedata_starting + 20

        prev_pagenumber = 1
        next_page_number = 2

        mainquery= product_master.objects.raw('SELECT * FROM `admin_account_product_master` GROUP BY `acpm_product_name`,`acpm_product_catagory_id`,`acpm_product_main_catagory_id`')
        totaldata = len(list(mainquery)) #product_master.objects.raw('').order_by('acpm_created_at').count()

        query_results = mainquery
        showingdata = len(list(query_results))

        context = {"query_results": query_results,
                   'totaldata': totaldata,
                   'curent_page': curent_page,
                   'pagedata_starting': pagedata_starting,
                   'prev_pagenumber': prev_pagenumber,
                   'next_page_number': next_page_number,
                   'showingdata': showingdata

                   }
        return render(request, 'admin/product_view.html', context)

@login_required(login_url='/login/')
def product_name_view_pagination(request, page_number):
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

        mainquery= product_master.objects.raw('SELECT * FROM `admin_account_product_master` GROUP BY `acpm_product_name`,`acpm_product_catagory_id`,`acpm_product_main_catagory_id`')
        totaldata = len(list(mainquery))# product_master.objects.all().order_by('acpm_created_at').count()

        query_results = mainquery[pagedata_starting:pagedata_ending]
        showingdata = len(list(query_results))

        context = {"query_results": query_results,
                   'totaldata': totaldata,
                   'curent_page': curent_page,
                   'pagedata_starting': pagedata_starting,
                   'prev_pagenumber': prev_pagenumber,
                   'next_page_number': next_page_number,
                   'showingdata': showingdata

                   }
        return render(request, 'admin/product_view.html', context)



@login_required(login_url='/login/')
def product_name_by_id(request,prod_name_id):
    if request.method == 'GET':
        
        # current_user = request.user

        product_name_exists = product_master.objects.filter(acpm_id=prod_name_id).exists()

        if product_name_exists :
            
            product_name_row = product_master.objects.filter(pk=prod_name_id)

            context = {"query_results": product_name_row,
            }
            return render(request, 'admin/product_name_view_by_id.html', context)
        else:
            messages.error(request, "No product found with this id. ")
            return redirect('product_name_view')
    else:
        product_name = request.POST.get("product_name")
        product_desc = request.POST.get("product_desc")

        product_name_exists = product_master.objects.filter(acpm_id=prod_name_id).exists()
        
        if product_name_exists :
            if product_name is None:
                messages.error(request, "product name should not be empty. ")                
                return redirect('product_name_by_id',sub_cat_id)
            
            if product_desc is None:
                messages.error(request, "product  description should not be empty. ")
                
                return redirect('product_name_by_id',sub_cat_id)


            product_name_data = product_master.objects.get(acpm_id=prod_name_id)

            product_master.objects.filter(acpm_product_catagory=product_name_data.acpm_product_catagory,acpm_product_main_catagory=product_name_data.acpm_product_main_catagory,).update(acpm_product_name=str(product_name),acpm_product_description=str(product_desc))

            messages.success(request, "updated successfully ")
            return redirect('product_name_by_id',prod_name_id)
        else:
            messages.error(request, "No product name found with this id. ")
            return redirect('product_name_view')

@login_required(login_url='/login/')
def sub_catagory_name_view(request):
    if request.method == 'GET':
        #query_results = site_master.objects.all()
        curent_page = 1
        pagedata_starting = 0
        pagedata_ending = pagedata_starting + 20

        prev_pagenumber = 1
        next_page_number = 2
        totaldata = product_catagory.objects.all().order_by('acpc_created_at').count()

        query_results = product_catagory.objects.all().order_by('acpc_created_at')
        showingdata = query_results.count()

        context = {"query_results": query_results,
                   'totaldata': totaldata,
                   'curent_page': curent_page,
                   'pagedata_starting': pagedata_starting,
                   'prev_pagenumber': prev_pagenumber,
                   'next_page_number': next_page_number,
                   'showingdata': showingdata

                   }
        return render(request, 'admin/sub_catagory_view.html', context)

@login_required(login_url='/login/')
def sub_catagory_name_view_pagination(request, page_number):
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

        totaldata = product_catagory.objects.all().order_by('acpc_created_at').count()

        query_results = product_catagory.objects.all().order_by(
            'acpc_created_at')[pagedata_starting:pagedata_ending]
        showingdata = query_results.count()

        context = {"query_results": query_results,
                   'totaldata': totaldata,
                   'curent_page': curent_page,
                   'pagedata_starting': pagedata_starting,
                   'prev_pagenumber': prev_pagenumber,
                   'next_page_number': next_page_number,
                   'showingdata': showingdata

                   }
        return render(request, 'admin/sub_catagory_view.html', context)

@login_required(login_url='/login/')
def sub_catagory_name_by_id(request,sub_cat_id):
    if request.method == 'GET':
        
        # current_user = request.user

        sub_cat_exists = product_catagory.objects.filter(acpc_id=sub_cat_id).exists()

        if sub_cat_exists :
            
            sub_cat_row = product_catagory.objects.filter(pk=sub_cat_id)

            context = {"query_results": sub_cat_row,
            }
            return render(request, 'admin/sub_cat_view_by_id.html', context)
        else:
            messages.error(request, "No sub catagory found with this id. ")
            return redirect('sub_catagory_name_view')
    else:
        sub_catagory_name = request.POST.get("sub_catagory_name")
        sub_cat_desc = request.POST.get("sub_cat_desc")

        sub_cat_exists = product_catagory.objects.filter(acpc_id=sub_cat_id).exists()
        
        if sub_cat_exists :
            if sub_catagory_name is None:
                messages.error(request, "sub catagory name should not be empty. ")
                
                return redirect('sub_catagory_name_by_id',sub_cat_id)
            
            if sub_cat_desc is None:
                messages.error(request, "sub catagory description should not be empty. ")
                
                return redirect('sub_catagory_name_by_id',sub_cat_id)


            sub_cat_obj= product_catagory.objects.get(acpc_id=sub_cat_id)



            sub_cat_obj.acpc_catagory_name = str(sub_catagory_name)
            sub_cat_obj.acpc_catagory_description = str(sub_cat_desc)
            
            sub_cat_obj.save()
            messages.success(request, "updated successfully ")
            return redirect('sub_catagory_name_by_id',sub_cat_id)
        else:
            messages.error(request, "No sub catagory found with this id. ")
            return redirect('sub_catagory_name_view')


@login_required(login_url='/login/')
def main_catagory_name_view(request):
    if request.method == 'GET':
        #query_results = site_master.objects.all()
        curent_page = 1
        pagedata_starting = 0
        pagedata_ending = pagedata_starting + 20

        prev_pagenumber = 1
        next_page_number = 2
        totaldata = product_main_catagory.objects.all().order_by('pmc_created_at').count()

        query_results = product_main_catagory.objects.all().order_by('pmc_created_at')
        showingdata = query_results.count()

        context = {"query_results": query_results,
                   'totaldata': totaldata,
                   'curent_page': curent_page,
                   'pagedata_starting': pagedata_starting,
                   'prev_pagenumber': prev_pagenumber,
                   'next_page_number': next_page_number,
                   'showingdata': showingdata

                   }
        return render(request, 'admin/main_catagory_view.html', context)

@login_required(login_url='/login/')
def main_catagory_name_view_pagination(request, page_number):
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

        totaldata = product_main_catagory.objects.all().order_by('pmc_created_at').count()

        query_results = product_main_catagory.objects.all().order_by(
            'pmc_created_at')[pagedata_starting:pagedata_ending]
        showingdata = query_results.count()

        context = {"query_results": query_results,
                   'totaldata': totaldata,
                   'curent_page': curent_page,
                   'pagedata_starting': pagedata_starting,
                   'prev_pagenumber': prev_pagenumber,
                   'next_page_number': next_page_number,
                   'showingdata': showingdata

                   }
        return render(request, 'admin/main_catagory_view.html', context)


@login_required(login_url='/login/')
def main_catagory_name_by_id(request,main_cat_id):
    if request.method == 'GET':
        
        # current_user = request.user

        main_cat_exists = product_main_catagory.objects.filter(pmc_id=main_cat_id).exists()

        if main_cat_exists :
            
            product_main_row = product_main_catagory.objects.filter(pk=main_cat_id)

            context = {"query_results": product_main_row,
            }
            return render(request, 'admin/main_cat_view_by_id.html', context)
        else:
            messages.error(request, "No main catagory found with this id. ")
            return redirect('main_catagory_name_view')
    else:

        main_catagory_name = request.POST.get("main_catagory_name")
        main_cat_desc = request.POST.get("main_cat_desc")

        main_cat_exists = product_main_catagory.objects.filter(pmc_id=main_cat_id).exists()
        
        if main_cat_exists :
            if main_catagory_name is None:
                messages.error(request, "Main catagory name should not be empty. ")
                
                return redirect('main_catagory_name_by_id',main_cat_id)
            
            if main_cat_desc is None:
                messages.error(request, "main catagory description should not be empty. ")
                
                return redirect('main_catagory_name_by_id',main_cat_id)


            main_cat_obj= product_main_catagory.objects.get(pmc_id=main_cat_id)



            main_cat_obj.pmc_main_catagory_name = str(main_catagory_name)
            main_cat_obj.pmc_main_catagory_description = str(main_cat_desc)
            
            main_cat_obj.save()
            messages.success(request, "updated successfully ")
            return redirect('main_catagory_name_by_id',main_cat_id)



@login_required(login_url='/login/')
def view_product_by_id(request, product_id):
    if request.method == 'GET':
        product_master_row = product_master.objects.filter(pk=product_id)
        print(product_id)
        print(product_master_row)

        # query_results = product_master.objects.all().order_by(
        #     'created_at')[pagedata_starting:pagedata_ending]
        # showingdata = query_results.count()

        context = {"query_results": product_master_row,

                   }
        return render(request, 'admin/product_view_by_id.html', context)

@login_required(login_url='/login/')
def purchase_order_view(request):
    if request.method == 'GET':
        #query_results = site_master.objects.all()
        curent_page = 1
        pagedata_starting = 0
        pagedata_ending = pagedata_starting + 20

        prev_pagenumber = 1
        next_page_number = 2
        totaldata = purchase_order.objects.filter(acpo_is_active=True).order_by('acpo_created_at').count()

        query_results = purchase_order.objects.filter(acpo_is_active=True).order_by('-acpo_created_at')[
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
        return render(request, 'purchase_order/purchase_order_index.html', context)

@login_required(login_url='/login/')
def purchase_order_view_pagination(request, page_number):
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

        totaldata = purchase_order.objects.filter(acpo_is_active=True).order_by('acpo_created_at').count()

        query_results = purchase_order.objects.filter(acpo_is_active=True).order_by('acpo_created_at')[pagedata_starting:pagedata_ending]
        showingdata = query_results.count()

        context = {"query_results": query_results,
                   'totaldata': totaldata,
                   'curent_page': curent_page,
                   'pagedata_starting': pagedata_starting,
                   'prev_pagenumber': prev_pagenumber,
                   'next_page_number': next_page_number,
                   'showingdata': showingdata

                   }
        return render(request, 'purchase_order/purchase_order_index.html', context)

@login_required(login_url='/login/')
def create_purchase_order(request):
    if request.method == 'GET':
        current_user = request.user
        d = purchase_order(acpo_last_modified_by=current_user,)
        d.save()
        messages.success(request, "new purchase order created successfully")
        return redirect('purchase_order_view')

    else:
        po_id = request.POST.get("po_id")
        print(po_id,"--------------------------------poid---------------------------")
        purchase_order_get = purchase_order.objects.get(pk=po_id)
        purchase_order_get.acpo_order_submited = True
        purchase_order_get.save()

        messages.success(request, "purchase order submited successfully")
        return redirect('po_details_view', po_id=po_id)

@login_required(login_url='/login/')
def po_details_view(request, po_id):

    if request.method == 'GET':
        purchase_order_row_exists = purchase_order.objects.filter(pk=po_id).exists()
        purchase_order_row = {}
        purchase_order_products = {}
        products_count = 0
        if purchase_order_row_exists:
            purchase_order_row = purchase_order.objects.filter(pk=po_id)
            purchase_order_get = purchase_order.objects.get(pk=po_id)
            purchase_order_product_exists = purchase_order_product.objects.filter(
                acpop_purchase_order=purchase_order_get, acpop_is_active=True).exists()
            if purchase_order_product_exists:
                purchase_order_products = purchase_order_product.objects.filter(
                    acpop_purchase_order=purchase_order_get, acpop_is_active=True)
                products_count = purchase_order_products.count()

        context = {"purchase_order_row": purchase_order_row,
                   "purchase_order_products": purchase_order_products,
                   "products_count": products_count
                   }
        return render(request, 'purchase_order/po_details_view_id.html', context)

    else:
        pass

@login_required(login_url='/login/')
def remove_product_from_po(request, product_id):
    if request.method == 'POST':

        po_id = request.POST.get("po_id")

        purchase_order_data = purchase_order.objects.get(
            pk=po_id)

        if purchase_order_data.acpo_order_submited == True:
            messages.error(
                request, "This po is already submited. you cant remove.")
            return redirect('po_details_view', po_id=po_id)

        current_user = request.user

        purchase_order_by_id = purchase_order.objects.get(
            pk=po_id, acpo_is_active=True)

        selected_product = purchase_order_product.objects.get(
            pk=product_id, acpop_is_active=True)

        po_product_exist = purchase_order_product.objects.filter(
            pk=product_id, acpop_purchase_order=purchase_order_by_id).exists()
        if po_product_exist:
            po_product = purchase_order_product.objects.get(
                pk=product_id, acpop_purchase_order=purchase_order_by_id)

            po_product.acpop_is_active = False
            po_product.save()

            messages.success(
                request, "successfully removed product from this po.")
            return redirect('po_details_view', po_id=po_id)

        else:

            messages.error(request, "For this id, product is not present.")
            return redirect('po_details_view', po_id=po_id)

@login_required(login_url='/login/')
def add_product_to_po(request, po_id):
    if request.method == 'POST':
        current_user = request.user
        product_name = request.POST.get("product_name")
        print('product_name', product_name)
        product_catagory = request.POST.get("product_catagory")
        product_unit = request.POST.get("product_unit")
        product_amount = request.POST.get("product_amount")
        # check if alredy submited

        purchase_order_data = purchase_order.objects.get(
            pk=po_id, acpo_is_active=True)
        if purchase_order_data.acpo_order_submited == True:
            messages.error(
                request, "This po is already submited please create a new one")
            return redirect('po_details_view', po_id=po_id)

        purchase_order_product_data = purchase_order_product.objects.filter(
            acpop_product_name=product_name, acpop_product_catagory=product_catagory, acpop_purchase_order=purchase_order_data).exists()

        if purchase_order_product_data:

            purchase_order_product_row = purchase_order_product.objects.get(
                acpop_product_name=product_name, acpop_product_catagory=product_catagory, acpop_purchase_order=purchase_order_data)

            if purchase_order_product_row.acpop_is_active == False:
                purchase_order_product_row.acpop_is_active = True
                purchase_order_product_row.acpop_product_amount = str(
                    product_amount)
                purchase_order_product_row.acpop_product_unit = str(
                    product_unit)

                purchase_order_product_row.acpop_product_name = str(
                    product_name)
                purchase_order_product_row.acpop_product_catagory = str(
                    product_catagory)
                purchase_order_product_row.save()

                messages.success(
                    request, "product added successfully")
                return redirect('po_details_view', po_id=po_id)
            else:
                purchase_order_product_row.acpop_product_amount = str(
                    product_amount)
                purchase_order_product_row.acpop_product_unit = str(
                    product_unit)
                purchase_order_product_row.acpop_product_name = str(
                    product_name)
                purchase_order_product_row.acpop_product_catagory = str(
                    product_catagory)
                purchase_order_product_row.save()

                messages.success(
                    request, "product readded successfully")
                return redirect('po_details_view', po_id=po_id)

        else:
            c = purchase_order_product(acpop_purchase_order=purchase_order_data,
                                       acpop_product_name=product_name,
                                       acpop_product_catagory=product_catagory,
                                       acpop_product_unit=str(product_unit),
                                       acpop_product_amount=str(
                                           product_amount),
                                       acpop_last_modified_by=current_user,
                                       )
            c.save()
            messages.success(request, "new product added successfully")
            return redirect('po_details_view', po_id=po_id)



@login_required(login_url='/login/')
def product_transection_view(request,user_id = "na"):
    if request.method == 'GET':
        current_user = request.user
        if not(user_id == "na"):
            user_id=int(user_id)
            user_exists = User.objects.filter(id=user_id).exists()

            if user_exists:
                current_user = User.objects.get(id=user_id)
            else:
                return render(request, '404.html')

        #query_results = site_master.objects.all()
        curent_page = 1
        pagedata_starting = 0
        pagedata_ending = pagedata_starting + 20

        prev_pagenumber = 1
        next_page_number = 2

        totaldata = product_transaction.objects.filter(pt_user=current_user).order_by('pt_created_at').count()

        query_results = product_transaction.objects.filter(pt_user=current_user).order_by('pt_created_at')[:pagedata_ending]
        showingdata = query_results.count()

        current_user = request.user
        groupid = current_user.groups.values_list('id', flat=True).first()
        groupname = current_user.groups.values_list('name', flat=True).first()
        # 'groupid':groupid,
        # 'groupname':groupname

        context = {"query_results": query_results,
                   'totaldata': totaldata,
                   'curent_page': curent_page,
                   'pagedata_starting': pagedata_starting,
                   'prev_pagenumber': prev_pagenumber,
                   'next_page_number': next_page_number,
                   'showingdata': showingdata,
                   'groupid':groupid,
                   'groupname':groupname,
                   'user_id':str(user_id)

                   }
        return render(request, 'admin/product_transection.html', context)

@login_required(login_url='/login/')
def product_transection_pagination_view(request, page_number,user_id = "na"):
    if request.method == 'GET':
        current_user = request.user
        if not(user_id == "na"):
            user_id=int(user_id)
            user_exists = User.objects.filter(id=user_id).exists()

            if user_exists:
                current_user = User.objects.get(id=user_id)
            else:
                return render(request, '404.html', context)

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

        totaldata = product_transaction.objects.filter(pt_user=current_user).order_by('pt_created_at').count()

        query_results = product_transaction.objects.filter(pt_user=current_user).order_by('pt_created_at')[pagedata_starting:pagedata_ending]
        showingdata = query_results.count()


        current_user = request.user
        groupid = current_user.groups.values_list('id', flat=True).first()
        groupname = current_user.groups.values_list('name', flat=True).first()
        # 'groupid':groupid,
        # 'groupname':groupname

        context = {"query_results": query_results,
                   'totaldata': totaldata,
                   'curent_page': curent_page,
                   'pagedata_starting': pagedata_starting,
                   'prev_pagenumber': prev_pagenumber,
                   'next_page_number': next_page_number,
                   'showingdata': showingdata,
                   'groupid':groupid,
                   'groupname':groupname,
                   'user_id':str(user_id)

                   }
        return render(request, 'admin/product_transection.html', context)

@login_required(login_url='/login/')
def product_trans_by_id(request,pt_id,user_id="na"):
    if request.method == 'GET':
        current_user = request.user
        if not(user_id == "na"):
            user_id=int(user_id)
            user_exists = User.objects.filter(id=user_id).exists()

            if user_exists:
                current_user = User.objects.get(id=user_id)
            else:
                return render(request, '404.html')

        pt_obj = product_transaction.objects.get(pk=pt_id)
        #query_results = site_master.objects.all()
        curent_page = 1
        pagedata_starting = 0
        pagedata_ending = pagedata_starting + 20

        prev_pagenumber = 1
        next_page_number = 2

        totaldata = all_product_transaction.objects.filter(apt_user = current_user,apt_product_name=pt_obj).order_by('apt_created_at').count()

        query_results = all_product_transaction.objects.filter(apt_user = current_user,apt_product_name=pt_obj).order_by('apt_created_at')[:pagedata_ending]
        showingdata = query_results.count()

        current_user = request.user

        groupid = current_user.groups.values_list('id', flat=True).first()
        groupname = current_user.groups.values_list('name', flat=True).first()
        # 'groupid':groupid,
        # 'groupname':groupname



        context = {"query_results": query_results,
                   'totaldata': totaldata,
                   'curent_page': curent_page,
                   'pagedata_starting': pagedata_starting,
                   'prev_pagenumber': prev_pagenumber,
                   'next_page_number': next_page_number,
                   'showingdata': showingdata,
                   'pt_id':pt_id,
                   'groupid':groupid,
                   'groupname':groupname,
                   'user_id':str(user_id)
                   }
        return render(request, 'admin/product_trans_by_id.html', context)

@login_required(login_url='/login/')
def product_trans_by_id_pagination(request,pt_id,page_number,user_id="na"):
    if request.method == 'GET':
        current_user = request.user
        if not(user_id == "na"):
            user_id=int(user_id)
            user_exists = User.objects.filter(id=user_id).exists()

            if user_exists:
                current_user = User.objects.get(id=user_id)
            else:
                return render(request, '404.html', context)
        pt_obj = product_transaction.objects.get(pk=pt_id)

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

        totaldata = all_product_transaction.objects.filter(apt_user=current_user,apt_product_name=pt_obj).order_by('apt_created_at').count()

        query_results = all_product_transaction.objects.filter(apt_user=current_user,apt_product_name=pt_obj).order_by('apt_created_at')[pagedata_starting:pagedata_ending]
        showingdata = query_results.count()


        current_user = request.user

        groupid = current_user.groups.values_list('id', flat=True).first()
        groupname = current_user.groups.values_list('name', flat=True).first()
        # 'groupid':groupid,
        # 'groupname':groupname

        context = {"query_results": query_results,
                   'totaldata': totaldata,
                   'curent_page': curent_page,
                   'pagedata_starting': pagedata_starting,
                   'prev_pagenumber': prev_pagenumber,
                   'next_page_number': next_page_number,
                   'showingdata': showingdata,
                   'pt_id':pt_id,
                   'groupid':groupid,
                   'groupname':groupname,
                   'user_id':str(user_id)

                   }
        return render(request, 'admin/product_trans_by_id.html', context)

@login_required(login_url='/login/')
def all_product_transaction_view(request,user_id = "na"):
    if request.method == 'GET':
        current_user = request.user

        if not(user_id == "na"):
            user_id=int(user_id)
            user_exists = User.objects.filter(id=user_id).exists()

            if user_exists:
                current_user = User.objects.get(id=user_id)
            else:
                return render(request, '404.html', context)
        #query_results = site_master.objects.all()
        curent_page = 1
        pagedata_starting = 0
        pagedata_ending = pagedata_starting + 20

        prev_pagenumber = 1
        next_page_number = 2

        totaldata = all_product_transaction.objects.filter(apt_user = current_user).order_by('apt_created_at').count()

        query_results = all_product_transaction.objects.filter(apt_user = current_user).order_by('apt_created_at')[:pagedata_ending]
        showingdata = query_results.count()


        current_user = request.user

        groupid = current_user.groups.values_list('id', flat=True).first()
        groupname = current_user.groups.values_list('name', flat=True).first()

        context = {"query_results": query_results,
                   'totaldata': totaldata,
                   'curent_page': curent_page,
                   'pagedata_starting': pagedata_starting,
                   'prev_pagenumber': prev_pagenumber,
                   'next_page_number': next_page_number,
                   'showingdata': showingdata,
                   'groupid':groupid,
                   'groupname':groupname,
                   'user_id':str(user_id)

                   }
        return render(request, 'admin/all_product_transaction.html', context)

@login_required(login_url='/login/')
def all_product_transaction_pagination_view(request,page_number,user_id="na"):
    if request.method == 'GET':
        current_user = request.user

        if not(user_id == "na"):
            user_id=int(user_id)
            user_exists = User.objects.filter(id=user_id).exists()

            if user_exists:
                current_user = User.objects.get(id=user_id)
            else:
                return render(request, '404.html', context)

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

        totaldata = all_product_transaction.objects.filter(apt_user=current_user).order_by('apt_created_at').count()

        query_results = all_product_transaction.objects.filter(apt_user=current_user).order_by('apt_created_at')[pagedata_starting:pagedata_ending]
        showingdata = query_results.count()


        current_user = request.user

        groupid = current_user.groups.values_list('id', flat=True).first()
        groupname = current_user.groups.values_list('name', flat=True).first()




        context = {"query_results": query_results,
                   'totaldata': totaldata,
                   'curent_page': curent_page,
                   'pagedata_starting': pagedata_starting,
                   'prev_pagenumber': prev_pagenumber,
                   'next_page_number': next_page_number,
                   'showingdata': showingdata,
                   'groupid':groupid,
                   'groupname':groupname,
                   'user_id':str(user_id)

                   }
        return render(request, 'admin/all_product_transaction.html', context)

@login_required(login_url='/login/')
def fra_product_from_invent(request):
    if request.method == "GET":
        data = product_catagory.objects.filter(acpc_is_active=True,acpc_fra_or_single='fractional')
        uniq_product_name = product_transaction.objects.filter(pt_product_catagory__acpc_fra_or_single = 'fractional')

        context = {"product_cat": data,"uniq_product_name":uniq_product_name}
        return render(request, 'admin/fra_product_from_invet.html', context)
        #return render(request, 'admin/admin_add_fractional_product.html', context)


    else:
        uniq_id = uuid.uuid1()
        uniq_id = uniq_id.hex

        current_user = request.user
        user_id = current_user.id

        input_catagory_name = request.POST.get("input_catagory_name")
        catagory_id = request.POST.get("catagory_id")
        if catagory_id == '0':
            data_catagory_exist = product_catagory.objects.filter(
                acpc_catagory_name=input_catagory_name).exists()
            if data_catagory_exist:
                data_catagory = product_catagory.objects.get(acpc_catagory_name=input_catagory_name)
                if data_catagory.acpc_fra_or_single != 'fractional':
                    messages.error(request, "this catagory already exist in single product catagory please choose a diffrent name for catagory ")
                    return redirect('add_new_product_fractional')
               # catagory_fetch_id_data.id
            else:  # incase catagory not exsist create  a catagory
                b = product_catagory(acpc_catagory_name = input_catagory_name,
                                     acpc_fra_or_single = 'fractional',
                                     acpc_last_modified_by=current_user)
                b.save()

        catagory_fetch_id_data = product_catagory.objects.get(
            acpc_catagory_name=input_catagory_name)
        c = product_master(acpm_product_name=request.POST.get("product_names"),
                           acpm_product_types='fractional',
                           acpm_product_catagory=catagory_fetch_id_data,
                           acpm_waranty_info=request.POST.get("waranty_info"),
                           acpm_serial_number=request.POST.get(
                               "serial_number"),
                           acpm_brand_details=request.POST.get(
                               "brand_details"),
                           acpm_vender_details=request.POST.get(
                               "brought_from"),
                           acpm_po_details=request.POST.get("po_details"),
                           acpm_product_unit=request.POST.get("product_unit"),
                           acpm_product_amount=request.POST.get(
                               "product_quantity"),

                           acpm_uniq_id=str(uniq_id),

                           acpm_last_modified_by=current_user
                           )

        c.save()

        # get the inserted id of product master

        product_master_lattest = product_master.objects.get(
            acpm_uniq_id=str(uniq_id))

        # get the inserted id of product master #

        # save data to barcode
        barcode_number = request.POST.get("barcode_details")

        barcode_get_post = request.POST.get("barcode_type")
        if barcode_number != 'not_recognised':
            barcode_exists = barcode_master.objects.filter(
                acbs_barcode_details=barcode_number).exists()
            if barcode_exists:
                print('mainif_if')
                barcode_master_data = barcode_master.objects.get(
                    acbs_barcode_details=barcode_number)
                barcode_master_data.acbs_product_master_id = product_master_lattest
                barcode_master_data.save()

            else:
                bc = barcode_master(acbs_barcode_details=barcode_number,
                                    acbs_product_master_id=product_master_lattest,
                                    )
                bc.save()
        # save data to barcode#
        lattitude = request.POST.get("latitude")
        longitude = request.POST.get("longitude")
        geo_location = str(lattitude) + ',' + str(longitude)

        last_scaned_by = current_user

        data_dict_qr_insert={"acpqm_product_master_id":product_master_lattest,
                              "acpqm_product_location":geo_location,
                              "acpqm_last_scaned_from":last_scaned_by,
                              "acpqm_last_scaned_by":last_scaned_by,
                              "acpqm_product_movment_details":'admin to admin',
                              "acpqm_uniq_id":"string_qrcode",
                              "acpqm_print_uniq_id" : str(uniq_id),
                              "acpqm_qr_image_path":"QRimage_path",
                              "acpqm_qr_image_name":"qr_image_name",
                              "acpqm_last_modified_by":last_scaned_by}

        string_qrcode=insert_product_qrmaster(data_dict_qr_insert)

        user = current_user
        qrcode_number = string_qrcode
        amount = str(product_master_lattest.acpm_product_amount)
        trans_with = current_user
        credit_or_debit = "debit"
        transection_status = product_transection_fun(user,qrcode_number,amount,trans_with,credit_or_debit)

        # user = current_user
        # qrcode_number = barcode_number
        # amount = str(product_master_lattest.acpm_product_amount)
        # trans_with = current_user
        credit_or_debit = "credit"
        transection_status = product_transection_fun(user,qrcode_number,amount,trans_with,credit_or_debit)
        print(transection_status)

        messages.success(
            request, "fractional product created  successfully ")
        return redirect('lattes_qrcode',print_id=str(uniq_id))






@login_required(login_url='/login/')
def inventory_report(request):
    if request.method == 'GET':


        main_catagory = product_main_catagory.objects.filter(pmc_is_active=True)
        catagory = product_catagory.objects.filter(acpc_is_active=True)
        product_master_data = product_master.objects.filter(acpm_is_active=True)
        
        

        product_main_catagory_maping_data= product_main_catagory_maping.objects.filter(pmcm_is_active=True) 

        uniq_product_transection = product_transaction.objects.filter(pt_is_active=True)       
        
        total_catagory_count= catagory.count()
        total_main_catagory_count= main_catagory.count()
        total_product_count= product_master_data.count()



        current_user = request.user
        groupid = current_user.groups.values_list('id', flat=True).first()
        groupname = current_user.groups.values_list('name', flat=True).first()
        # 'groupid':groupid,
        # 'groupname':groupname

        results=product_master_data

        dict_name={}


        for item in product_master_data:
            prd_name =item.acpm_product_name
            prd_cat = item.acpm_product_catagory.acpc_catagory_name
            prd_main_cat =item.acpm_product_main_catagory.pmc_main_catagory_name

            string_data = prd_name+prd_cat+prd_main_cat

            if string_data in dict_name :
                results  = results.exclude(acpm_id=item.acpm_id)
            else:
                dict_name[string_data]="0"
        
        print(dict_name)      



        context = {'total_main_catagory':main_catagory,
                   'total_catagory':catagory,                   
                   'product_master_data':results,
                   'product_main_catagory_maping_data':product_main_catagory_maping_data,                   

                   'uniq_product_transection':uniq_product_transection,

                   'total_catagory_count':total_catagory_count,
                   'total_main_catagory_count':total_main_catagory_count,
                   'total_product_count':total_product_count,

                   'groupid':groupid,
                   'groupname':groupname
                   
                   }
        return render(request, 'admin/product_report.html', context)

@login_required(login_url='/login/')
def product_trans_by_product_id(request,product_id):
    if request.method == 'GET':
        
        current_user = request.user

        product_master_exists = product_master.objects.filter(acpm_id=product_id).exists()

        if product_master_exists :
            
            product_master_lattest = product_master.objects.get(pk=product_id)

            product_transaction_exists = product_transaction.objects.filter(pt_user=current_user,
                                                                        pt_product_name = product_master_lattest.acpm_product_name,
                                                                        pt_product_unit = product_master_lattest.acpm_product_unit,
                                                                        pt_product_catagory = product_master_lattest.acpm_product_catagory,
                                                                        pt_product_main_catagory = product_master_lattest.acpm_product_main_catagory).exists()
            
            if product_transaction_exists :
                product_transaction_data = product_transaction.objects.get(pt_user=current_user,
                                                                        pt_product_name = product_master_lattest.acpm_product_name,
                                                                        pt_product_unit = product_master_lattest.acpm_product_unit,
                                                                        pt_product_catagory = product_master_lattest.acpm_product_catagory,
                                                                        pt_product_main_catagory = product_master_lattest.acpm_product_main_catagory)
                pt_id_get=product_transaction_data.pt_id
                return redirect('product_trans_by_id',pt_id=pt_id_get,user_id="na")
            else:
                messages.error(request, "no transection found ")
                return redirect('inventory_report')
        else:
            messages.error(request, "no transection found ")
            return redirect('inventory_report')
    else:
        messages.error(request, "no transection found ")
        return redirect('inventory_report')

            
        



