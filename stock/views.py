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


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
    
class categorieslistViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = [permissions.IsAuthenticated]

""" @csrf_exempt
def categories_list(request):

    if request.method == 'GET':
        categories = Categories.objects.all()
        serializer = CategoriesSerializer(categories, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = CategoriesSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400) """