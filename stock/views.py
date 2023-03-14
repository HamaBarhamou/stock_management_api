from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import ProductSerializer, StockSerializer, CompanyWarehouseSerializer
from .serializers import CompanySerializer
from django.views.decorators.csrf import csrf_exempt
from .models import Product, Stock, Threshold, CompanyWarehouse, Company
from rest_framework.parsers import JSONParser
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F
    
    
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Récupération de l'utilisateur connecté
        user = self.request.user
        
        # Filtre pour récupérer les produits des entreprises de l'utilisateur
        companies = Company.objects.filter(created_by=user)
        queryset = []
        for company in companies:
            queryset += Product.objects.filter(company=company)
            
        return queryset

    # Return a list of products that have a quantity in stock of low_stock or lower
    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        company = get_object_or_404(Company, created_by=request.user)
        threshold = get_object_or_404(Threshold, company=company, name='low_stock', defaults={'value': 10})
        products = self.get_queryset().filter(quantity_in_stock__lte=threshold.value)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    # Return a list of products that have a rotation of low_demand or lower
    @action(detail=False, methods=['get'])
    def low_demand(self, request):
        company = get_object_or_404(Company, created_by=request.user)
        threshold = get_object_or_404(Threshold, company=company, name='low_demand', defaults={'value': 5})
        products = self.get_queryset().filter(rotation__lte=threshold.value)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    # Return a list of products that have a profit margin of low_profit_margin or lower
    @action(detail=False, methods=['get'])
    def low_profit_margin(self, request):
        company = get_object_or_404(Company, created_by=request.user)
        threshold = get_object_or_404(Threshold,company=company, name='low_profit_margin', defaults={'value': 0.1})
        products = self.get_queryset().filter(profit_margin__lte=threshold.value)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    # Return a list of products that have a quantity in stock of low_quantity or lower
    @action(detail=False, methods=['get'])
    def low_quantity(self, request):
        company = get_object_or_404(Company, created_by=request.user)
        threshold = get_object_or_404(Threshold, company=company, name='low_quantity', defaults={'value': 5})
        products = self.get_queryset().filter(quantity_in_stock__lte=threshold.value)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    # Return a list of products that have a rotation of low_rotation or lower
    @action(detail=False, methods=['get'])
    def low_rotation(self, request):
        company = get_object_or_404(Company, created_by=request.user)
        threshold = get_object_or_404(Threshold, company=company, name='low_rotation', defaults={'value': 2})
        products = self.get_queryset().filter(rotation__lte=threshold.value)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    # Return a list of products that have a rotation of high_demand or higher
    @action(detail=False, methods=['get'])
    def high_demand(self, request):
        company = get_object_or_404(Company, created_by=request.user)
        threshold = get_object_or_404(Threshold, company=company, name='high_demand', defaults={'value': 8})
        products = self.get_queryset().filter(rotation__gte=threshold.value)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    # Return a list of products that have a profit margin of high_profit_margin or higher
    @action(detail=False, methods=['get'])
    def high_profit_margin(self, request):
        company = get_object_or_404(Company, created_by=request.user)
        threshold = get_object_or_404(Threshold, company=company, name='high_profit_margin', defaults={'value': 0.2})
        products = self.get_queryset().filter(profit_margin__gte=threshold.value)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    # Return a list of products that have a rotation of high_rotation or higher
    @action(detail=False, methods=['get'])
    def high_rotation(self, request):
        company = get_object_or_404(Company, created_by=request.user)
        threshold = get_object_or_404(Threshold, company=company, name='high_rotation', defaults={'value': 10})
        products = self.get_queryset().filter(rotation__gte=threshold.value)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    # Return a list of products that are on clearance
    @action(detail=False, methods=['get'])
    def clearance(self, request):
        products = self.get_queryset().filter(on_clearance=True)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    # Return a list of products that are on sale
    @action(detail=False, methods=['get'])
    def sale(self, request):
        products = self.get_queryset().filter(on_sale=True)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    # Return a list of products that are out of stock
    @action(detail=False, methods=['get'])
    def out_of_stock(self, request):
        products = self.get_queryset().filter(quantity_in_stock=0)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)


