
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate ,login as auth_login,logout
from django.contrib import messages
from django.http import JsonResponse,HttpResponseNotFound
from django.shortcuts import render,get_object_or_404
from django.core.mail import send_mail
from . models import *
from django.contrib.auth.decorators import *
from django.views.decorators.cache import *
import razorpay
import json
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .forms import  UserForm, UserProfileForm
from django.core.exceptions import ObjectDoesNotExist
from firstapp.models import Thread

#from django.contrib.auth.models import User

def index(request):
    # if request.user.is_authenticated:
     return render(request, 'index.html')

def header(request):
    # if request.user.is_authenticated:
     return render(request, 'header.html')


 

def register_user(request):
    if request.method == "POST":
        username=request.POST.get('email')
        fullName = request.POST.get('fullName') 
        #lname = request.POST.get('lastname')
        password = request.POST.get('password')
        confirmPassword = request.POST.get('confirmPassword')
        phone = request.POST.get('phone')
        #address = request.POST.get('address')
        email = request.POST.get('email')

        
        

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
        elif password != confirmPassword:
            messages.error(request, "Passwords do not match")
        else:
            user = CustomUser(fullName=fullName,username=username, email=email,phone=phone, user_types='2')  # Change role as needed
            user.set_password(password)
            user.save()
            messages.success
            (request, "Registered successfully")
            return redirect("login")
        # if form.is_valid():
        #     try:
        #         form.save()
        #         # Redirect to a success page or login page
        #         return redirect('login')
        #     except IntegrityError:
        #         # Handle the case where a duplicate username is entered
        #         form.add_error('username', 'This username is already taken.')
        # else:
        #     form = SignupForm()
    return render(request, "register.html")


def login_user(request):
    if 'username' in request.session:
        return redirect('/')
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        # if user is not None:
        #     auth_login(request, user)
        #     return redirect('/userhome')
        # else:
        #    messages.success(request,("Invalid credentials."))
        # print(username)  # Print the email for debugging
        # print(password)  # Print the password for debugging


        if username and password:
            user = authenticate(request, username =username , password=password)

            if user is not None:
                auth_login(request,user)
                
                
            
                if request.user.user_types==CustomUser.CUSTOMER:
                    request.session["username"]=user.username
                    return redirect('userhome')
                # elif request.user.user_typ == CustomUser.VENDOR:
                #     print("user is therapist")
                #     return redirect(reverse('therapist'))
       
                
                elif request.user.user_types == CustomUser.ADMIN:
                    print("user is admin")                   
                    return redirect('adminpanel')
                # else:
                #     print("user is normal")
                #     return redirect('')

            else:
                messages.success(request,("Invalid credentials."))
                
        else:
            messages.success(request,("Please fill out all fields."))
        
    return render(request, 'login.html')

# def product_grid(request):
#     products = Product.objects.all()  # Fetch all products
#     return render(request, 'product.html', {'products': products})

@never_cache
@login_required(login_url='login')
def adminpanel(request):
    return render(request, 'adminpanel.html')

def logout_user(request):
    # if request.user.is_authenticated:
    # if 'username' in request.session:
    #     request.session.flush()
    logout(request)
    messages.success(request,("logged out"))
    return render(request, 'index.html')

# def logout_page(request):
#     return render(request, 'logout.html')


@never_cache
@login_required(login_url='login')
def Customer_Profile(request):
    # Ensure that the user is authenticated
    if not request.user.is_authenticated:
        # Handle the case where the user is not authenticated, e.g., redirect to the login page.
        return redirect('login')  # Replace 'login' with the name of your login view.

    # Get or create the user's profile
    user_profile, created = Profile.objects.get_or_create(customer=request.user)

    if request.method == 'POST':
        # Handle the POST request for updating user profile fields
        FullName = request.POST.get('fullName')
        gender = request.POST.get('gender')
        
        #gender = request.POST['gender']
        date_of_birth = request.POST.get('date_of_birth')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        # Update the user profile fields
        user_profile.fullName = FullName
        if gender is not None:
            user_profile.gender = gender
        #user_profile.gender = gender
        user_profile.date_of_birth = date_of_birth
        if email is not None:
           user_profile.email = email
        #user_profile.email = email
        user_profile.phone= phone
        user_profile.save()

        messages.success(request, 'Profile updated successfully')  # Display a success message
        return redirect('Customer_Profile')  # Redirect to the same page or another page after update

    # Handle the GET request for displaying the user profile form
    context = {
        'user_profile': user_profile,
        'form_submitted': False,
        'date_of_birth': user_profile.date_of_birth,
    }
    return render(request, 'Customer_Profile.html',context)

def address(request):

    user_profile = None
    if request.user.is_authenticated:
        user_profile = Address.objects.get_or_create(customer=request.user)
    if request.method == 'POST':
        full_name = request.POST.get('fullName')
        phone = request.POST.get('phone')
        pincode = request.POST.get('pincode')
        address = request.POST.get('address')
        landmark = request.POST.get('landmark')
        city = request.POST.get('city')
        state = request.POST.get('state')
        address_type = request.POST.get('address-type')

        user_profile, created = Address.objects.get_or_create(customer=request.user)
        user_profile.fullName = full_name
        user_profile.phone = phone
        user_profile.pincode = pincode
        user_profile.address = address
        user_profile.landmark = landmark
        user_profile.city = city
        user_profile.state = state
        user_profile.address_type = address_type
        user_profile.save()

        if request.user.is_authenticated:
           user_profile = Address.objects.get(customer=request.user)


    return render(request, 'Customer_Profile.html', {'user_address': user_profile})

def edit_address(request):
    user_profile = None
    if request.user.is_authenticated:
        user_profile, created = Address.objects.get_or_create(customer=request.user)

    if request.method == 'POST':
        full_name = request.POST.get('fullName')
        phone = request.POST.get('phone')
        pincode = request.POST.get('pincode')
        address = request.POST.get('address')
        landmark = request.POST.get('landmark')
        city = request.POST.get('city')
        state = request.POST.get('state')
        address_type = request.POST.get('address-type')

        # Check if the Address object exists
        if not created:
            # Update the user profile with form data
            user_profile.fullName = full_name
            user_profile.phone = phone
            user_profile.pincode = pincode
            user_profile.address = address
            user_profile.landmark = landmark
            user_profile.city = city
            user_profile.state = state
            user_profile.address_type = address_type
            user_profile.save()

            messages.success(request, 'Address updated successfully.')
            return redirect('profile')  # Redirect to the profile page or another appropriate page after editing

    return render(request, 'edit_address.html', {'user_address': user_profile})


        

# @never_cache
# @login_required(login_url='login')
def user_home(request):
     return render(request, 'userhome.html')

from django.shortcuts import render, redirect



# def add_product(request):
#     if request.method == 'POST':
#         # Handle the form submission
#         product_id = request.POST.get('product-id')
#         product_name = request.POST.get('product-name')
#         category = request.POST.get('category-name')
#         subcategory = request.POST.get('subcategory-name')
#         stock = request.POST.get('stock')
#         description = request.POST.get('description')
#         price = request.POST.get('price')
#         discount = request.POST.get('discount')  # Retrieve as a string
#         status = request.POST.get('status')
#         product_image = request.FILES.get('product-image')

