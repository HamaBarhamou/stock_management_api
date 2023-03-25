from django.urls import path
from .views import CompanyListView, CompanyCreateView, CompanyUpdateView, CompanyDeleteView
from .views import CompanyWarehouseListView, CompanyWarehouseCreateView
from .views import CompanyWarehouseUpdateView, CompanyWarehouseDeleteView
from .views import ProductList, ProductCreate, ProductUpdate, ProductDelete, product_detail
from .views import StockListView, StockCreateView, StockDetailView, StockUpdateView, StockDeleteView
from .views import threshold_list, threshold_edit


from . import views

app_name = 'stock'

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('stocks/', views.stock_list, name='stock_list_menue'),
    path('product_liste/', views.product_list, name='product_liste'),
    path('stock/<int:stock_id>/', views.stock_detail, name='stock_detail'),
    path('statistics/', views.statistics, name='statistics'),
    path('enterprise/<int:enterprise_id>/', views.enterprise_detail, name='enterprise_detail'),
    path('warehouse/<int:warehouse_id>/', views.warehouse_detail, name='warehouse_detail'),
    path('stock_statistics/', views.stock_statistics, name='stock_statistics'),
    path('my_custom_view/', views.my_custom_view, name='my_custom_view'),
    path('landing/', views.landingpage, name='landing'),
    
    path('company_list/', CompanyListView.as_view(), name='company_list'),
    path('company_create/', CompanyCreateView.as_view(), name='company_create'),
    path('update/<int:pk>/', CompanyUpdateView.as_view(), name='company_update'),
    path('delete/<int:pk>/', CompanyDeleteView.as_view(), name='company_delete'),
    
    path('companywarehouse/', CompanyWarehouseListView.as_view(), name='company_warehouse_list'),
    path('companywarehouse/create/', CompanyWarehouseCreateView.as_view(), name='company_warehouse_create'),
    path('companywarehouse/<int:pk>/update/', CompanyWarehouseUpdateView.as_view(), name='company_warehouse_update'),
    path('companywarehouse/<int:pk>/delete/', CompanyWarehouseDeleteView.as_view(), name='company_warehouse_delete'),
    
    path('product_list', ProductList.as_view(), name='product_list'),
    path('product_create/', ProductCreate.as_view(), name='product_create'),
    path('<int:pk>/update/', ProductUpdate.as_view(), name='product_update'),
    path('<int:pk>/delete/', ProductDelete.as_view(), name='product_delete'),
    path('<int:pk>/', product_detail, name='product_detail'),
    
    path('stock_list', StockListView.as_view(), name='stock_list'),
    path('stock_create/', StockCreateView.as_view(), name='stock_create'),
    path('<int:pk>/stock', StockDetailView.as_view(), name='stock_detail_db'),
    path('<int:pk>/update_stock/', StockUpdateView.as_view(), name='stock_update'),
    path('<int:pk>/delete_stock/', StockDeleteView.as_view(), name='stock_delete'),
    
    path('threshold_list', views.threshold_list, name='threshold_list'),
    path('<int:threshold_id>/threshold_edit/', views.threshold_edit, name='threshold_edit'),
    
    path('clearance/', views.clearance_products, name='clearance_products'),
    path('low-stock/', views.low_stock_products, name='low_stock'),
]
