
from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('site_app/', include('site_app.urls')),
    path('admin_dashboard/', include('admin_dashboard.urls')),
    path('', include('admin_dashboard.urls')),
    path('admin_account/', include('admin_account.urls')),
    path('login/', views.main_login, name='main_login'),
    path('error_page/', views.error_page, name='error_page'),
    path('vender_app/', include('vender_app.urls')),
    path('item_app/', include('item_app.urls')),
    path('site_manager/', include('site_manager.urls')),
    path('site_user/', include('site_user.urls')),
    path('started_project/', include('start_project.urls')),



]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