#         # Convert price and discount to floats
#         price = float(price)
#         discount = float(discount)

#         # Calculate sale_price
#         sale_price = price - (price * (discount / 100))

#         # Retrieve the Category and Subcategory objects based on their names
#         category = Category1.objects.get(name=category)
#         subcategory = Subcategory1.objects.get(name=subcategory)

#         # Create a new Product object and save it to the database
#         product = Product1(
#             product_id=product_id,
#             product_name=product_name,
#             category=category,  # Assign the Category object
#             subcategory=subcategory,  # Assign the Subcategory object
#             stock=stock,
#             description=description,
#             price=price,
#             discount=discount,
#             sale_price=sale_price,
#             status=status,
#             product_image=product_image
#         )
#         product.save()

#         # Redirect to a success page or any other desired action
#         return redirect('adminpanel')

#     return render(request, 'adminpanel.html')
from django.shortcuts import render, redirect
from .models import Product1  # Import the Product1 model

from django.shortcuts import render, redirect
from .models import Product1, Category1, Subcategory1

# def add_product(request):
#     if request.method == 'POST':
#         # Extract form data from the request
#         product_name = request.POST.get('product-name')
#         category_name = request.POST.get('category-name')
#         subcategory_name = request.POST.get('subcategory-name')
#         quantity = request.POST.get('quantity')
#         description = request.POST.get('description')
#         price = request.POST.get('price')
#         discount = request.POST.get('discount')
#         sale_price = request.POST.get('sale-price')
#         status = request.POST.get('status')
#         product_image = request.FILES.get('product-image')

#         # Retrieve Category1 and Subcategory1 instances based on the names
#         try:
#             category = Category1.objects.get(name=category_name)
#             subcategory = Subcategory1.objects.get(name=subcategory_name)
#         except Category1.DoesNotExist:
#             # Handle the case where the category doesn't exist
#             # You can return an error response or redirect as needed
#             # For simplicity, you can redirect to the add_product page
#             return redirect('add_product')

#         # Create a new Product1 instance and save it
#         product = Product1(
#             product_name=product_name,
#             category=category,
#             subcategory=subcategory,
#             stock=quantity,
#             description=description,
#             price=price,
#             discount=discount,
#             sale_price=sale_price,
#             status=status,
#             product_image=product_image
#         )
#         product.save()

#         return redirect('adminpanel')  # Replace 'product_list' with the URL name for the product listing page

#     return render(request, 'adminpanel.html')

# 
# from django.shortcuts import render, redirect
# from .models import Category1, Subcategory1, Product1

# def add_product(request):
#     if request.method == 'POST':
#         # Extract form data from the request
#         product_name = request.POST.get('product-name')
#         category_name = request.POST.get('category-name')
#         subcategory_name = request.POST.get('subcategory-name')
#         quantity = request.POST.get('quantity')
#         description = request.POST.get('description')
#         price = request.POST.get('price')
#         discount = request.POST.get('discount')
#         sale_price = request.POST.get('sale-price')
#         status = request.POST.get('status')
#         product_image = request.FILES.get('product-image')

#         # Validate form data (you may need to add more validation)
#         if not (product_name and category_name and subcategory_name and quantity and
#                 description and price and discount and sale_price and status and product_image):
#             # Handle invalid form data (redirect, show error message, etc.)
#             return redirect('add_product')

#         # Retrieve or create Category1 instance based on the name
#         category, created_category = Category1.objects.get_or_create(name=category_name)

#         # Retrieve or create Subcategory1 instance based on the name and category
#         subcategory, created_subcategory = Subcategory1.objects.get_or_create(
#             name=subcategory_name,
#             category=category
#         )

#         # Create a new Product1 instance and save it
#         product = Product1(
#             product_name=product_name,
#             category=category,
#             subcategory=subcategory,
#             stock=quantity,
#             description=description,
#             price=price,
#             discount=discount,
#             sale_price=sale_price,
#             status=status,
#             product_image=product_image
#         )
#         product.save()

#         return redirect('adminpanel')  # Replace 'adminpanel' with the URL name for the admin panel

#     return render(request, 'adminpanel.html')

# from django.shortcuts import render, redirect
# from django.db.models import Q
# from .models import Category1, Subcategory1, Product1

# def add_product(request):
#     if request.method == 'POST':
#         # Extract form data from the request
#         product_name = request.POST.get('product-name')
#         category_name = request.POST.get('category-name')
#         subcategory_name = request.POST.get('subcategory-name')
#         quantity = request.POST.get('quantity')
#         description = request.POST.get('description')
#         price = request.POST.get('price')
#         discount = request.POST.get('discount')
#         sale_price = request.POST.get('sale-price')
#         status = request.POST.get('status')
#         product_image = request.FILES.get('product-image')

#         # Validate form data (you may need to add more validation)
#         if not (product_name and category_name and subcategory_name and quantity and
#                 description and price and discount and sale_price and status and product_image):
#             # Handle invalid form data (redirect, show error message, etc.)
#             return redirect('add_product')

#         # Retrieve or create Category1 instance based on the name (case-insensitive)
#         category, created_category = Category1.objects.get_or_create(name=category_name)
#         if not created_category:
#             # If the category already exists, you might want to handle this differently,
#             # for example, by showing an error message or redirecting back to the form.
#             return redirect('add_product')

#         # Retrieve or create Subcategory1 instance based on the name and category (case-insensitive)
#         subcategory, created_subcategory = Subcategory1.objects.get_or_create(
#             name__iexact=subcategory_name,
#             category=category
#         )

#         # Create a new Product1 instance and save it
#         product = Product1(
#             product_name=product_name,
#             category=category,
#             subcategory=subcategory,
#             stock=quantity,
#             description=description,
#             price=price,
#             discount=discount,
#             sale_price=sale_price,
#             status=status,
#             product_image=product_image
#         )
#         product.save()

#         return redirect('adminpanel')  # Replace 'adminpanel' with the URL name for the admin panel

    # return render(request, 'adminpanel.html')


from django.shortcuts import render, redirect
from .models import Category1, Subcategory1, Product1

def add_product(request):
    if request.method == 'POST':
        category_name = request.POST.get('category-name')
        category, created = Category1.objects.get_or_create(name=category_name)

        # Retrieve or create the Subcategory2 instance while providing the Category2 instance
        subcategory_name = request.POST.get('subcategory-name')
        subcategory, created = Subcategory1.objects.get_or_create(name=subcategory_name, category=category)

        # Handle the form submission
        product_name = request.POST.get('product-name')
        stock = request.POST.get('stock')  # Retrieve quantity from the form
        description = request.POST.get('description')
        price = request.POST.get('price')
        discount = request.POST.get('discount')
        status = request.POST.get('status')
        product_image = request.FILES.get('product-image')

        price = float(price)
        discount = float(discount)

        # Calculate sale_price
        sale_price = price - (price * (discount / 100))

        # Create a new Product2 object and save it to the database
        product = Product1(
            product_name=product_name,
            category=category,
            subcategory=subcategory,
            stock=stock,  # Assign the quantity field
            description=description,
            price=price,
            discount=discount,
            sale_price=sale_price,
            status=status,
            product_image=product_image,
        )
        product.save()

        # Redirect to a success page or any other desired action
        return redirect('viewproduct')

    return render(request, 'addproduct.html')


