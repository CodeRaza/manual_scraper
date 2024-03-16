# serializers.py
from rest_framework import serializers
from .models import Brand, Category, ProductType, ProductModel, ProductModelDocumentTypeDocs

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['name', 'link', 'category', 'product_type']
        depth = 1 

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = ['brand', 'name', 'product_models', 'created_at']
        depth = 1
        
class ProductModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields = '__all__'

class ProductModelDocumentTypeDocsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModelDocumentTypeDocs
        fields = ['id', 'name', 'doc_link', 'model', 'doc_article', 'created_at']
        depth = 1
