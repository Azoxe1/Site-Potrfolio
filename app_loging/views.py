from audioop import reverse

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.authtoken.models import Token

from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.conf import settings
from django.urls import reverse_lazy
from rest_framework.request import Request

from .forms import RegistrationForm
from .models import *
from .serializers import UserSerializer


class RegisterUser(CreateView):
    form_class = RegistrationForm
    template_name = 'auth/register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, f"Аккаунт {form.cleaned_data.get('username')} успешно зарегестрирован.")
        return redirect('base')


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'auth/login.html'

    def get_success_url(self):
        return reverse_lazy('base')


# def loginview(request, *args, **kwargs):
#     if request.user.is_authenticated:
#         return redirect('base')
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#
#         try:
#             user = User.objects.get(email=email)
#         except:
#             messages.warning(request, f'Пользователь с почтой {email} не существует')
#
#         user = authenticate(request, email=email, password=password)
#         if user is not None:
#             login(request, user)
#             messages.success(request, 'Успех')
#             return redirect('base')
#         else:
#             messages.warning(request, 'Пользователь не существует')
#     return render(request, 'auth/login.html')


def logout_user(request):
    logout(request)
    return redirect('base')


def lk(request):
    return render(request, 'auth/lk.html', )


class RegisterAccount(APIView):

    def post(self, request, *args, **kwargs):
        if {'username', 'email', 'password', 'title', 'type'}.issubset(request.data):
            sad = 'asd'
            try:
                validate_password(request.data['password'])
            except Exception as password_error:
                error_array = []
                for item in password_error:
                    error_array.append(item)
                return JsonResponse({'Status': False, 'Errors': {'password': error_array}})
            else:
                user_serializer = UserSerializer(data=request.data)
                if user_serializer.is_valid():
                    user = user_serializer.save()
                    user.set_password(request.data['password'])
                    user.save()
                    return JsonResponse({'Status': True})
                else:
                    return JsonResponse({'Status': False, 'Errors': user_serializer.errors})
        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})


class ConfirmAccount(APIView):

    def post(self, request, *args, **kwargs):
        if {'email', 'token'}.issubset(request.data):
            token = ConfirmEmailToken.objects.filter(user__email=request.data['email'],
                                                     key=request.data['token']).first()
            if token:
                token.user.is_active = True
                token.user.save()
                token.delete()
                return JsonResponse({'Status': True})
            else:
                return JsonResponse({'Status': False, 'Errors': 'Неправильно указан токен или email'})

        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})


class AccountDetails(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request: Request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)
        if 'password' in request.data:
            errors = {}
            try:
                validate_password(request.data['password'])
            except Exception as password_error:
                error_array = []
                for item in password_error:
                    error_array.append(item)
                return JsonResponse({'Status': False, 'Errors': {'password': error_array}})
            else:
                request.user.set_password(request.data['password'])
        user_serializer = UserSerializer(request.user, data=request.data, partial=True)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse({'Status': True})
        else:
            return JsonResponse({'Status': False, 'Errors': user_serializer.errors})


class LoginAccount(APIView):

    def post(self, request, *args, **kwargs):
        if {'email', 'password'}.issubset(request.data):
            user = authenticate(request, username=request.data['email'], password=request.data['password'])
            if user is not None:
                if user.is_active:
                    token, _ = Token.objects.get_or_create(user=user)
                    return JsonResponse({'Status': True, 'Token': token.key})
            return JsonResponse({'Status': False, 'Errors': 'Не удалось авторизовать'})
        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})
