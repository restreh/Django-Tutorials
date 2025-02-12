from django.shortcuts import render
from django.views.generic import TemplateView
from django.views import View
from django import forms 
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse


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

class Product: 
    products = [ 
        {"id":"1", "name":"TV", "description":"Best TV","price":200}, 
        {"id":"2", "name":"iPhone", "description":"Best iPhone","price":5000}, 
        {"id":"3", "name":"Chromecast", "description":"Best Chromecast","price":90}, 
        {"id":"4", "name":"Glasses", "description":"Best Glasses","price":75} 
    ] 
 
class ProductIndexView(View): 
    template_name = 'products/index.html' 
 
    def get(self, request): 
        viewData = {} 
        viewData["title"] = "Products - Online Store" 
        viewData["subtitle"] =  "List of products" 
        viewData["products"] = Product.products 
 
        return render(request, self.template_name, viewData) 
 
class ProductShowView(View): 
    template_name = 'products/show.html' 
 
 
    def get(self, request, id):
        try:
            product_index = int(id) - 1
        except ValueError:
            return HttpResponseRedirect(reverse("home"))

        if product_index < 0 or product_index >= len(Product.products):
            return HttpResponseRedirect(reverse("home"))

        product = Product.products[product_index]

        viewData = {
            "title": f'{product["name"]} - Online Store',
            "subtitle": f'{product["name"]} - Product information',
            "product": product,
        }

        return render(request, self.template_name, viewData)

class ProductForm(forms.Form): 
    name = forms.CharField(required=True) 
    price = forms.FloatField(required=True) 

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is None or price <= 0:
            raise forms.ValidationError("El precio debe ser mayor que cero")
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