from django.urls import path
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
    #path('product/low_demand_by_company/<int:company_id>/', views.ProductViewSet.as_view({'get': 'low_demand_by_company'}), name='low_demand_by_company'),
    #path('product/low_stock/<int:company_id>/', views.ProductViewSet.as_view({'get': 'low_stock'}), name='low_stock'),


]
