from django import forms
from .models import Product,Category

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'category',  # This field should be a ModelChoiceField for selecting a category
            'product_name',
            'buying_price',
            'quantity',
            'unit',
            'expiry_date',
            'threshold_value',
            'product_image',
        ]

    # Add a custom constructor to set the queryset for the 'category' field
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()  # Replace 'Category' with your actual Category model


        categories = Category.objects.all()
        category_choices = [(category.category_id, category.category_name) for category in categories]
        self.fields['category'] = forms.ChoiceField(choices=category_choices)


class ProductSearchForm(forms.Form):
    search_query = forms.CharField(max_length=255, required=False)