# def add_product(request):
#     if request.method == 'POST':
#         # Extract form data from the request
#         product_name = request.POST.get('product-name')
#         category_name = request.POST.get('category-name')
#         subcategory_name = request.POST.get('subcategory-name')
#         quantity = request.POST.get('quantity')
#         description = request.POST.get('description')
#         price = request.POST.get('price')
#         discount = request.POST.get('discount')
#         sale_price = request.POST.get('sale-price')
#         status = request.POST.get('status')
#         product_image = request.FILES.get('product-image')

#         # Validate form data (you may need to add more validation)
#         # if not (product_name and category_name and subcategory_name and quantity and
#         #         description and price and discount and sale_price and status and product_image):
#         #     # Handle invalid form data (redirect, show error message, etc.)
#         #     return redirect('add_product')
#         if not (product_name and category_name and subcategory_name and quantity and
#             description and price and discount and sale_price and status and product_image):
#         # Handle invalid form data
#             messages.error(request, 'Please fill in all the required fields.')
#             return redirect('add_product')
#         else:
   

#         #Retrieve or create Category1 instance based on the name (case-insensitive)
#             category, created_category = Category1.objects.get_or_create(name__iexact=category_name)
#             if not created_category:
#                 # If the category already exists, you might want to handle this differently,
#             # for example, by showing an error message or redirecting back to the form.
#                 return redirect('add_product')

#             #Create or retrieve Subcategory1 instance based on the name and category (case-insensitive)
#             subcategory, created_subcategory = Subcategory1.objects.get_or_create(
#                 name__iexact=subcategory_name,
#                 category=category
#             )

#             # Create a new Product1 instance and save it
#             product = Product1(
#                 product_name=product_name,
#                 category=category,
#                 subcategory=subcategory,
#                 stock=quantity,
#                 description=description,
#                 price=price,
#                 discount=discount,
#                 sale_price=sale_price,
#                 status=status,
#                 product_image=product_image
#             )
#             product.save()

#         return redirect('adminpanel')  # Replace 'adminpanel' with the URL name for the admin panel

#     return render(request, 'adminpanel.html')


@login_required
def view_product(request):
    products = Product1.objects.all()  # Retrieve all products from the database
    return render(request, 'viewproduct.html', {'products': products})

def delete_product(request, product_id):
    if request.method == 'POST':
        # Delete the product from the database
        try:
            product = Product1.objects.get(pk=product_id)
            product.delete()
            return redirect('viewproduct')
        except Product1.DoesNotExist:
            pass
    return redirect('viewproduct')  # Redirect back to the product list view

def delete_user(request, user_id):
    if request.method == 'POST':
        try:
            user = CustomUser.objects.get(id=user_id)
            user.delete()
        except CustomUser.DoesNotExist:
            # Handle the case where the user does not exist
            pass
        # Redirect to a success page or any other desired action
        return redirect('view_users')  # Redirect to the user listing page
    return render(request, 'user.html')




# def add_to_cart(request):
#     # Fetch the product details from your Product model
#     products = Product.objects.all()  # This fetches all products; adjust as needed

#     # You can pass these products to your template
#     return render(request, 'addtocart.html', {'products': products})



def get_product_details(request):
    # Retrieve the product details (you can modify this based on your requirements)
    products = Product1.objects.all()
    product_data = []

    for product in products:
        product_data.append({
            
            'product_name': product.product_name,
            'category': product.category,
            'subcategory': product.subcategory,
            'stock': product.stock,
            'description': product.description,
            'price': product.price,
            'discount': product.discount,
            'sale_price': product.sale_price,
            'status': product.status,
            'product_image': product.product_image.url,
        })

    return render(request, 'product_details.html', {'products': product_data})

    


def product_details(request, id):
    # Retrieve the product details from the database
    product = get_object_or_404(Product1, id=id)

    # Render the product details template with the product data
    return render(request, 'details.html', {'product': product})


from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
# from .models import Product  # Import your Product model
@login_required
def edit_product(request, id):
    # Retrieve the product using get_object_or_404 to handle cases where the product doesn't exist
    product = get_object_or_404(Product1, pk=id)

    if request.method == 'POST':
        # Handle form submission and update the product
        # You can access form data using request.POST and request.FILES
        # Perform validation and update the product data in the database

        # Example:
        product.product_name = request.POST['product-name']
        product.category1 = request.POST['category-name']
        product.subcategory1 = request.POST['subcategory-name']
        product.stock = request.POST['stock']
        product.description = request.POST['description']
        product.price = request.POST['price']
        product.discount = request.POST['discount']
        product.sale_price = request.POST['sale-price']
        # product.product_image = request.POST['product_image']
        #product.product_image = request.FILES.get('product-image')
        
        # Save the updated product
        product.save()

        # Redirect to a product detail page or a success page
        #return HttpResponseRedirect('/product_detail/{0}/'.format(product.product_id))
       # return HttpResponseRedirect('adminpanel')

    # If the request method is GET, render the edit product form
    return render(request, 'editproduct.html', {'product': product})

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse


def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')  # Get the old password from the form
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        user = request.user  # Get the currently logged-in user

        # Check if the entered old password matches the user's current password
        if not user.check_password(old_password):
            return JsonResponse({'error': 'Incorrect old password'}, status=400)

        if new_password == confirm_password:
            # Change the user's password and save it to the database
            user.set_password(new_password)
            user.save()

            # Update the session to keep the user logged in
            update_session_auth_hash(request, user)

            return JsonResponse({'message': 'Password changed successfully'})
        else:
            return JsonResponse({'error': 'Passwords do not match'}, status=400)

    return render(request, 'change_password.html')






# def view_cart(request):
#     cart_items = AddToCart2.objects.filter(user=request.user, is_active=True)

#     # Calculate order summary
#     subtotal = sum(item.product.sale_price * item.quantity for item in cart_items)
#     shipping = 10  # Adjust this value as needed
#     total = subtotal + shipping
    
#     context = {
#         'cart_items': cart_items,
#         'subtotal': subtotal,
#         'shipping': shipping,
#         'total': total,
#     }
#     return render(request, 'view_cart.html', context)

# def remove_from_cart(request, item_id):
#     item = get_object_or_404(AddToCart2, pk=item_id)

#     if item.user == request.user:
#         # Remove the item from the cart and the database
#         item.delete()

#     # Recalculate order summary after item removal
#     cart_items = AddToCart2.objects.filter(user=request.user, is_active=True)
#     subtotal = sum(item.product.sale_price * item.quantity for item in cart_items)
#     shipping = 10  # Adjust this value as needed
#     total = subtotal + shipping

#     context = {
#         'cart_items': cart_items,
#         'subtotal': subtotal,
#         'shipping': shipping,
#         'total': total,
#     }
#     return render(request, 'view_cart.html', context)

# @never_cache
# @login_required(login_url='login')
# def add_to_cart(request, id):
#     product = get_object_or_404(Product1, pk=id)
    
#     # Check if the product is in stock
#     if product.stock <= 0:
#         messages.warning(request, f"{product.product_name} is out of stock.")
#     else:
#         # Get or create a cart item for the user and the selected product
#         cart_item, created = AddToCart2.objects.get_or_create(user=request.user, product=product)
        
