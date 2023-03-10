""" from django.urls import path
from stock import views

urlpatterns = [
    path('categories', views.categorieslistViewSet.as_view()),
] """