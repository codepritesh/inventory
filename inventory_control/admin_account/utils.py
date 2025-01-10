
import cv2
import numpy as np
from pyzbar import pyzbar

from .models import *
import os

import base64
import string
import random
import qrcode
from django.db import IntegrityError
from re import search
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from django.conf import settings





def allowed_file_image(filename):
    ALLOWED_EXTENSIONS_IMAGE = set(['png', 'jpg', 'jpeg'])

    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_IMAGE

def Upload_file_image(file,path_ex,img_file_name):
    if file and allowed_file_image(file.filename):
        file.save(os.path.join(path_ex, img_file_name))
        return img_file_name
    else:
        return False

def save_filewc(file,ppi_id,path_ex):

    split_tup = os.path.splitext(file.filename)
    file_name = split_tup[0]
    file_extension = split_tup[1]

    img_file_name = "Instaled_img_" + str(ppi_id) + file_extension

    get_filename = Upload_file_image(file,path_ex,img_file_name)
    return get_filename

def base64_to_barcodenumber(imagedata):
    img = data_uri_to_cv2_img(imagedata)
    # cv2.imshow('',img)
    # cv2.waitKey(0)
    result_dict = barcode_read(img)
    return result_dict




def data_uri_to_cv2_img(uri):
    encoded_data = uri.split(',')[1]
    # print(encoded_data)
    im_bytes = base64.b64decode(encoded_data)
    # im_arr is one-dim Numpy array
    im_arr = np.frombuffer(im_bytes, dtype=np.uint8)
    img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
    return img


def uniq_string_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def insert_product_qrmaster(d):
    try:
        #file_path = os.path.join(settings.STATIC_ROOT, 'data/foobar.csv')



        get_acpqm_uniq_id = uniq_string_generator()
        d["acpqm_uniq_id"] = get_acpqm_uniq_id

        string_qrcode = str(get_acpqm_uniq_id)
        qr = qrcode.make(string_qrcode)

        I1 = ImageDraw.Draw(qr)
        myFont = ImageFont.truetype(settings.STATIC_ROOT+'/assets/font/OpenSans-ExtraBold.ttf', 27)
        # Add Text to an image
        I1.text((40, 1),string_qrcode,font=myFont,fill=(0))
        # stroke_fill="black"


        QRimage_path = settings.STATIC_ROOT+"/assets/img/"
        qr_image_name = string_qrcode + ".png"
        image_address = QRimage_path + qr_image_name

        d["acpqm_qr_image_path"] = QRimage_path
        d["acpqm_qr_image_name"] = qr_image_name


        d = product_qr_master(acpqm_product_master_id=d["acpqm_product_master_id"],
                              acpqm_product_location=d["acpqm_product_location"],
                              acpqm_last_scaned_from=d["acpqm_last_scaned_from"],
                              acpqm_last_scaned_by=d["acpqm_last_scaned_by"],
                              acpqm_product_movment_details=d["acpqm_product_movment_details"],
                              acpqm_uniq_id=d["acpqm_uniq_id"],
                              acpqm_print_uniq_id =d["acpqm_print_uniq_id"],
                              acpqm_qr_image_path=d["acpqm_qr_image_path"],
                              acpqm_qr_image_name=d["acpqm_qr_image_name"],
                              acpqm_last_modified_by=d["acpqm_last_modified_by"]
                              )
        d.save()
        qr.save(image_address)



        #this code will create a pdf and will save it to pdf

        # img_list=[image_address]
        # im_list=[]
        # for imagename in img_list:
        #     im1 = Image.open(imagename)
        #     im_list.append(im1)
        # path = "static/assets/pdf/"
        # pdf_fil_ename = path+get_acpqm_uniq_id+".pdf"
        # pdfimg = im_list[0]
        # print(im_list,'im_list-----------------------im_list-------------------im_list')
        # pdfimg.save(pdf_fil_ename, "PDF" ,resolution=100.0, save_all=True, append_images=im_list)

        image1 = Image.open(image_address)
        #im1 = image1.convert('RGB')
        path = settings.STATIC_ROOT+"/assets/pdf/"
        pdf_fil_ename = path+get_acpqm_uniq_id+".pdf"
        image1.save(pdf_fil_ename)

        return string_qrcode

    except Exception as e:
        if search("Duplicate entry", str(e)):
            insert_product_qrmaster(d)
        else:
            print(str(e),"something error happened")