#         if not created:
#             # If the cart item already exists, update its quantity and set it as active
#             cart_item.is_active = True
#             cart_item.quantity += 1
#             cart_item.save()
#         else:
#             # If it's a new item, set it as active
#             cart_item.is_active = True
#             cart_item.save()
    
#     return redirect('view_cart')  

# def remove_from_cart(request, item_id):
#     cart_item = get_object_or_404(AddToCart, id=item_id)
    
#     # Check if the item belongs to the current user
#     if cart_item.user == request.user:
#         cart_item.is_active = False
#         cart_item.save()
#         messages.success(request, f"{cart_item.product.product_name} has been removed from your cart.")
#     else:
#         messages.error(request, "You don't have permission to remove this item from your cart.")
    
#     return redirect('view_cart')


@never_cache
@login_required(login_url='login')
def add_to_cart(request, id):
    product = Product1.objects.get(pk=id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
    
    return redirect('view_cart')

# def add_to_cart(request, id):
#     rental_product = RentalProduct.objects.get(pk=id)
#     rental_cart, created = RentalCart.objects.get_or_create(rental_cart_user=request.user)
#     rental_cart_item, item_created = RentalCartItem.objects.get_or_create(cart=rental_cart, rental_product=rental_product)
    
#     if not item_created:
#         rental_cart_item.quantity += 1
#         rental_cart_item.save()
    
#     return redirect('view_cart')

# def add_to_cart(request, id):
#     rental_product = RentalProduct.objects.get(pk=id)
#     user = request.user

#     # Check if the user already has a rental cart
#     try:
#         rental_cart = RentalCart.objects.get(rental_cart_user=user)
#     except RentalCart.DoesNotExist:
#         # If the user doesn't have a rental cart, create one
#         rental_cart = RentalCart.objects.create(rental_cart_user=user)

#     # Check if the rental product is already in the user's cart
#     rental_cart_item, created = RentalCartItem.objects.get_or_create(cart=rental_cart, rental_product=rental_product)

#     if not created:
#         rental_cart_item.quantity += 1
#         rental_cart_item.save()

#     return redirect('view_cart')
def rentaladd_to_cart(request, id):
    rental_product = RentalProduct.objects.get(pk=id)
    rental_cart, created = RentalCart.objects.get_or_create(rental_cart_user=request.user)
    rental_cart_item, item_created = RentalCartItem.objects.get_or_create(cart=rental_cart, rental_product=rental_product)
    
    if not item_created:
        rental_cart_item.quantity += 1
        rental_cart_item.save()
    
    return redirect('rentalview_cart')





def remove_from_cart(request, id):
    product = Product1.objects.get(pk=id)
    
    cart = Cart.objects.get(user=request.user)
    try:
        cart_item = cart.cartitem_set.get(product=product)
        if cart_item.quantity >= 1:
             cart_item.delete()
    except CartItem.DoesNotExist:
        pass
    
    return redirect('view_cart')

def rentalremove_from_cart(request, id):
    rental_product = get_object_or_404(RentalProduct, pk=id)
    
    rental_cart = request.user.rentalcart
    try:
        rental_cart_item = rental_cart.rentalcartitem_set.get(rental_product=rental_product)
        rental_cart_item.delete()
    except RentalCartItem.DoesNotExist:
        pass
    
    return redirect('rentalview_cart')

# @login_required(login_url='login')
# def increase_cart_item(request, id):
#     rentalproduct = RentalProduct.objects.get(pk=id)
#     rental_cart = request.user.cart
#     rental_cart_item, created = RentalCartItem.objects.get_or_create(rental_cart=rental_cart, rentalproduct=rentalproduct)
#     if rental_cart_item.quantity < rentalproduct.stock:
#      rental_cart_item.quantity += 1
#      rental_cart_item.save()

#     return redirect('view_cart')

login_required(login_url='login')
def increase_cart_item(request, id):
    product = Product1.objects.get(pk=id)
    cart = request.user.cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if cart_item.quantity < product.stock:
     cart_item.quantity += 1
     cart_item.save()

    return redirect('view_cart')

login_required(login_url='login')
def rentalincrease_cart_item(request, id):
    rental_product = get_object_or_404(RentalProduct, pk=id)

    rental_cart = request.user.rentalcart  # Assuming user has a one-to-one relationship with RentalCart
    rental_cart_item, created = RentalCartItem.objects.get_or_create(cart=rental_cart, rental_product=rental_product)

    if rental_cart_item.quantity < rental_product.stock:
        rental_cart_item.quantity += 1
        rental_cart_item.save()

    return redirect('rentalview_cart')

@login_required(login_url='login')
def decrease_cart_item(request, id):
    
    product = Product1.objects.get(pk=id)
    cart = request.user.cart
    cart_item = cart.cartitem_set.get(product= product)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('view_cart')

@login_required(login_url='login')
def rentaldecrease_cart_item(request, id):
    rental_product = get_object_or_404(RentalProduct, pk=id)
    rental_cart = request.user.rentalcart
    rental_cart_item = rental_cart.rentalcartitem_set.get(rental_product= rental_product)


    if rental_cart_item.quantity > 1:
        rental_cart_item.quantity -= 1
        rental_cart_item.save()
    else:
        rental_cart_item.delete()

    return redirect('rentalview_cart')



def view_cart(request):
    cart = request.user.cart
    cart_items = CartItem.objects.filter(cart=cart)
    for item in cart_items:
        item.total_price = item.product.sale_price * item.quantity
    
    total_amount = sum(item.total_price for item in cart_items)

    return render(request, 'view_cart.html', {'cart_items': cart_items,'total_amount': total_amount})

# def view_cart(request):
#     rental_cart = RentalCart.objects.get(rental_cart_user=request.user)
#     rental_cart_items = RentalCartItem.objects.filter(cart=rental_cart)
#     for item in rental_cart_items:
#         item.total_price = item.rental_product.rental_price * item.quantity
    
#     total_amount = sum(item.total_price for item in rental_cart_items)

#     return render(request, 'view_cart.html', {'cart_items': rental_cart_items, 'total_amount': total_amount})

from django.db.models import ProtectedError

def rentalview_cart(request):
    try:
        rental_cart = RentalCart.objects.get(rental_cart_user=request.user)
    except RentalCart.DoesNotExist:
        rental_cart = RentalCart.objects.create(rental_cart_user=request.user)
    
    rental_cart_items = RentalCartItem.objects.filter(cart=rental_cart)
    
    for item in rental_cart_items:
        item.total_price = item.rental_product.rental_price * item.quantity
    
    total_amount = sum((item.rental_product.rental_price + item.rental_product.security_deposit) * item.quantity for item in rental_cart_items)

    return render(request, 'rentalview_cart.html', {'cart_items': rental_cart_items, 'total_amount': total_amount})



def fetch_cart_count(request):
    cart_count = 0
    if request.user.is_authenticated:
        cart = request.user.cart
        cart_count = CartItem.objects.filter(cart=cart).count()
    return JsonResponse({'cart_count': cart_count})

def get_cart_count(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(cart=request.user.cart)
        cart_count = cart_items.count()
    else:
        cart_count = 0
    return cart_count


def user_r(request):
    user_s = CustomUser.objects.exclude(user_types=1)
  # Fetch all products
    return render(request, 'user.html', {'user_s': user_s})

def delete_user(request, user_id):
    if request.method == 'POST':
        try:
            user = CustomUser.objects.get(id=user_id)
            user.delete()
        except CustomUser.DoesNotExist:
            # Handle the case where the user does not exist
            pass
        # Redirect to a success page or any other desired action
        return redirect('user_r')  # Redirect to the user listing page
    return render(request, 'user.html')


# def subcategory_products(request, category_name, subcategory_name):
#     products = Product.objects.filter(category=category_name, subcategory=subcategory_name)
#     return render(request, 'subcategory_products.html', {'category_name': category_name, 'subcategory_name': subcategory_name, 'products': products})


# def products_by_subcategory(request, subcategory):
#     # Retrieve products based on the provided subcategory
#     products = Product1.objects.filter(subcategory=subcategory)  # Replace 'subcategory' with your actual field name

#     return render(request, 'product.html', {'products': products})

from django.shortcuts import get_object_or_404


from django.shortcuts import get_list_or_404
def products_by_subcategory(request, subcategory):
    # Retrieve a list of Subcategory1 objects based on the provided subcategory name
    subcategories = get_list_or_404(Subcategory1, name=subcategory)

    # Retrieve products based on the list of Subcategory1 objects
    products = Product1.objects.filter(subcategory__in=subcategories)

    return render(request, 'product.html', {'products': products})


from django.shortcuts import render, redirect
from .models import WishlistItem

# def add_to_wishlist(request, id):
#     if request.user.is_authenticated:
#         product = Product1.objects.get(id=id)
#         WishlistItem, created = WishlistItem.objects.get_or_create(user=request.user, product=product)
#         if created:
#             # The item was added to the wishlist
#             messages.success(request, f'{product.product_name} has been added to your wishlist.')
#         else:
#             # The item is already in the wishlist
#             messages.warning(request, f'{product.product_name} is already in your wishlist.')
#     return redirect('wishlist')
def add_to_wishlist(request, id):
    if request.user.is_authenticated:
        product = Product1.objects.get(id=id)
        wishlist_item, created = WishlistItem.objects.get_or_create(user=request.user, product=product)
        if created:
            # The item was added to the wishlist
            messages.success(request, f'{product.product_name} has been added to your wishlist.')
        else:
            # The item is already in the wishlist
            messages.warning(request, f'{product.product_name} is already in your wishlist.')
    return redirect('wishlist')


@never_cache
@login_required(login_url='login')
def wishlist(request):
    if request.user.is_authenticated:
        wishlist_items = WishlistItem.objects.filter(user=request.user)
        return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})
    else:
        return redirect('login')  # Redirect to the login page if the user is not authenticated

