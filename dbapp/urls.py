# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BrandViewSet, CategoryViewSet, ProductTypeViewSet, ProductModelViewSet, ProductModelDocumentTypeDocsViewSet

router = DefaultRouter()
router.register(r'brands', BrandViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'product-types', ProductTypeViewSet)
router.register(r'product-models', ProductModelViewSet)
router.register(r'document-types', ProductModelDocumentTypeDocsViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