class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        # filtrer les stocks par entreprise et entrepôt associés à l'utilisateur
        user = self.request.user
        stocks = Stock.objects.filter(
            product__company__created_by=user,
            warehouse__company__created_by=user
        )

        # filtrer les stocks en fonction des paramètres de requête
        on_delivery = self.request.query_params.get('on_delivery', None)
        on_reorder = self.request.query_params.get('on_reorder', None)
        on_return = self.request.query_params.get('on_return', None)

        if on_delivery is not None:
            stocks = stocks.filter(on_delivery=on_delivery)
        if on_reorder is not None:
            stocks = stocks.filter(on_reorder=on_reorder)
        if on_return is not None:
            stocks = stocks.filter(on_return=on_return)

        return stocks
    
    # Définir une fonction disponible qui retourne tous les stocks disponibles
    @action(detail=False, methods=['get'])
    def available(self, request):
        stocks = self.get_queryset().filter(on_delivery=False, on_reorder=False, on_return=False)
        serializer = self.get_serializer(stocks, many=True)
        return Response(serializer.data)

    # Définir une fonction en cours de livraison qui retourne tous les stocks en cours de livraison
    @action(detail=False, methods=['get'])
    def on_delivery(self, request):
        stocks = self.get_queryset().filter(on_delivery=True)
        serializer = self.get_serializer(stocks, many=True)
        return Response(serializer.data)
    
    # Fonction pour obtenir tous les stocks associés à une entreprise
    @action(detail=True, methods=['get'])
    def by_company(self, request, pk=None):
        company = get_object_or_404(Company, pk=pk, created_by=request.user)
        stocks = self.get_queryset().filter(product__company=company)
        serializer = self.get_serializer(stocks, many=True)
        return Response(serializer.data)

    # Fonction pour obtenir tous les stocks associés à un entrepôt
    @action(detail=True, methods=['get'])
    def by_warehouse(self, request, pk=None):
        warehouse = get_object_or_404(CompanyWarehouse, pk=pk, company__created_by=request.user)
        stocks = self.get_queryset().filter(warehouse=warehouse)
        serializer = self.get_serializer(stocks, many=True)
        return Response(serializer.data)

    # Fonction pour obtenir tous les stocks associés à l'utilisateur
    @action(detail=False, methods=['get'])
    def by_user(self, request):
        stocks = self.get_queryset()
        serializer = self.get_serializer(stocks, many=True)
        return Response(serializer.data)

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Company.objects.filter(created_by=self.request.user)
    
    def perform_create(self, serializer):
        serializer.validated_data['created_by'] = self.request.user
        serializer.save()

class CompanyWarehouseViewSet(viewsets.ModelViewSet):
    queryset = CompanyWarehouse.objects.all()
    serializer_class = CompanyWarehouseSerializer
    permission_classes = [permissions.IsAuthenticated]
        
    def get_queryset(self):
        company_ids = Company.objects.filter(created_by=self.request.user).values_list('id', flat=True)
        queryset = CompanyWarehouse.objects.filter(company__in=company_ids)
        return queryset
    


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def stock_list(request):
    companies = request.user.created_companies.all()
    stocks = Stock.objects.filter(warehouse__company__in=companies)
    return render(request, 'stock_list.html', {'stocks': stocks})

@login_required
def stock_detail(request, stock_id):
    stock = Stock.objects.get(id=stock_id)
    return render(request, 'stock_detail.html', {'stock': stock})

@login_required
def statistics(request):
    company = request.user.created_companies.first() # on récupère la première entreprise créée par l'utilisateur
    warehouse_totals = CompanyWarehouse.objects.filter(company=company).annotate(total_stock=Sum('stock__quantity'))
    company_total = Company.objects.filter(id=company.id).annotate(total_stock=Sum('warehouses__stock__quantity'))
    return render(request, 'statistics.html', {'warehouse_totals': warehouse_totals, 'company_total': company_total})

@login_required
def home(request):
    user = request.user
    created_companies = user.created_companies.all()
    warehouses = CompanyWarehouse.objects.filter(company__in=created_companies)
    context = {
        'enterprises': created_companies,
        'warehouses': warehouses,
    }
    return render(request, 'user/home.html', context)

@login_required
def enterprise_detail(request, enterprise_id):
    enterprise = Company.objects.get(id=enterprise_id, created_by=request.user)
    context = {
        'enterprise': enterprise,
    }
    return render(request, 'user/enterprise_detail.html', context)

@login_required
def warehouse_detail(request, warehouse_id):
    warehouse = CompanyWarehouse.objects.get(id=warehouse_id, company__created_by=request.user)
    context = {
        'warehouse': warehouse,
    }
    return render(request, 'user/warehouse_detail.html', context)

@login_required
def stock_statistics(request):
    user = request.user
    enterprises = Company.objects.filter(owner=user)
    statistics = {}
    for enterprise in enterprises:
        warehouses = CompanyWarehouse.objects.filter(enterprise=enterprise)
        for warehouse in warehouses:
            stocks = Stock.objects.filter(warehouse=warehouse)
            total_value = stocks.aggregate(total=Sum(F('quantity') * F('unit_cost')))['total'] or 0
            statistics[f'{enterprise.name} - {warehouse.name}'] = {
                'total_value': total_value,
                'stock_count': stocks.count(),
            }
    context = {
        'statistics': statistics,
    }
    return render(request, 'user/stock_statistics.html', context)