# def remove_from_wishlist(request, wishlist_item_id):
#     # Retrieve the WishlistItem object for the product
#     wishlist_item = get_object_or_404(WishlistItem, wishlist_item_id=wishlist_item_id, user=request.user)
# def remove_from_wishlist(request, wishlist_item_id):
#     try:
#         wishlist_item = get_object_or_404(WishlistItem, id=wishlist_item_id)
#         # Perform the logic to remove the wishlist item here
#         # ...
#     except WishlistItem.DoesNotExist:
#         # Handle the case where the item with the specified ID doesn't exist
#         # ...


#     # Remove the item from the wishlist
#        wishlist_item.delete()

#     # Redirect the user back to their wishlist page
#     return redirect('wishlist')  # Adjust the URL name as needed

from django.shortcuts import get_object_or_404
from .models import WishlistItem
@login_required
def remove_from_wishlist(request, wishlist_item_id):
    try:
        wishlist_item = get_object_or_404(WishlistItem, id=wishlist_item_id)
        # Perform the logic to remove the wishlist item here
        # ...
        wishlist_item.delete()  # Remove the item from the wishlist
        return redirect('wishlist')  # Redirect the user back to their wishlist page
    except WishlistItem.DoesNotExist:
        # Handle the case where the item with the specified ID doesn't exist
        return HttpResponseNotFound("Wishlist item not found")


# def remove_from_wishlist(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     # Remove the product from the user's wishlist
#     WishlistItem.objects.filter(user=request.user, product=product).delete()
#     return redirect('wishlist')

# def profile_view(request):
#     user_profile = request.user.profile

#     if request.method == 'POST':
#         # Handle the form submission
#         fullName = request.POST['fullName']
#         gender = request.POST['gender']
#         date_of_birth = request.POST['date-of-birth']
#         email = request.POST['email']
#         phone = request.POST['phone']

#         user_profile.fullName = fullName
#         user_profile.gender = gender
#         user_profile.date_of_birth = date_of_birth
#         user_profile.email = email
#         user_profile.phone = phone

#         user_profile.save()
#         messages.success(request, 'Profile information updated successfully.')
#         return redirect('Customer_Profile')  # Redirect to the profile page after the update

#     context = {
#         'user_profile': user_profile,
#     }

#     return render(request, 'Customer_Profile.html', context)



def total_users(request):
    total_users_count = CustomUser.objects.count()
    print(total_users_count)  # Add this line for debugging
    return render(request, 'adminpanel.html', {'total_users_count': total_users_count})

# def block_unblock_user(request, user_id):
#     user = CustomUser.objects.get(pk=user_id)
#     if user.is_active:
#         user.is_active = False  # Block the user
#         subject = 'Account Blocked'
#         message = 'Your account has been blocked by the admin.'
#         from_email = 'chithiracb2024a@mca.ajce.in'  # Use your admin's email address
#         recipient_list = [user.email]
#         send_mail(subject, message, from_email, recipient_list, fail_silently=False)
#     else:
#         user.is_active = True  # Unblock the user
#     user.save()
#     return redirect('adminpanel')


# def checkout(request):
#     user_address = Address.objects.filter(customer=request.user).first()

#     return render(request, 'checkout.html', {'user_address': user_address})
# def checkout(request):   
#     user_address = Address.objects.filter(customer=request.user).first()

#     # Retrieve cart items
#     cart_items = AddToCart2.objects.filter(user=request.user)

#     total_price = sum(item.product.sale_price * item.quantity for item in cart_items)

#     # Calculate total amount
#     total = sum(item.product.sale_price * item.quantity for item in cart_items)

#     return render(request, 'checkout.html', {
#         'user_address': user_address,
#         'cart_items': cart_items,
#         'total': total,
#         'total_price':total_price,
#     })

# def checkout(request):   
#     user_address = Address.objects.filter(customer=request.user).first()

#     # Retrieve cart items
#     cart_items = Cart.objects.filter(user=request.user)

#     # Calculate total amount and total price for each item
#     total = sum(item.product.sale_price * item.quantity for item in cart_items)
    
#     # Calculate total price for all items
#     total_price = sum(item.product.sale_price * item.quantity for item in cart_items)

#     # Add total_price to each cart item
#     for item in cart_items:
#         item.total_price = item.product.sale_price * item.quantity

#     return render(request, 'checkout.html', {
#         'user_address': user_address,
#         'cart_items': cart_items,
#         'total': total,
#         'total_price': total_price,
#     })

