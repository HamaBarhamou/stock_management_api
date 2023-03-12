from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import CategoriesSerializer, ProductSerializer, StockSerializer
from django.views.decorators.csrf import csrf_exempt
from .models import Categories, Product, Stock, Threshold
from rest_framework.parsers import JSONParser
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from rest_framework.decorators import action
from rest_framework.response import Response


class categorieslistViewSet(viewsets.ModelViewSet):
    """
    Viewset pour la gestion des catégories.
    """
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    #permission_classes = [permissions.IsAuthenticated]

    """ @extend_schema(
        description='Displays the list of categories',
        # attach request/response examples to the operation.
        examples=[
            OpenApiExample(
                'Example 1',
                description='Returns a list of categories',
                value=[
                    {
                        "name": "Ordinateurs Portables"
                    },
                    {
                        "name": "Accesoire de portables"
                    },
                    {
                        "name": "Consommable Bureautique"
                    }
                ]
            ),
            OpenApiExample(
                'Example 2',
                description='Returns empty list',
                value=[]
            )
        ],

        request=OpenApiParameter(
            name='my_custom_parameter',
            description='Custom parameter description',
            required=False,
            type=OpenApiTypes.STR
        )
    )

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs) """
    
    
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # Return a list of products that have a quantity in stock of 10 or lower
    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        threshold = get_object_or_404(Threshold, name='low_stock')
        products = self.get_queryset().filter(quantity_in_stock__lte=threshold.value)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    # Return a list of products that have a rotation of 5 or lower
    @action(detail=False, methods=['get'])
    def low_demand(self, request):
        threshold = get_object_or_404(Threshold, name='low_demand')
        products = self.get_queryset().filter(rotation__lte=threshold.value)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    # Return a list of products that have a profit margin of 0.1 or lower
    @action(detail=False, methods=['get'])
    def low_profit_margin(self, request):
        threshold = get_object_or_404(Threshold, name='low_profit_margin')
        products = self.get_queryset().filter(profit_margin__lte=threshold.value)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    # Return a list of products that have a quantity in stock of 5 or lower
    @action(detail=False, methods=['get'])
    def low_quantity(self, request):
        threshold = get_object_or_404(Threshold, name='low_quantity')
        products = self.get_queryset().filter(quantity_in_stock__lte=threshold.value)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    # Return a list of products that have a rotation of 2 or lower
    @action(detail=False, methods=['get'])
    def low_rotation(self, request):
        threshold = get_object_or_404(Threshold, name='low_rotation')
        products = self.get_queryset().filter(rotation__lte=threshold.value)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    # Return a list of products that have a rotation of 8 or higher
    @action(detail=False, methods=['get'])
    def high_demand(self, request):
        threshold = get_object_or_404(Threshold, name='high_demand')
        products = self.get_queryset().filter(rotation__gte=threshold.value)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    # Return a list of products that have a profit margin of 0.2 or higher
    @action(detail=False, methods=['get'])
    def high_profit_margin(self, request):
        threshold = get_object_or_404(Threshold, name='high_profit_margin')
        products = self.get_queryset().filter(profit_margin__gte=threshold.value)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    # Return a list of products that have a rotation of 10 or higher
    @action(detail=False, methods=['get'])
    def high_rotation(self, request):
        threshold = get_object_or_404(Threshold, name='high_rotation')
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

    @action(detail=False, methods=['get'])
    def available(self, request):
        stocks = self.get_queryset().filter(on_delivery=False, on_reorder=False, on_return=False)
        serializer = self.get_serializer(stocks, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def on_delivery(self, request):
        stocks = self.get_queryset().filter(on_delivery=True)
        serializer = self.get_serializer(stocks, many=True)
