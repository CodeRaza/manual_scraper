# views.py
from rest_framework import viewsets
from .models import Brand, Category, ProductType, ProductModel, ProductModelDocumentTypeDocs
from .serializers import BrandSerializer, CategorySerializer, ProductTypeSerializer, ProductModelSerializer, ProductModelDocumentTypeDocsSerializer

class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductTypeViewSet(viewsets.ModelViewSet):
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer

class ProductModelViewSet(viewsets.ModelViewSet):
    queryset = ProductModel.objects.all()
    serializer_class = ProductModelSerializer

class ProductModelDocumentTypeDocsViewSet(viewsets.ModelViewSet):
    queryset = ProductModelDocumentTypeDocs.objects.all()
    serializer_class = ProductModelDocumentTypeDocsSerializer