def checkout(request):
    user_address = ProfileUser.objects.filter(user=request.user).first()

    cart_items = CartItem.objects.filter(cart=request.user.cart)
    total_amount = sum(item.product.price * item.quantity for item in cart_items)

    cart_count = get_cart_count(request)
    # email = request.user.email
    # full_name = request.user.profile.full_name

    context = {
        'cart_count': cart_count,
        'cart_items': cart_items,
        'total_amount': total_amount,
        'user_address': user_address,
        # 'email':email,
        # 'full_name': full_name
    }
    return render(request, 'checkout.html', context)


# @csrf_exempt
# def create_order(request):
#     if request.method == 'POST':
#         user = request.user
#         cart = user.cart

#         cart_items = CartItem.objects.filter(cart=cart)
#         total_amount = sum(item.product.price * item.quantity for item in cart_items)

#         try:
#             order = Order.objects.create(user=user, total_amount=total_amount)
#             for cart_item in cart_items:
#                 OrderItem.objects.create(
#                     order=order,
#                     product=cart_item.product,
#                     quantity=cart_item.quantity,
#                     item_total=cart_item.product.price * cart_item.quantity
#                 )

#             client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
#             payment_data = {
#                 'amount': int(total_amount*100),
#                 'currency': 'INR',
#                 'receipt': f'order_{order.id}',
#                 'payment_capture': '1'
#             }
#             orderData = client.order.create(data=payment_data)
#             order.payment = orderData['id']
#             order.save()

#             return JsonResponse({'order_id': orderData['id']})
        
#         except Exception as e:
#             print(str(e))
#             return JsonResponse({'error': 'An error occurred. Please try again.'}, status=500)

@csrf_exempt
def create_order(request):
    if request.method == 'POST':
        user = request.user
        cart = user.cart

        cart_items = CartItem.objects.filter(cart=cart)
        total_amount = sum(item.product.price * item.quantity for item in cart_items)

        try:
            order = Order.objects.create(user=user, total_amount=total_amount)
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    item_total=cart_item.product.price * cart_item.quantity
                )

            client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
            payment_data = {
                'amount': int(total_amount * 100),
                'currency': 'INR',
                'receipt': f'order_{order.id}',
                'payment_capture': '1'
            }
            orderData = client.order.create(data=payment_data)
            order.payment_id = orderData['id']
            order.save()

            return JsonResponse({'order_id': orderData['id']})
        
        except Exception as e:
            print(str(e))
            return JsonResponse({'error': 'An error occurred. Please try again.'}, status=500)



# @csrf_exempt
# def handle_payment(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         razorpay_order_id = data.get('order_id')
#         payment_id = data.get('payment_id')

#         try:
#             order = Order.objects.get(payment_id=razorpay_order_id)

#             client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
#             payment = client.payment.fetch(payment_id)

#             if payment['status'] == 'captured':
#                 order.payment_status = True
#                 order.save()
#                 place_order(request.user.email)

#                 user = request.user
#                 user.cart.cartitem_set.all().delete()
#                 return JsonResponse({'message': 'Payment successful'})
#             else:
#                 return JsonResponse({'message': 'Payment failed'})

#         except Order.DoesNotExist:
#             return JsonResponse({'message': 'Invalid Order ID'})
#         except Exception as e:

#             print(str(e))
#             return JsonResponse({'message': 'Server error, please try again later.'})

# @login_required(login_url='login')
# def place_order(request):
#     # Your existing code to place the order

#     # Fetch the user's email
#     user_email = request.user.email

#     # Send order confirmation email
#     subject = 'Order Confirmation'
#     message = 'Thank you for placing your order!'
#     from_email = 'chithiracb2024a@mca.ajce.in'
#     recipient_list = [user_email]
#     send_mail(subject, message, from_email, recipient_list)

# def send_order_confirmation_email(user_email):
#     subject = 'Order Confirmation'
#     message = 'Thank you for placing your order! Your payment was successful.'
#     from_email = 'chithiracb2024a@mca.ajce.in'
#     recipient_list = [user_email]
    
#     send_mail(subject, message, from_email, recipient_list)



def edit_profile(request):
    userprofile = get_object_or_404(UserProfile1, user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('edit_profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'userprofile': userprofile,
    }
    return render(request, 'edit_profile.html', context)

@csrf_exempt
def handle_payment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        razorpay_order_id = data.get('order_id')
        payment_id = data.get('payment_id')

        try:
            order = Order.objects.get(payment_id=razorpay_order_id)

            client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
            payment = client.payment.fetch(payment_id)

            if payment['status'] == 'captured':
                order.payment_status = True
                order.save()

                for order_item in order.orderitem_set.all():
                        product = order_item.product
                        product.stock -= order_item.quantity
                        product.save()


                data = {
                  'order_id': order.id,
                   'transID': order.payment_id,
            }
                return JsonResponse({'message': 'Payment successful', 'order_id': order.id, 'transID': order.payment_id})
            #     return JsonResponse({'message': 'Payment successful'})
            # else:
            #     return JsonResponse({'message': 'Payment failed'})

        except Order.DoesNotExist:
            return JsonResponse({'message': 'Invalid Order ID'})
        except Exception as e:

            print(str(e))
            return JsonResponse({'message': 'Server error, please try again later.'})


def order_complete(request):
    order_id = request.GET.get('order_id')
    transID = request.GET.get('payment_id')
    print("Order ID from GET parameters:", order_id)
    try:
   
        order = Order.objects.get(id=order_id, payment_status=True)
        print("Retrieved Order:", order)
        ordered_products = OrderItem.objects.filter(order_id=order.id)

        subtotal = 0
        for i in ordered_products: 
            subtotal += i.product.sale_price * i.quantity
        

        context = {
            'order': order,
            'ordered_products': ordered_products,
            'order_id': order.id,
           'transID': transID,
           'subtotal': subtotal,
        }

        return render(request, 'order_complete.html', context)
    except Order.DoesNotExist:
        return redirect('userhome')


@login_required(login_url='login')
def myorders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'orders': orders,
        
    }
    return render(request, 'myorders.html', context)

def user_profile(request):
    # Retrieve the logged-in user's information
    user = request.user

    # You can fetch additional information from the user's profile if needed
    # For example: profile = user.profileuser

    context = {
        'user': user,
        # Add additional context variables as needed
    }

    return render(request, 'user_profile.html', context)






def save_profile(request):
    if request.method == 'POST':
        try:
            # Retrieve the user's profile instance or create it if it doesn't exist
            user_profile, created = ProfileUser.objects.get_or_create(user=request.user)

            # Get form data from the request
            phone_number = request.POST.get('phone_number')
            pincode = request.POST.get('pincode')
            address = request.POST.get('address')
            gender = request.POST.get('gender')
            city = request.POST.get('city')
            state = request.POST.get('state')

            # Update the user's profile fields
            user_profile.phone_number = phone_number
            user_profile.pincode = pincode
            user_profile.address = address
            user_profile.gender = gender
            user_profile.city = city
            user_profile.state = state

            # Save the changes
            user_profile.save()

            messages.success(request, 'Profile updated successfully.')
            return redirect('user_profile')  # Redirect to the user profile page
        except Exception as e:
            messages.error(request, f'Error updating profile: {e}')

    return render(request, 'user_profile.html')