def product_transection_fun(user,qrcode_number,amount,trans_with,credit_or_debit):
    return_status={}

    qrcode_exists = product_qr_master.objects.filter(acpqm_uniq_id=qrcode_number).exists()

    if qrcode_exists :
        qrcode_exists_data = product_qr_master.objects.get(acpqm_uniq_id=qrcode_number)


        product_name = qrcode_exists_data.acpqm_product_master_id.acpm_product_name
        product_unit = qrcode_exists_data.acpqm_product_master_id.acpm_product_unit
        product_catagory_obj = qrcode_exists_data.acpqm_product_master_id.acpm_product_catagory
        product_main_catagory_obj = qrcode_exists_data.acpqm_product_master_id.acpm_product_main_catagory


        product_transaction_exists = product_transaction.objects.filter(pt_user=user,
                                                                        pt_product_name = product_name,
                                                                        pt_product_unit = product_unit,
                                                                        pt_product_catagory = product_catagory_obj,
                                                                        pt_product_main_catagory = product_main_catagory_obj).exists()
        if product_transaction_exists:

            #then update  product_transaction
            data_pt_row = product_transaction.objects.get(pt_user=user,
                                            pt_product_name = product_name,
                                            pt_product_unit = product_unit,
                                            pt_product_catagory = product_catagory_obj,
                                            pt_product_main_catagory = product_main_catagory_obj)
            amount_int = int(amount)
            table_amount = int(data_pt_row.pt_product_amount)
            data_pt_row.pt_last_modified_by = user

            if credit_or_debit =="credit":


                data_pt_row.pt_product_amount = table_amount + amount_int
                c = all_product_transaction(apt_user=user,
                                           apt_product_name=data_pt_row,
                                           apt_credit_amount=amount_int,
                                           apt_debit_amount= 0,
                                           apt_description="credited amount "+str(amount_int)+"",
                                           apt_credited_or_debited_with=trans_with,
                                           )
                c.save()
                data_pt_row.save()

                return_status['status']=1
                return_status['message']="credit Transection done successfully"

                return return_status


            else:
                print('step4')
                if (table_amount >= amount_int):

                    data_pt_row.pt_product_amount = table_amount - amount_int

                    d = all_product_transaction(apt_user=user,
                                               apt_product_name=data_pt_row,
                                               apt_credit_amount= 0,
                                               apt_debit_amount= amount_int,
                                               apt_description="Debited amount "+str(amount_int)+".",
                                               apt_credited_or_debited_with=trans_with
                                               )
                    d.save()
                    data_pt_row.save()


                    return_status['status']=1
                    return_status['message']="debit Transection done successfully"

                    return return_status
                else:

                    return_status['status']=0
                    return_status['message']="Amount is greater then present amount"

                    return return_status


        else:

            #if product transection not exists
            if credit_or_debit =="debit":

                return_status['status']=0
                return_status['message']="no credit amount exist for debit."

                return return_status

            else:


                nc = product_transaction(pt_user=user,
                                           pt_product_name= product_name,
                                           pt_product_unit= product_unit,
                                           pt_product_amount= int(amount),
                                           pt_product_catagory= product_catagory_obj,
                                           pt_product_main_catagory = product_main_catagory_obj,
                                           pt_last_modified_by= user
                                           )
                nc.save()

                data_pt_row = product_transaction.objects.get(pt_user=user,
                                                pt_product_name = product_name,
                                                pt_product_unit = product_unit,
                                                pt_product_catagory = product_catagory_obj,
                                                pt_product_main_catagory = product_main_catagory_obj)
                amount_int = int(amount)

                nct = all_product_transaction(apt_user=user,
                                           apt_product_name= data_pt_row,
                                           apt_credit_amount= amount_int,
                                           apt_debit_amount= 0,
                                           apt_description="credited amount "+str(amount_int)+"",
                                           apt_credited_or_debited_with=trans_with,
                                           )
                nct.save()


                return_status['status'] = 1
                return_status['message'] = "new transection added successfully"
                return return_status
    else:

        return_status['status'] = 0
        return_status['message'] = "no qr code data exist."
        return return_status


def barcode_read(image):
    barcodes = pyzbar.decode(image)
    # print(barcodes)
    # loop over the detected barcodes
    barcodeData = 'na'
    barcodeType = 'na'
    for barcode in barcodes:
        # extract the bounding box location of the barcode and draw the
        # bounding box surrounding the barcode on the image
        (x, y, w, h) = barcode.rect
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
        # the barcode data is a bytes object so if we want to draw it on
        # our output image we need to convert it to a string first
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type
        #print(barcodeType, '********************************************type')
        # draw the barcode data and barcode type on the image
        text = "{} ({})".format(barcodeData, barcodeType)
        cv2.putText(image, text, (x+10, y+h+20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        # print the barcode type and data to the terminal
        #print("[INFO] Found {} barcode: {}".format(barcodeType, barcodeData))
        break
    # show the output image
    #cv2.imshow("Image", image)
    retval, buffer_img = cv2.imencode('.jpg', image)
    data_image_bas64_bites = base64.b64encode(buffer_img)
    base64_message = data_image_bas64_bites.decode('utf-8')
    found_data = {'barcodeData': barcodeData,
                  'barcodeType': barcodeType, 'image_rec_base64': base64_message}
    return found_data
