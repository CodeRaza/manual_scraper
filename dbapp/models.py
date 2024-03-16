from django.db import models

class Brand(models.Model):
    name = models.CharField(max_length=1000)
    link = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.link}"

class Category(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="category")
    name = models.CharField(max_length=100, null=True, blank=True)
    link = models.CharField(max_length=1000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.brand.name} - {self.name}"


class ProductType(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="product_type")
    name = models.CharField(max_length=100, null=True, blank=True)
    # link = models.CharField(max_length=1000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.brand.name} - {self.name}"

class ProductModel(models.Model):
    product = models.ForeignKey(ProductType, on_delete=models.CASCADE, related_name="product_models")
    model = models.CharField(max_length=100, null=True, blank=True)
    # link = models.CharField(max_length=1000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name}"

class ProductModelDocumentTypeDocs(models.Model):
    model = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name="document_type")
    name = models.CharField(max_length=100, null=True, blank=True)
    doc_link = models.CharField(max_length=1000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"


class Article(models.Model):
    doc = models.OneToOneField('ProductModelDocumentTypeDocs', related_name='doc_article', on_delete=models.CASCADE)
    table_content = models.TextField()
    title = models.CharField(max_length=5000, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    pdf_file = models.FileField(upload_to='pdfs/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title}"
