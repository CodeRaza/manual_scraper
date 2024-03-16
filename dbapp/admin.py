# myapp/admin.py
from django.contrib import admin
from .models import Brand, Category, ProductModel, ProductModelDocumentTypeDocs, ProductType

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'link', 'created_at')
    search_fields = ('name', 'link')
    list_filter = ('created_at',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('brand', 'name', 'link', 'created_at')
    search_fields = ('brand__name', 'name', 'link')
    list_filter = ('created_at', 'brand__name')


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('brand', 'name', 'created_at')
    search_fields = ('brand__name', 'name')
    list_filter = ('created_at', 'brand__name')

@admin.register(ProductModel)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ('product', 'model', 'created_at')
    search_fields = ('product__brand__name', 'model')
    list_filter = ('created_at', 'product__brand__name')

@admin.register(ProductModelDocumentTypeDocs)
class ProductModelDocumentTypeDocsAdmin(admin.ModelAdmin):
    list_display = ('model', 'name', 'doc_link', 'created_at')
    search_fields = ('model__product__brand__name', 'model__model', 'name', 'doc_link')
    list_filter = ('created_at', 'model__product__brand__name', 'model__model')
    
    
from .models import Article

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'pdf_file') 
    search_fields = ('title', )  

admin.site.register(Article, ArticleAdmin)
