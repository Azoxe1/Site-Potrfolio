from importlib.abc import Loader

from cfgv import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.core.validators import URLValidator
from django.http import JsonResponse
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, OpenApiResponse, inline_serializer
from drf_spectacular.types import OpenApiTypes
from distutils.util import strtobool
from rest_framework.request import Request
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from yaml import load as load_yaml, Loader
from rest_framework import serializers as s
from .models import *
from rest_framework.throttling import UserRateThrottle
from .serializers import *
from django.db import IntegrityError
from django.db.models import Q, Sum, F
from django.http import JsonResponse
from requests import get
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from yaml import load as load_yaml

from .signals import new_order


class ProductsView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CategoriesView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProjectsView(ListAPIView):
    queryset = Projects.objects.all()
    serializer_class = ProjectsSerializer


class ContactView(APIView):
    throttle_classes = [UserRateThrottle]

    @extend_schema(
        description='Get a list of contact information',
        operation_id='Create_Saved_Search',
        parameters=[
            OpenApiParameter('contact_title', type=OpenApiTypes.STR,
                             required=True, description='Enter contact title'),
        ],
        responses={
            (200, 'application/json'): OpenApiResponse(
                description='Success',
                response=inline_serializer(
                    name='saved_search_list',
                    fields={
                        'city': s.CharField(),
                        "street": s.CharField(),
                        "house": s.CharField(),
                        "structure": s.CharField(),
                        "building": s.CharField(),
                        'apartment': s.CharField(),

                    },
                )
            )
        }
    )
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)
        contact = Contact.objects.filter(
            user_id=request.user.id)
        serializer = ContactSerializer(contact, many=True)
        return Response(serializer.data)

    @extend_schema(
        description='Post a new contact',
        operation_id='Post_Saved_Search',
        request=ContactSerializer,
        responses={
            (201, 'application/json'): OpenApiResponse(description='Ok'),
            404: OpenApiResponse(description='User does not exist')}
    )
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)
        if {'city', 'street', 'phone'}.issubset(request.data):
            request.data._mutable = True
            request.data.update({'user': request.user.id})
            serializer = ContactSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'Status': True})
            else:
                return JsonResponse({'Status': False, 'Errors': serializer.errors})
        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})

    @extend_schema(
        description='Update contact',
        operation_id='Put_Saved_Search',
        parameters=[
            OpenApiParameter('contact_id', type=OpenApiTypes.STR, description='Enter a contact id',
                             location=OpenApiParameter.QUERY),
            OpenApiParameter('contact_value', type=OpenApiTypes.STR, description='Enter a new contact value',
                             location=OpenApiParameter.QUERY)
        ],
        responses={
            (201, 'application/json'): OpenApiResponse(description='Ok'),
            404: OpenApiResponse(description='Contact does not exist')}
    )
    def put(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)
        if 'id' in request.data:
            if request.data['id'].isdigit():
                contact = Contact.objects.filter(id=request.data['id'], user_id=request.user.id).first()
                print(contact)
                if contact:
                    serializer = ContactSerializer(contact, data=request.data, partial=True)
                    if serializer.is_valid():
                        serializer.save()
                        return JsonResponse({'Status': True})
                    else:
                        return JsonResponse({'Status': False, 'Errors': serializer.errors})
        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})


class OrderView(APIView):
    throttle_classes = [UserRateThrottle]

    @extend_schema(
        description='Сreating a saved search',
        operation_id='Create_Saved_Search',
        parameters=[
            OpenApiParameter('vacancy_name', type=OpenApiTypes.STR, description='Enter a vacancy_name',
                             location=OpenApiParameter.QUERY)],

        responses={
            (201, 'application/json'): OpenApiResponse(description='Saved search successfully created'),
            400: OpenApiResponse(description='No vacancy name'),
            401: OpenApiResponse(description='Incorrect authentication credentials.'),
            403: OpenApiResponse(description="Credentials weren't provided"),
            404: OpenApiResponse(description='The token/User does not exist'),
        }
    )
    def get(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)
        order = Order.objects.filter(user_id=request.user.id)
        serializer = OrderSerializer(order, many=True)
        return Response(serializer.data)

    @extend_schema(
        description='Сreating a saved search',
        operation_id='Create_Saved_Search',
        parameters=[
            OpenApiParameter('vacancy_name', type=OpenApiTypes.STR, description='Enter a vacancy_name',
                             location=OpenApiParameter.QUERY)],

        responses={
            (200, 'application/json'): OpenApiResponse(description='ok'),
            401: OpenApiResponse(description='Incorrect authentication credentials.'),
            404: OpenApiResponse(description='The token/User does not exist'),
        }
    )
    def post(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)
        if {'id', 'contact'}.issubset(request.data):
            if request.data['id'].isdigit():
                try:
                    is_updated = Order.objects.filter(
                        user_id=request.user.id, id=request.data['id']).update(
                        contact_id=request.data['contact'],
                        state='new')
                except IntegrityError as error:
                    print(error)
                    return JsonResponse({'Status': False, 'Errors': 'Неправильно указаны аргументы'})
                else:
                    if is_updated:
                        new_order.send(sender=self.__class__, user_id=request.user.id)
                        return JsonResponse({'Status': True})
        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})


