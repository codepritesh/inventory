from django.shortcuts import render




def started_project(request,po_id):
    if request.method == "GET":
        context = {"data": "data"}
        return render(request, 'login.html', context)
    else:
        context = {"data": "data"}
        return render(request, 'login.html', context)


def project_manager_dashboard(request):
    if request.method == "GET":
        context = {"data": "data"}
        return render(request, 'dashboard/project_manage_dashboard.html', context)
    else:
        context = {"data": "data"}
        return render(request, 'login.html', context)


def project_user_dashboard(request):
    if request.method == "GET":
        context = {"data": "data"}
        return render(request, 'dashboard/project_user_dashboard.html', context)
    else:
        context = {"data": "data"}
        return render(request, 'login.html', context)


def inventory_dashboard(request):
    if request.method == "GET":
        context = {"data": "data"}
        return render(request, 'dashboard/inventory_dashboard.html', context)
    else:
        context = {"data": "data"}
        return render(request, 'login.html', context)

def product_management_dash(request):
    if request.method == "GET":
        context = {"data": "data"}
        return render(request, 'dashboard/product_management_dashboard.html', context)
    else:
        context = {"data": "data"}
        return render(request, 'login.html', context)

def project_dashboard(request):
    if request.method == "GET":
        context = {"data": "data"}
        return render(request, 'dashboard/project_dashboard.html', context)
    else:
        context = {"data": "data"}
        return render(request, 'login.html', context)
