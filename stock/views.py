from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import UserSerializer, GroupSerializer
from .serializers import CategoriesSerializer, ProductSerializer
from django.views.decorators.csrf import csrf_exempt
from .models import Categories
from rest_framework.parsers import JSONParser

    
class categorieslistViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    #permission_classes = [permissions.IsAuthenticated]
