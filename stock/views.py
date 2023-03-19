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
from django.db.models import Sum, F, Q
from rest_framework import status
from django.core.paginator import Paginator
from django.urls import reverse

    
    
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Récupération de l'utilisateur connecté
        user = self.request.user
        # Filtre pour récupérer les produits des entreprises de l'utilisateur
        companies = Company.objects.filter(created_by=user)
        companies = Company.objects.filter(created_by=user)
        return Product.objects.filter(company__in=companies)
    
    # Return a list of products that have a quantity in stock of low_stock or lower
    @action(detail=False, methods=['get'], url_path='low_stock/(?P<company_id>[^/.]+)')
    def low_stock(self, request, company_id):
        """
            Returns a list of products that have a quantity in stock of low_stock or lower.
            This is achieved by filtering the products based on the threshold value set for 
            low_stock in the specified company. The result is serialized using the serializer 
            defined for this viewset and returned as a response.
        """
        company = get_object_or_404(Company, id=company_id, created_by=request.user)
        threshold = get_object_or_404(Threshold, company=company, name='low_stock')
        products = self.get_queryset().filter(quantity_in_stock__lte=threshold.value)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    # Return a list of products that have a rotation of low_demand or lower
    @action(detail=False, methods=['get'], url_path='low_demand_by_company/(?P<company_id>[^/.]+)')
    def low_demand_by_company(self, request, company_id):
        """
            Retrieve a list of products that have a rotation of low_demand or lower for a given company.

            Args:
                company_id (int): The ID of the company for which to retrieve the list of products.

            Returns:
                A list of products that have a rotation of low_demand or lower for the given company.

            Raises:
                Http404: If the company or threshold object does not exist.
        """
        company = get_object_or_404(Company, id=company_id, created_by=request.user)
        threshold = get_object_or_404(Threshold, company=company, name='low_demand')
        products = self.get_queryset().filter(company=company, rotation__lte=threshold.value)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    # Return a list of products that have a profit margin of low_profit_margin or lower
    @action(detail=False, methods=['get'], url_path='low_profit_margin/(?P<company_id>[^/.]+)')
    def low_profit_margin(self, request, company_id):
        """
        Retrieve a list of products that have a profit margin of low_profit_margin or lower.

        :param request: The request object.
        :param company_id: The ID of the company to filter the products by.
        :type company_id: int
        :return: A list of products with low profit margins.
        :rtype: Response
        """
        company = get_object_or_404(Company, id=company_id, created_by=request.user)
        threshold = get_object_or_404(Threshold,company=company, name='low_profit_margin')
        products = self.get_queryset().filter(profit_margin__lte=threshold.value)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    # Return a list of products that have a quantity in stock of low_quantity or lower
    @action(detail=False, methods=['get'], url_path='low_quantity/(?P<company_id>[^/.]+)')
    def low_quantity(self, request, company_id):
        """
        Retrieve a list of products that have a quantity in stock of low_quantity or lower.

        :param request: The request object.
        :param company_id: The ID of the company to filter the products by.
        :type company_id: int
        :return: A list of products with low stock quantities.
        :rtype: Response
        """
        company = get_object_or_404(Company, id=company_id, created_by=request.user)
        threshold = get_object_or_404(Threshold, company=company, name='low_quantity')
        products = self.get_queryset().filter(quantity_in_stock__lte=threshold.value)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    # Return a list of products that have a rotation of low_rotation or lower
    @action(detail=False, methods=['get'], url_path='low_rotation/(?P<company_id>[^/.]+)')
    def low_rotation(self, request, company_id):
        """
        Retrieve a list of products that have a rotation of low_rotation or lower.

        :param request: The request object.
        :param company_id: The ID of the company to filter the products by.
        :type company_id: int
        :return: A list of products with low rotations.
        :rtype: Response
        """
        company = get_object_or_404(Company, id=company_id, created_by=request.user)
        threshold = get_object_or_404(Threshold, company=company, name='low_rotation')
        products = self.get_queryset().filter(rotation__lte=threshold.value)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    # Return a list of products that have a rotation of high_demand or higher
    @action(detail=False, methods=['get'], url_path='high_demand/(?P<company_id>[^/.]+)')
    def high_demand(self, request, company_id):
        company = get_object_or_404(Company, id=company_id, created_by=request.user)
        threshold = get_object_or_404(Threshold, company=company, name='high_demand')
        products = self.get_queryset().filter(rotation__gte=threshold.value)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    # Return a list of products that have a profit margin of high_profit_margin or higher
    @action(detail=False, methods=['get'], url_path='high_profit_margin/(?P<company_id>[^/.]+)')
    def high_profit_margin(self, request, company_id):
        """
        Return a list of products that have a profit margin of low_profit_margin or lower.

        :param request: Request object.
        :param company_id: Id of the company whose products to filter.
        :type company_id: str
        :return: List of products with profit margin <= low_profit_margin threshold.
        :rtype: rest_framework.response.Response
        """
        company = get_object_or_404(Company, id=company_id, created_by=request.user)
        threshold = get_object_or_404(Threshold, company=company, name='high_profit_margin')
        products = self.get_queryset().filter(profit_margin__gte=threshold.value)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    # Return a list of products that have a rotation of high_rotation or higher
    @action(detail=False, methods=['get'], url_path='high_rotation/(?P<company_id>[^/.]+)')
    def high_rotation(self, request, company_id):
        company = get_object_or_404(Company, id=company_id, created_by=request.user)
        threshold = get_object_or_404(Threshold, company=company, name='high_rotation')
        products = self.get_queryset().filter(rotation__gte=threshold.value)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    # Return a list of products that are on clearance
    @action(detail=False, methods=['get'])
    def clearance(self, request):
        products = self.get_queryset().filter(on_clearance=True)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='clearance/(?P<company_id>[^/.]+)')
    def clearance_by(self, request, company_id):
        products = self.get_queryset().filter(company=company_id, on_clearance=True)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    # Return a list of products that are on sale
    @action(detail=False, methods=['get'])
    def sale(self, request):
        products = self.get_queryset().filter(on_sale=True)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
    
    # Return a list of products that are on sale
    @action(detail=False, methods=['get'], url_path='sale/(?P<company_id>[^/.]+)')
    def sale_by(self, request, company_id):
        products = self.get_queryset().filter(company=company_id, on_sale=True)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    # Return a list of products that are out of stock
    @action(detail=False, methods=['get'])
    def out_of_stock(self, request):
        products = self.get_queryset().filter(quantity_in_stock=0)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
    
    # Return a list of products that are out of stock
    @action(detail=False, methods=['get'], url_path='out_of_stock_by/(?P<company_id>[^/.]+)')
    def out_of_stock_by(self, request, company_id):
        products = self.get_queryset().filter(company=company_id, quantity_in_stock=0)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
    
    # Mettre à jour la quantité en stock d'un produit
    @action(detail=True, methods=['put'])
    def update_quantity_in_stock(self, request, pk=None):
        product = self.get_object()
        new_quantity = request.data.get('quantity_in_stock', None)
        if new_quantity is None:
            return Response(
                    {'error': 'Veuillez fournir une nouvelle quantité en stock.'},
                    status=status.HTTP_400_BAD_REQUEST
                    )
        old_quantity = product.quantity_in_stock
        product.quantity_in_stock = int(new_quantity)
        product.save()
        # Mettre à jour les stocks liés au produit
        for stock in product.stock_set.all():
            stock.quantity += (product.quantity_in_stock - old_quantity)
            stock.save()
        serializer = self.get_serializer(product)
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
    
    # Réapprovisionner le stock d'un produit
    @action(detail=True, methods=['put'])
    def restock(self, request, pk=None):
        stock = self.get_object()
        quantity = request.data.get('quantity', None)
        if quantity is None:
            return Response(
                    {'error': 'Veuillez fournir une quantité pour le réapprovisionnement.'},
                    status=status.HTTP_400_BAD_REQUEST
                    )
        stock.quantity += int(quantity)  # Ajouter la nouvelle quantité à la quantité existante
        stock.save()
        
        # Mettre à jour la quantité en stock du produit
        product = stock.product
        product.update_quantity_in_stock(stock.quantity)
        
        # Mettre à jour le statut du stock
        self.update_status(request, pk=pk)
        
        serializer = self.get_serializer(stock)
        return Response(serializer.data)

    
    # Mettre à jour le statut du stock
    @action(detail=True, methods=['put'])
    def update_status(self, request, pk=None):
        stock = self.get_object()
        status_fields = ['in_transit', 'on_delivery', 'on_reorder', 'on_return']
        for field in status_fields:
            field_value = request.data.get(field, None)
            if field_value is not None:
                setattr(stock, field, field_value)
        stock.save()
        serializer = self.get_serializer(stock)
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
    user = request.user

    # Vue d'ensemble des produits les plus vendus avec leurs quantités disponibles dans les différents entrepôts.
    #products = Product.objects.filter(company__created_by=user).annotate(total_quantity=Sum('stock__quantity')).order_by('-total_quantity')[:5]
    # Récupérer les 5 produits les plus vendus par la compagnie de l'utilisateur
    products = Product.objects.filter(company__created_by=user).annotate(total_quantity=Sum('stock__quantity')).order_by('-total_quantity')[:5]
    top_5_products = sorted(products, key=lambda p: p.total_quantity, reverse=True)[:5] 

    # Récupérer les stocks de chaque produit dans les entrepôts de la compagnie de l'utilisateur
    stock_data = []
    for product in top_5_products:
        for warehouse in user.created_companies.first().warehouses.all():
            stock = Stock.objects.filter(product=product, warehouse=warehouse).first()
            if stock:
                stock_data.append({'product_name': product.name, 'warehouse_name': warehouse.name, 'quantity': stock.quantity})


    # Vue d'ensemble des seuils de stock pour les différents produits.
    thresholds = Threshold.objects.filter(company__created_by=user).order_by('-value')[:5]


    # Vue d'ensemble des commandes en cours, des commandes en attente et des commandes livrées.
    orders = user.company.orders.all()
    orders_pending = orders.filter(status='Pending')
    orders_delivered = orders.filter(status='Delivered')

    # Vue d'ensemble des entrepôts de l'entreprise avec les quantités de produits stockées dans chacun d'entre eux.
    warehouses = user.company.warehouses.all()
    stocks = Stock.objects.filter(warehouse__in=warehouses).values('warehouse__name', 'product__name').annotate(total_quantity=Sum('quantity'))
    warehouse_stock = {}
    for stock in stocks:
        if stock['warehouse__name'] not in warehouse_stock:
            warehouse_stock[stock['warehouse__name']] = {}
        warehouse_stock[stock['warehouse__name']][stock['product__name']] = stock['total_quantity']

    # Vue d'ensemble des produits en rupture de stock ou bientôt en rupture de stock.
    out_of_stock = Product.objects.filter(company=user.company, quantity_in_stock=0)
    low_stock = Product.objects.filter(company=user.company, quantity_in_stock__lt=F('minimum_quantity') + 10)
    
    # Vue d'ensemble des produits en promotion ou en soldes.
    on_sale = Product.objects.filter(company=user.company, on_sale=True)
    on_clearance = Product.objects.filter(company=user.company, on_clearance=True)

    # Vue d'ensemble des activités récentes de l'utilisateur sur la plateforme.
    recent_activities = user.company.recent_activities.all()[:5]

    # Formulaire de recherche de produits.
    search_query = request.GET.get('q')
    if search_query:
        products = products.filter(Q(name__icontains=search_query) | Q(barcode__icontains=search_query) | Q(category__icontains=search_query))

    context = {
        'products': products,
        'product_stock': stock_data,
        'thresholds': thresholds,
        'orders_pending': orders_pending,
        'orders_delivered': orders_delivered,
        'warehouse_stock': warehouse_stock,
        'out_of_stock': out_of_stock,
        'low_stock': low_stock,
        'on_sale': on_sale,
        'on_clearance': on_clearance,
        'recent_activities': recent_activities,
        'search_query': search_query,
    }

    return render(request, 'dashboard.html', context)  


@login_required
def stock_list(request):
    stocks = Stock.objects.all()
    paginator = Paginator(stocks, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'stock_list.html', {'page_obj': page_obj})

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


def my_custom_view(request):
    link = reverse('home')
    return link