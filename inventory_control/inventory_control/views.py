from django.shortcuts import render
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt



@csrf_exempt
def main_login(request):

    if request.user.is_authenticated:
        user = request.user
        groupid = user.groups.values_list('id', flat=True).first()
        groupname = user.groups.values_list('name', flat=True).first()

        #2 project site_manager
        #3 project user
        context = {"user":user,"groupid":groupid,'groupname':groupname}
        return render(request, 'index.html', context)

    if request.method == "GET":
        context = {"data":"data"}
        return render(request, 'login.html', context)

    else:
        email = request.POST.get("email")
        password = request.POST.get("password")

        email_id_exist = User.objects.filter(email=email.lower()).exists()
        if not(email_id_exist):
            context = {"user":"wp","login_try":"Y"}
            return render(request, 'login.html', context)

        username = User.objects.get(email=email.lower()).username

        user = authenticate(request,username=username, password=password)
        if user is not None:
            login(request, user)

            groupid = user.groups.values_list('id', flat=True).first()
            groupname = user.groups.values_list('name', flat=True).first()

            #2 project site_manager
            #3 project user
            context = {"user":user,"groupid":groupid,'groupname':groupname}
            return render(request, 'index.html', context)

        else:
            context = {"user":"wp","login_try":"Y"}
            return render(request, 'login.html', context)

@csrf_exempt
def error_page(request):
    if request.method == "GET":
        context = {"data":"data"}
        return render(request, '404.html', context)
