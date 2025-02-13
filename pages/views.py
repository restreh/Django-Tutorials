from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.views import View
from django import forms 
from django.shortcuts import render, redirect,  get_object_or_404 
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Product 


class HomePageView(TemplateView):
    template_name = 'pages/home.html'

class AboutPageView(TemplateView):
    template_name = 'pages/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "About us - Online Store",
            "subtitle" : "About us",
            "description": "This is an about page...",
            "author" : "Developed by: Juan José Restrepo Higuita",
        })

        return context

class ContactPageView(TemplateView):
    template_name= 'pages/contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "email": "onlinestore@email.com",
            "adress" : "Street 1 #2-3 AB",
            "phone": "1234567890",
        })

        return context
 
class ProductIndexView(View): 
    template_name = 'products/index.html' 
 
    def get(self, request): 
        viewData = {} 
        viewData["title"] = "Products - Online Store" 
        viewData["subtitle"] =  "List of products" 
        viewData["products"] = Product.objects.all()
 
        return render(request, self.template_name, viewData) 
 
class ProductShowView(View): 
    template_name = 'products/show.html' 
 
 
    def get(self, request, id):
        try:
            product_id = int(id)
            if product_id < 1:
                raise ValueError("Product ID must be 1 or greater")
        except (ValueError, IndexError):
            return HttpResponseRedirect(reverse("home"))


        product = get_object_or_404(Product, pk=product_id) 
        viewData = {
            "title": f'{product.name} - Online Store',
            "subtitle": f'{product.name} - Product information',
            "product": product,
        }

        return render(request, self.template_name, viewData)
    
class ProductListView(ListView): 
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'
 
    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs) 
        context['title'] = 'Products - Online Store' 
        context['subtitle'] = 'List of products' 
        return context

class ProductForm(forms.ModelForm): 
    class Meta:
        model=Product
        fields= ['name','price']

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is None or price <= 0:
            raise forms.ValidationError("Price must be greater than 0")
        return price
 
class ProductCreateView(View): 
    template_name = 'products/create.html'
    success_template = 'products/product_created.html'
 
    def get(self, request): 
        form = ProductForm() 
        viewData = {} 
        viewData["title"] = "Create product" 
        viewData["form"] = form 
        return render(request, self.template_name, viewData) 
 
    def post(self, request): 
        form = ProductForm(request.POST) 
        if form.is_valid(): 
            form.save()
            viewData = {
                "title": "Product Created",
                "message": "Product created"
            }
            return render(request, self.success_template, viewData)
        else: 
            viewData = {} 
            viewData["title"] = "Create product" 
            viewData["form"] = form 
            return render(request, self.template_name, viewData)