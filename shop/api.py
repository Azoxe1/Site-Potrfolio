from django.contrib.auth.password_validation import validate_password
from django.http import JsonResponse
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from drf_spectacular.utils import (
    OpenApiParameter, OpenApiResponse, extend_schema, inline_serializer,
)
from rest_framework import serializers as s
from .models import *
from .serializers import *
from app_loging.serializers import UserSerializer, ConfirmEmailToken




class ProductsView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CategoriesView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProjectsView(ListAPIView):
    queryset = Projects.objects.all()
    serializer_class = ProjectsSerializer