@never_cache
@login_required(login_url='login')
def profile(request):
    return render(request, 'profile.html')


def search_products(request):
    query = request.GET.get('q', '')
    products = Product1.objects.filter(product_name=query)
    
    context = {
        'products': products,
        'query': query,
    }
    return render(request, 'viewproduct.html', context)


# def rent_product(request, product_id):
#     if request.method == 'POST':
#         # Process the rental form submission
#         # You can access the form data using request.POST
#         # For example: rental_start_date = request.POST.get('start_date')
#         # Perform necessary validations and save data to the database
#         # Redirect the user to a thank you page or back to the product details page
#         return redirect('thank_you_page')  # Replace 'thank_you_page' with the URL name of your thank you page
#     else:
#         # Render the rental form
#         return render(request, 'rent_product.html')
    
def rent_product(request,id):
    return render(request, 'details.html')

def rental(request):
    return render(request, 'rental.html')

# def add_rental_product(request):
#     return render(request, 'addrentalproduct.html')



def add_rental_product(request):
    if request.method == 'POST':
        category_name = request.POST.get('category-name')
        category, created = Category1.objects.get_or_create(name=category_name)
        
        subcategory_name = request.POST.get('subcategory-name')
        subcategory, created = Subcategory1.objects.get_or_create(name=subcategory_name, category=category)

        rental_product_name = request.POST.get('product-name')
        stock = request.POST.get('stock')
        description = request.POST.get('description')
        rental_price = request.POST.get('price')
        security_deposit = request.POST.get('security-amount')
        status = request.POST.get('status')
        image = request.FILES.get('product-image')

        # Create and save the RentalProduct object
        rental_product = RentalProduct(
            rental_product_name=rental_product_name,
            category=category,
            subcategory=subcategory,
            stock=stock,
            description=description,
            rental_price=rental_price,
            security_deposit=security_deposit,
            status=status,
            image=image
        )
        rental_product.save()

        # Redirect to a success page or dashboard
        return redirect('adminpanel')  # Replace 'adminpanel' with the actual URL name for your admin panel
    
    return render(request, 'addrentalproduct.html')

def view_rental_product(request):
    rental_products = RentalProduct.objects.all()  # Retrieve all rental products from the database
    return render(request, 'viewrentalproduct.html', {'rental_products': rental_products})

def delete_rental_product(request, id):
    if request.method == 'POST':
        # Get the rental product object
        rental_product = get_object_or_404(RentalProduct, pk=id)
        # Update the status to 'inactive'
        rental_product.status = 'inactive'
        rental_product.save()
        # Redirect to a relevant page after deletion
        return redirect('viewrentalproduct')
    # Handle GET requests if needed
    return redirect('viewrentalproduct') 

def rental_products(request):
    rental_products = RentalProduct.objects.all()
    return render(request, 'rental_products.html', {'rental_products': rental_products})

def rental_details(request, id):
    # Retrieve the product details from the database
    rental_products = get_object_or_404(RentalProduct, id=id)
    ratings = RentalRating.objects.filter(rental_products=rental_products)

    # Render the product details template with the product data
    return render(request, 'rentaldetails.html', {'rental_products': rental_products,'ratings':ratings})

# def rentalproducts_by_subcategory(request, subcategory_name):
#     # Get the subcategory object based on the subcategory name
#     subcategory = Subcategory1.objects.get(name=subcategory_name)
    
#     # Filter rental products based on the subcategory
#     rental_products = RentalProduct.objects.filter(subcategory=subcategory)
    
#     return render(request, 'rental_products.html', {'rental_products': rental_products})

def rentalproducts_by_subcategory(request, subcategory):
    # Retrieve a list of Subcategory1 objects based on the provided subcategory name
    subcategories = get_list_or_404(Subcategory1, name=subcategory)

    # Retrieve products based on the list of Subcategory1 objects
    rental_products = RentalProduct.objects.filter(subcategory__in=subcategories)

    return render(request, 'rental_products.html', {'rental_products': rental_products})

# def rentaladd_to_cart(request, id):
#     rentalproduct = RentalProduct.objects.get(pk=id)
#     cart, created = RentalCart.objects.get_or_create(user=request.user)
#     cart_item, item_created = RentalCartItem.objects.get_or_create(cart=cart, rentalproduct=rentalproduct)
    
#     if not item_created:
#         cart_item.quantity += 1
#         cart_item.save()
    
#     return redirect('rentalview_cart')

# def rentalview_cart(request):
#     cart = request.user.cart
#     cart_items = RentalCartItem.objects.filter(cart=cart)
#     # for item in cart_items:
#     #     item.total_price = item.product.sale_price * item.quantity
    
#     # total_amount = sum(item.total_price for item in cart_items)

#     return render(request, 'rentalview_cart.html', {'cart_items': cart_items})

from django.shortcuts import get_object_or_404

# def rentalview_cart(request):
#     # Retrieve the RentalCart instance for the current user
#     rental_cart = get_object_or_404(RentalCart, user=request.user)

#     # Retrieve the cart items associated with the RentalCart instance
#     cart_items = RentalCartItem.objects.filter(cart=rental_cart)

#     return render(request, 'rentalview_cart.html', {'cart_items': cart_items})

# def rentalview_cart(request):
#     return render(request, 'rentalview_cart.html')

# def rentalview_cart(request):
#     cart = request.user.cart
#     cart_items = RentalCartItem.objects.filter(cart=cart)
#     for item in cart_items:
#         item.total_price = item.product.sale_price * item.quantity
    
#     total_amount = sum(item.total_price for item in cart_items)

#     return render(request, 'rentalview_cart.html', {'cart_items': cart_items,'total_amount': total_amount})


def rental_checkout(request):
    user_address = ProfileUser.objects.filter(user=request.user).first()

    rental_cart_items = RentalCartItem.objects.filter(cart__rental_cart_user=request.user)
    total_amount = sum((item.rental_product.rental_price + item.rental_product.security_deposit) * item.quantity for item in rental_cart_items)

    cart_count = get_cart_count(request)

    context = {
        'cart_count': cart_count,
        'rental_cart_items': rental_cart_items,
        'total_amount': total_amount,
        'user_address': user_address,
    }
    return render(request, 'rentalcheckout.html', context)

def create_rental_order(request):
    if request.method == 'POST':
        user = request.user
        cart = user.rentalcart  # Assuming user has a RentalCart related_name set to 'rentalcart'

        cart_items = RentalCartItem.objects.filter(cart=cart)
        total_amount = sum(item.rental_product.rental_price * item.quantity for item in cart_items)

        try:
            rental_order = RentalOrder.objects.create(user=user, total_amount=total_amount)
            for cart_item in cart_items:
                RentalOrderItem.objects.create(
                    order=rental_order,
                    rental_product=cart_item.rental_product,
                    quantity=cart_item.quantity,
                    item_total=cart_item.rental_product.rental_price * cart_item.quantity
                )

            client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
            payment_data = {
                'amount': int(total_amount * 100),
                'currency': 'INR',
                'receipt': f'rental_order_{rental_order.id}',
                'payment_capture': '1'
            }
            order_data = client.order.create(data=payment_data)
            rental_order.payment_id = order_data['id']
            rental_order.save()

            return JsonResponse({'order_id': order_data['id']})
        
        except Exception as e:
            print(str(e))
            return JsonResponse({'error': 'An error occurred. Please try again.'}, status=500)

