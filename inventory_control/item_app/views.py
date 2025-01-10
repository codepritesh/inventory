from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from .forms import item_form
from .models import item_master



# def site_create(request):
#     if request.method == "GET":
#         context = {"data":"data"}
#         return render(request, 'site_app/site_create_index.html', context)
#     else:
#         context = {"data":"data"}
#         return render(request, 'site_app/site_create_index.html', context)


def item_create(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        print ('post')
        # create a form instance and populate it with data from the request:
        form = item_form(request.POST)
        # check whether it's valid:
        if form.is_valid():
           
            form.save()

            # # process the data in form.cleaned_data as required
            # obj = Listing() #gets new object
            # obj.business_name = form.cleaned_data['business_name']
            # obj.business_email = form.cleaned_data['business_email']
            # obj.business_phone = form.cleaned_data['business_phone']
            # obj.business_website = form.cleaned_data['business_website']
            # #finally save the object in db
            #obj.save()
            # ...
            # redirect to a new URL:
            return redirect('item_view')
            

    # if a GET (or any other method) we'll create a blank form
    else:
        form = item_form()

    return render(request, 'item_app/item_form.html', {'form': form})


def item_view(request):
    if request.method =='GET':
        #query_results = item_master.objects.all()
        curent_page = 1 
        pagedata_starting = 0
        pagedata_ending = pagedata_starting + 5

        prev_pagenumber = 1
        next_page_number = 2
        totaldata = item_master.objects.all().order_by('created_at').count()


        query_results = item_master.objects.all().order_by('created_at')[:pagedata_ending]
        showingdata = query_results.count()
        
        
        context = {"query_results":query_results,
                   'totaldata':totaldata,
                   'curent_page':curent_page,
                   'pagedata_starting':pagedata_starting,
                   'prev_pagenumber':prev_pagenumber,
                   'next_page_number':next_page_number,
                   'showingdata':showingdata
                   
                   }
        return render(request, 'item_app/item_view.html', context)


def item_view_pagination(request,page_number):
    if request.method =='GET':

        #query_results = site_master.objects.all()
        if page_number != 1:
            curent_page = int(page_number)
            page_number = page_number-1
            prev_pagenumber = curent_page - 1
            pagedata_starting = page_number * 5
            pagedata_ending = pagedata_starting + 5
        else:
            curent_page = 1
            page_number = 1
            prev_pagenumber = 1
            pagedata_starting = 0
            pagedata_ending = pagedata_starting + 5
            
    

        
        next_page_number = curent_page + 1 

        totaldata = item_master.objects.all().order_by('created_at').count()


        query_results = item_master.objects.all().order_by('created_at')[pagedata_starting:pagedata_ending]
        showingdata = query_results.count()
        
        
        
        context = {"query_results":query_results,
                   'totaldata':totaldata,
                   'curent_page':curent_page,
                   'pagedata_starting':pagedata_starting,
                   'prev_pagenumber':prev_pagenumber,
                   'next_page_number':next_page_number,
                   'showingdata':showingdata
                   
                   }
        return render(request, 'item_app/item_view.html', context)
        



