from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets

from main.forms import ContactForm
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
