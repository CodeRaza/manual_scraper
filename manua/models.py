from django.db import models

class Brand(models.Model):
    title = models.CharField(max_length=1000, blank=True, null=True)
    link = models.CharField(max_length=2000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or ''

class Product(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')
    title = models.CharField(max_length=1000, blank=True, null=True)
    link = models.CharField(max_length=2000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or ''

class Manual(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='manuals')
    title = models.CharField(max_length=1000, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    pdf = models.FileField(upload_to='manuals/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or ''
