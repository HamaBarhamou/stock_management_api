"""stock_management_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from stock import views as views_stock
from user import views as views_user
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework.authtoken.views import ObtainAuthToken
from django.conf import settings
from django.conf.urls.static import static


router = routers.DefaultRouter()
router.get_api_root_view().cls.__name__ = "Stock Management Api"
router.get_api_root_view().cls.__doc__ = "This application is an API-based \
    inventory management system created with Django and Django REST Framework."
router.register(r'users', views_user.UserViewSet)
router.register(r'Company', views_stock.CompanyViewSet)
router.register(r'CompanyWarehouse', views_stock.CompanyWarehouseViewSet)
router.register(r'product', views_stock.ProductViewSet)
router.register(r'stock', views_stock.StockViewSet)
router.register(r'product', views_stock.ProductViewSet, basename='product')
#router.register(r'groups', views_user.GroupViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api', include(router.urls)),
    path('home/', include('stock.urls')),
    path('', include('landingpage.urls')),
    path('user/', include('user.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('logout/', views_user.logout_view, name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)