def rental_handle_payment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        razorpay_order_id = data.get('order_id')
        payment_id = data.get('payment_id')

        try:
            rental_order = RentalOrder.objects.get(payment_id=razorpay_order_id)

            client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
            payment = client.payment.fetch(payment_id)

            if payment['status'] == 'captured':
                rental_order.payment_status = True
                rental_order.save()

                # Perform any additional actions related to payment success
                # For example, updating stock levels or sending confirmation emails
                
                data = {
                    'order_id': rental_order.id,
                    'transID': rental_order.payment_id,
                }
                return JsonResponse({'message': 'Payment successful', 'order_id': rental_order.id, 'transID': rental_order.payment_id})
            else:
                return JsonResponse({'message': 'Payment failed'})

        except RentalOrder.DoesNotExist:
            return JsonResponse({'message': 'Invalid Order ID'})
        except Exception as e:
            print(str(e))
            return JsonResponse({'message': 'Server error, please try again later.'})


def rental_order_complete(request):
    order_id = request.GET.get('order_id')
    transID = request.GET.get('payment_id')
    print("Order ID from GET parameters:", order_id)
    try:
        rental_order = RentalOrder.objects.get(id=order_id, payment_status=True)
        print("Retrieved RentalOrder:", rental_order)
        ordered_rental_products = RentalOrderItem.objects.filter(order_id=rental_order.id)

        subtotal = 0
        for item in ordered_rental_products:
            subtotal += item.rental_product.rental_price * item.quantity

        context = {
            'rental_order': rental_order,
            'ordered_rental_products': ordered_rental_products,
            'order_id': rental_order.id,
            'transID': transID,
            'subtotal': subtotal,
        }

        return render(request, 'rental_order_complete.html', context)
    except RentalOrder.DoesNotExist:
        return redirect('userhome')


def rate_rentalproduct(request, id):
    if request.method == 'POST':
        user = request.user
        rental_products= RentalProduct.objects.get(pk=id)
        value = int(request.POST['rating'])
        comment = request.POST.get('comment', '')

        rating, created = RentalRating.objects.get_or_create(user=user, rental_products=rental_products, defaults={'value': value, 'comment': comment})

        if not created:
            rating.value = value
            rating.comment = comment
            rating.save()

        return redirect('rate_rentalproduct', id=rental_products.id)
    else:
        return redirect('userhome')
    
def rate_product(request, id):
    if request.method == 'POST':
        user = request.user
        product= Product1.objects.get(pk=id)
        value = int(request.POST['rating'])
        comment = request.POST.get('comment', '')

        rating, created = RentalRating.objects.get_or_create(user=user, product=product, defaults={'value': value, 'comment': comment})

        if not created:
            rating.value = value
            rating.comment = comment
            rating.save()

        return redirect('rate_product', id=product.id)
    else:
        return redirect('userhome')


# def order_cancellation(request,id):
#     return render(request, 'ordercancellation.html')
    
def order_status(request, id):
    # Retrieve the order object based on the provided ID
    order = get_object_or_404(Order, id=id)
    user_address = ProfileUser.objects.filter(user=request.user).first()
    
    # Extract relevant information from the order object
    order_id = order.id
    status = order.status
    products = order.products.all()  # Retrieve associated products
    
    # Pass the data to the template
    context = {
        'order_id': order_id,
        'status': status,
        'products': products,
        'user_address':user_address,
        'total_amount': order.total_amount,
    }

    return render(request, 'orderstatus.html', context)

def order_cancellation(request, id):
    if request.method == 'POST':
        # Get the order object
        order = Order.objects.get(id=id)
        
        # Update order status to 'Cancelled'
        order.status = 'Cancelled'
        order.save()
        
        # Optionally, you can handle additional logic here, such as sending confirmation emails, etc.
        
        return JsonResponse({'message': 'Order successfully cancelled'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

# def order_cancellation(request, id):
#     if request.method == 'POST':
#         # Get the order object
#         order = Order.objects.get(id=id)
        
#         # Update status of order items to 'Cancelled'
#         order_items = OrderItem.objects.filter(order=order)
#         for item in order_items:
#             item.status = 'Cancelled'
#             item.save()
        
#         # Check if all order items are cancelled
#         all_cancelled = all(item.status == 'Cancelled' for item in order_items)
#         if all_cancelled:
#             # Update order status to 'Cancelled'
#             order.status = 'Cancelled'
#             order.save()
        
#         # Optionally, you can handle additional logic here, such as sending confirmation emails, etc.
        
#         # Redirect to the myorders page
#         return redirect('myorders')  # Assuming 'myorders' is the name of the URL pattern for the myorders page
#     else:
#         return JsonResponse({'error': 'Invalid request method'}, status=405)

def order_details(request, order_id):
    order = Order.objects.get(id=order_id)
    cancel_button_visible = order.status != 'Cancelled'
    return render(request, 'orderstatus.html', {'order': order, 'cancel_button_visible': cancel_button_visible})

def order_view(request):
    orders = Order.objects.order_by('-created_at')
    order_items = OrderItem.objects.select_related('product').filter(order__in=orders)
    return render(request, 'orderview.html', {'orders': orders, 'order_items': order_items})
   
def order_detail_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = order.orderitem_set.all()  # Fetch related OrderItems
    return render(request, 'orderdetailview.html', {'order': order, 'order_items': order_items})

def messages_page(request):
    threads = Thread.objects.by_user(user=request.user).prefetch_related('chatmessage_thread').order_by('timestamp')
    context = {
        'Threads': threads
    }
    return render(request, 'messages.html', context)

def refund_request(request, order_id):
    
    return render(request, 'refund_request.html', {'order_id': order_id})

def update_order_status(request, order_id):
    if request.method == 'POST':
        new_status = request.POST.get('status')
        order = Order.objects.get(pk=order_id)
        order.status = new_status
        order.save()
        return redirect('orderview')  # Redirect to the order view page after updating status
    else:
        # Handle GET request if needed
        pass

def deliveryboydashboard(request):
    return render(request, 'deliveryboydashboard.html')

import csv

def financial_report_csv(request):
    # Retrieve orders data or any other financial data you need, ordered by creation date in descending order
    orders = Order.objects.order_by('-created_at')
    
    # Prepare CSV data
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="financial_report.csv"'

    # Create a CSV writer
    writer = csv.writer(response)
    
    # Write header row
    writer.writerow(['Order ID', 'User', 'Total Amount', 'Status', 'Purchased On'])

    # Write order data rows
    for order in orders:
        writer.writerow([order.id, order.user.fullName, order.total_amount, order.status, order.created_at])

    return response

def return_order(request):
    if request.method == 'POST':
        # Retrieve form data
        return_reason = request.POST.get('returnReason')
        return_comments = request.POST.get('returnComments')
        
        # Process the return request, you can send it to the admin panel here
        
        # Example response
        return JsonResponse({'message': 'Return request submitted successfully'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
