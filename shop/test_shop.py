import unittest
from django.test import RequestFactory
from django.urls import reverse
from .models import Projects, Vendor, Product, Category, ProductReview
from .forms import CategoryForm, ProductReviewForm
from .views import projects, base, index, product_list_view, category_list, product_view, add_review
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio.test_settings')

class ViewsTestCase(unittest.TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_projects(self):
        request = self.factory.get(reverse('projects'))
        response = projects(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'project_page_2.html')

    def test_base(self):
        request = self.factory.get(reverse('base'))
        response = base(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base_page.html')

    def test_index(self):
        request = self.factory.get(reverse('index'))
        response = index(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/index.html')

    def test_product_list_view(self):
        category = Category.objects.create(title='Test Category')
        request = self.factory.get(reverse('product_list_view', args=[category.title]))
        response = product_list_view(request, category.title)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/index.html')

    def test_category_list(self):
        request = self.factory.get(reverse('category_list'))
        response = category_list(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/category.html')

    def test_product_view(self):
        product = Product.objects.create(title='Test Product')
        request = self.factory.get(reverse('product_view', args=[product.title]))
        response = product_view(request, product.title)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/product_2.html')

    def test_add_review(self):
        product = Product.objects.create(title='Test Product')
        request = self.factory.post(reverse('add_review', args=[product.title]), {
            'review': 'Test Review',
            'rating': 5
        })
        response = add_review(request, product.title)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('product_view', args=[product.title]))


if __name__ == '__main__':
    unittest.main()
