from django.urls import path
from .views import CompanyListView, CompanyCreateView, CompanyUpdateView, CompanyDeleteView
from .views import CompanyWarehouseListView, CompanyWarehouseCreateView
from .views import CompanyWarehouseUpdateView, CompanyWarehouseDeleteView

from . import views

app_name = 'stock'

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('stocks/', views.stock_list, name='stock_list'),
    path('stock/<int:stock_id>/', views.stock_detail, name='stock_detail'),
    path('statistics/', views.statistics, name='statistics'),
    path('enterprise/<int:enterprise_id>/', views.enterprise_detail, name='enterprise_detail'),
    path('warehouse/<int:warehouse_id>/', views.warehouse_detail, name='warehouse_detail'),
    path('stock_statistics/', views.stock_statistics, name='stock_statistics'),
    path('my_custom_view/', views.my_custom_view, name='my_custom_view'),
    path('landing/', views.landingpage, name='landing'),
    path('company_list/', CompanyListView.as_view(), name='company_list'),
    path('create/', CompanyCreateView.as_view(), name='company_create'),
    path('update/<int:pk>/', CompanyUpdateView.as_view(), name='company_update'),
    path('delete/<int:pk>/', CompanyDeleteView.as_view(), name='company_delete'),
    path('companywarehouse/', CompanyWarehouseListView.as_view(), name='company_warehouse_list'),
    path('companywarehouse/create/', CompanyWarehouseCreateView.as_view(), name='company_warehouse_create'),
    path('companywarehouse/<int:pk>/update/', CompanyWarehouseUpdateView.as_view(), name='company_warehouse_update'),
    path('companywarehouse/<int:pk>/delete/', CompanyWarehouseDeleteView.as_view(), name='company_warehouse_delete'),
]
