from django.shortcuts import render
from .forms import ContactForm
from .utilities import feedback_email_send
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            feedback_email_send(request, form)
            return HttpResponseRedirect(request.build_absolute_uri(reverse_lazy('base')))
    form = ContactForm()
    return render(request, "contact_form.html", {'form': form})
