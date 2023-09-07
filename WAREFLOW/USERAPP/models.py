from django.db import models

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name
    
class Subcategory(models.Model):
    subcategory_id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory_name = models.CharField(max_length=100)

    def __str__(self):
        return self.subcategory_name


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    buying_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    unit = models.CharField(max_length=50)
    expiry_date = models.DateField()
    threshold_value = models.PositiveIntegerField()
    product_image = models.ImageField(upload_to='product_images/')  # Add this field

    def __str__(self):
        return self.product_name