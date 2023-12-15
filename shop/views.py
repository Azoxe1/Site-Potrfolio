from django.db.models.aggregates import Avg
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse_lazy
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from .serializers import *
from rest_framework import status

from .forms import *
from .models import *

User = settings.AUTH_USER_MODEL


def projects(request):
    project = Projects.objects.all()
    context = {
        'project': project

    }
    return render(request, 'project_page_2.html', context)


class ProjectsView(ListAPIView):
    queryset = Projects.objects.all()
    serializer_class = ProjectsSerializer


def base(request):
    return render(request, 'base_page.html', )


def index(request):
    products = Product.objects.filter(feachured=True, product_status="опубликовано").order_by('-id')
    context = {
        "products": products
    }

    return render(request, 'shop/index.html', context)


def product_list_view(request, title):
    category = Category.objects.get(title=title)
    products = Product.objects.filter(product_status="опубликовано", category=category)
    context = {
        'category': category,
        'products': products,

    }
    return render(request, 'shop/index.html', context)


def category_list(request):
    category = Category.objects.all().order_by('-id')
    cat_form = CategoryForm()
    context = {
        "category": category,
        'cat_form': cat_form
    }

    return render(request, 'shop/category.html', context)


def product_view(request, title):
    one_prod = Product.objects.get(title=title)
    product = Product.objects.filter(title=title)
    reviews = ProductReview.objects.filter(product=one_prod)
    average_rating = ProductReview.objects.filter(product=one_prod).aggregate(rating=Avg('rating'))
    review = ProductReviewForm()
    context = {
        'product': product,
        'reviews': reviews,
        'average_rating': average_rating,
        'review': review

    }
    return render(request, 'shop/product_2.html', context)


def add_review(request, title):
    product = Product.objects.get(title=title)
    user = request.user
    if request.method == "POST":
        form = ProductReviewForm(request.POST)
        if form.is_valid():
            review_post = ProductReview.objects.create(
                product=product,
                user=user,
                review=form.cleaned_data['review'],
                rating=form.cleaned_data['rating']
            )
            review_post.save()
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

    context = {
        'user': user.username,
        'review': request.POST.get('review'),
        'rating': request.POST.get('rating'),
    }
    average_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg("rating"))

    return render(request, 'shop/product.html', context)


def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES)
        y = request.POST.get('image')
        print(y)
        if form.is_valid():
            cat_post = Category.objects.create(
                title=form.cleaned_data['title'],
                image=form.cleaned_data['image']

            )
            cat_post.save()
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        else:
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
