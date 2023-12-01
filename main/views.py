from audioop import reverse

from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets

from main.forms import ContactForm, RegistrationForm
from main.utilities import feedback_email_send
from django.http import HttpResponseRedirect

from django.urls import reverse_lazy


def projects(request):
    return render(request, 'projects_page.html', )


def base(request):
    return render(request, 'base_page.html', )


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            feedback_email_send(request, form)
            return HttpResponseRedirect(request.build_absolute_uri(reverse_lazy('base')))
    form = ContactForm()
    return render(request, "contact_form.html", {'form': form})


class RegisterUser(CreateView):
    form_class = RegistrationForm
    template_name = 'auth/register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('base')


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'auth/login.html'

    def get_success_url(self):
        return reverse_lazy('base')


def logout_user(request):
    logout(request)
    return redirect('base')

def lk(request):
    return render(request, 'auth/lk.html', )