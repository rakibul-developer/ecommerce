from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q

from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from django.http import Http404


# Create your views here.
class LatestProductsList(APIView):
    def get(self, request, format=None):
        products = Product.objects.all()[0:4]
        serializer = ProductSerializer(
            products,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)


class ProductDetail(APIView):
    def get_object(self, category_slug, product_slug):
        try:
            return Product.objects.filter(
                category__slug=category_slug
            ).get(slug=product_slug)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, category_slug, product_slug, format=None):
        product = self.get_object(category_slug, product_slug)
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data)


class CategoryDetail(APIView):
    def get_object(self, category_slug):
        try:
            return Category.objects.get(slug=category_slug)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, category_slug, format=None):
        category = self.get_object(category_slug)
        serializer = CategorySerializer(category, context={'request': request})
        return Response(serializer.data)


class ProductSearchView(APIView):
    def post(self, request, *args, **kwargs):
        query = request.data.get('query', '')

        if query:
            products = Product.objects.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )
            serializer = ProductSerializer(
                products,
                context={'request': request},
                many=True
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"products": []}, status=status.HTTP_200_OK)