class CartView(APIView):
    throttle_classes = [UserRateThrottle]

    @extend_schema(
        description='Watch Cart',
        operation_id='watch_cart',
        responses={
            (200, 'application/json'): OpenApiResponse(
                description='Success',
                response=inline_serializer(
                    name='watch_cart',
                    fields={
                        'ordered_items': s.ListField(),
                        "product_name": s.CharField(),
                        "quantity": s.CharField(),

                    },
                )
            )
        }
    )
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)
        basket = Order.objects.filter(
            user_id=request.user.id, state='cart')
        serializer = OrderSerializer(basket, many=True)
        return Response(serializer.data)

    @extend_schema(
        description='Add to cart',
        operation_id='Add_to_cart',
        parameters=[
            OpenApiParameter('product_name', type=OpenApiTypes.INT, description='select product id',
                             location=OpenApiParameter.QUERY),
            OpenApiParameter('quantity', type=OpenApiTypes.INT, description='select quantity',
                             location=OpenApiParameter.QUERY),
        ],

        responses={
            (200, 'application/json'): OpenApiResponse(description='ok'),
            401: OpenApiResponse(description='Incorrect authentication credentials.'),
            404: OpenApiResponse(description='The token/User does not exist'),
        }
    )
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)
        items_sting = request.data.get('items')
        if items_sting:
            try:
                items_dict = load_json(items_sting)
            except ValueError:
                return JsonResponse({'Status': False, 'Errors': 'Неверный формат запроса'})
            else:
                cart, _ = Order.objects.get_or_create(user_id=request.user.id, state='cart')
                objects_created = 0
                for order_item in items_dict:
                    order_item.update({'order': cart.id})
                    serializer = OrderItemSerializer(data=order_item)
                    if serializer.is_valid():
                        try:
                            serializer.save()
                        except IntegrityError as error:
                            return JsonResponse({'Status': False, 'Errors': str(error)})
                        else:
                            objects_created += 1
                    else:
                        return JsonResponse({'Status': False, 'Errors': serializer.errors})
                return JsonResponse({'Status': True, 'Создано объектов': objects_created})
        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})

    @extend_schema(
        description='Put cart',
        operation_id='Put_cart',
        parameters=[
            OpenApiParameter('product', type=OpenApiTypes.INT, description='select product id',
                             location=OpenApiParameter.QUERY),
            OpenApiParameter('quantity', type=OpenApiTypes.INT, description='select quantity',
                             location=OpenApiParameter.QUERY),
        ],

        responses={
            (200, 'application/json'): OpenApiResponse(description='ok'),
            401: OpenApiResponse(description='Incorrect authentication credentials.'),
            404: OpenApiResponse(description='The token/User does not exist'),
        }
    )
    def put(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)
        items_sting = request.data.get('items')
        if items_sting:
            try:
                items_dict = load_json(items_sting)
            except ValueError:
                return JsonResponse({'Status': False, 'Errors': 'Неверный формат запроса'})
            else:
                basket, _ = Order.objects.get_or_create(user_id=request.user.id, state='cart')
                for order_item in items_dict:
                    OrderItem.objects.filter(order_id=basket.id, product_name=order_item['product']).update(
                        quantity=order_item['quantity'])
                return JsonResponse({'Status': True})
        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})

    @extend_schema(
        description='Delete product cart',
        operation_id='Delete_from_cart',
        parameters=[
            OpenApiParameter('product', type=OpenApiTypes.INT, description='select product id',
                             location=OpenApiParameter.QUERY),
        ],

        responses={
            (200, 'application/json'): OpenApiResponse(description='ok'),
            401: OpenApiResponse(description='Incorrect authentication credentials.'),
            404: OpenApiResponse(description='The token/User does not exist'),
        }
    )
    def delete(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)
        items_sting = request.data.get('items')
        if items_sting:
            items_list = items_sting.split(',')
            basket, _ = Order.objects.get_or_create(user_id=request.user.id, state='basket')
            for order_item_id in items_list:
                if order_item_id.isdigit():
                    OrderItem.objects.filter(product_id=order_item_id, order_id=basket.id).delete()
                    return JsonResponse({'Status': True, 'Удалено': True})
        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})
