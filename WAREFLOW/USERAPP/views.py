from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout, get_user_model
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render
from .models import Category, Product,Subcategory
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.core.serializers.json import DjangoJSONEncoder
from django.core.paginator import Paginator


def index(request):
    return render(request, 'index.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            request.session['user_id'] = user.id
            request.session['username'] = user.username
            return redirect('index')  # Replace with your desired URL
        else:
            messages.error(request, "Invalid credentials")
            return redirect('login')
    else:
        return render(request, 'login.html')

def register(request):
    if request.method == "POST":
        first_name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('pass')
        Cpassword = request.POST.get('cpass')
        
        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Exists")
            return render(request, "register.html", {'email': username})
        else:
            user = User.objects.create_user(first_name=first_name,username=username,email=email,password=password)
            user.save()
            messages.success(request, "Registration successful! Please log in.")
            return redirect('login')
    else:
        return render(request, "register.html")


def loggout(request):
    print('Logged Out')
    logout(request)
    if 'username' in request.session:
        del request.session['username']
    return redirect('login')

def check_email(request):
    email = request.GET.get('email')
    exists = User.objects.filter(email=email).exists()
    return JsonResponse({'exists': exists})

def check_username(request):
    username = request.GET.get('username')
    exists = User.objects.filter(username=username).exists()
    return JsonResponse({'exists': exists})


def notifications(request):
    return render(request, 'notifications.html')

def error(request):
    return render(request, '404.html')

def account(request):
    return render(request, 'account.html')

def charts(request):
    return render(request, 'charts.html')

def docs(request):
    return render(request, 'docs.html')

def help(request):
    return render(request, 'help.html')

def orders(request):
  categories = Category.objects.all()
  context = {'categories': categories}
  return render(request, 'orders.html', context)

def settings(request):
    return render(request, 'settings.html')


def add_product(request):
    if request.method == 'POST':
        category_id = request.POST['category']
        subcategory_id = request.POST.get('subcategory')
        category = Category.objects.get(pk=category_id)
        subcategory = Subcategory.objects.get(pk=subcategory_id)
        product_image = request.FILES['productImage']
        product_name = request.POST['productName']
        buying_price = request.POST['buyingPrice']
        quantity = request.POST['quantity']
        unit = request.POST['unit']
        expiry_date = request.POST['expiryDate']
        threshold_value = request.POST['thresholdValue']
        

        product = Product(category=category, subcategory=subcategory,product_image=product_image, product_name=product_name,
                          buying_price=buying_price, quantity=quantity, unit=unit,
                          expiry_date=expiry_date, threshold_value=threshold_value)
        product.save()

        # Redirect to a success page or wherever you want
        return redirect('list_products')  # Change 'success_page' to the actual URL


def list_products(request):
    # Assuming 'products' is a queryset of all products
    products = Product.objects.all()

    # Set the number of products per page
    products_per_page = 15

    # Create a Paginator instance
    paginator = Paginator(products, products_per_page)

    # Get the current page number from the request's GET parameters
    page_number = request.GET.get('page')

    # Get the Page object for the current page
    page = paginator.get_page(page_number)

    # Assuming 'categories' is a queryset of all categories
    categories = Category.objects.all()

    return render(request, 'orders.html', {'page': page, 'categories': categories})


def get_subcategories(request):
    category_id = request.GET.get('category_id')
    subcategories = Subcategory.objects.filter(category=category_id)
    subcategory_options = [{'id': subcategory.subcategory_id, 'name': subcategory.subcategory_name} for subcategory in subcategories]
    return JsonResponse({'subcategories': subcategory_options})


@csrf_exempt
def delete_product(request, product_id):
    try:
        product = Product.objects.get(pk=product_id)
        product.delete()
        return JsonResponse({'message': 'Product deleted successfully'})
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)
    
    
def update_product(request, product_id):
    if request.method == 'POST':
        # Get the product instance based on the product ID
        product = get_object_or_404(Product, product_id=product_id)

        # Process the form data
        product.product_name = request.POST.get('productNameupdate')
        product.category_id = request.POST.get('categoryupdate')
        product.subcategory_id = request.POST.get('subcategoryupdate')
        product.buying_price = request.POST.get('buyingPriceupdate')
        product.quantity = request.POST.get('quantityupdate')
        product.unit = request.POST.get('unitupdate')
        product.expiry_date = request.POST.get('expiryDateupdate')
        product.threshold_value = request.POST.get('thresholdValueupdate')
        
        # Check if a new product image is provided
        if request.FILES.get('productImageupdate'):
            product.product_image = request.FILES['productImageupdate']

        # Save the updated product
        product.save()

        # Return a JSON response indicating success
        return redirect('list_products')

    # Handle GET requests or other HTTP methods
    return JsonResponse({'message': 'Invalid request method'}, status=400)


def get_product_details(request, product_id):
    # Retrieve the product based on the product_id or return a 404 if not found
    product = get_object_or_404(Product, product_id=product_id)  # Use the correct field name for the primary key

    # Convert the product data into a dictionary
    product_data = {
        'product_id': product.product_id,
        'category_id': product.category_id,
        'subcategory_id': product.subcategory_id,
        'product_name': product.product_name,
        'buying_price': product.buying_price,
        'quantity': product.quantity,
        'unit': product.unit,
        'expiry_date': product.expiry_date.strftime('%Y-%m-%d'),  # Format date as string
        'threshold_value': product.threshold_value,
        # Add other product fields as needed
    }

    # Return the product data as JSON response
    return JsonResponse(product_data)