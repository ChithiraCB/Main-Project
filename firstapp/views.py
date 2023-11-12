
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate ,login as auth_login,logout
from django.contrib import messages
from django.http import JsonResponse,HttpResponseNotFound
from django.shortcuts import render,get_object_or_404
from django.core.mail import send_mail
from . models import *
from django.contrib.auth.decorators import *
from django.views.decorators.cache import *


#from django.contrib.auth.models import User

def index(request):
    # if request.user.is_authenticated:
     return render(request, 'index.html')
 

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

        user_profile = None
    if request.user.is_authenticated:
        user_profile = Address.objects.get_or_create(customer=request.user)

    return render(request, 'Customer_Profile.html', {'user_profile': user_profile})

        

@never_cache
@login_required(login_url='login')
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
        # Extract form data from the request
        product_name = request.POST.get('product-name')
        category_name = request.POST.get('category-name')
        subcategory_name = request.POST.get('subcategory-name')
        quantity = request.POST.get('quantity')
        description = request.POST.get('description')
        price = request.POST.get('price')
        discount = request.POST.get('discount')
        sale_price = request.POST.get('sale-price')
        status = request.POST.get('status')
        product_image = request.FILES.get('product-image')

        # Validate form data (you may need to add more validation)
        if not (product_name and category_name and subcategory_name and quantity and
                description and price and discount and sale_price and status and product_image):
            # Handle invalid form data (redirect, show error message, etc.)
            return redirect('add_product')

        # Retrieve or create Category1 instance based on the name (case-insensitive)
        category, created_category = Category1.objects.get_or_create(name__iexact=category_name)
        if not created_category:
            # If the category already exists, you might want to handle this differently,
            # for example, by showing an error message or redirecting back to the form.
            return redirect('add_product')

        # Create or retrieve Subcategory1 instance based on the name and category (case-insensitive)
        subcategory, created_subcategory = Subcategory1.objects.get_or_create(
            name__iexact=subcategory_name,
            category=category
        )

        # Create a new Product1 instance and save it
        product = Product1(
            product_name=product_name,
            category=category,
            subcategory=subcategory,
            stock=quantity,
            description=description,
            price=price,
            discount=discount,
            sale_price=sale_price,
            status=status,
            product_image=product_image
        )
        product.save()

        return redirect('adminpanel')  # Replace 'adminpanel' with the URL name for the admin panel

    return render(request, 'adminpanel.html')


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
        product.product_image = request.POST['product_image']
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






def view_cart(request):
    cart_items = AddToCart2.objects.filter(user=request.user, is_active=True)

    # Calculate order summary
    subtotal = sum(item.product.sale_price * item.quantity for item in cart_items)
    shipping = 10  # Adjust this value as needed
    total = subtotal + shipping
    
    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping': shipping,
        'total': total,
    }
    return render(request, 'view_cart.html', context)

def remove_from_cart(request, item_id):
    item = get_object_or_404(AddToCart2, pk=item_id)

    if item.user == request.user:
        # Remove the item from the cart and the database
        item.delete()

    # Recalculate order summary after item removal
    cart_items = AddToCart2.objects.filter(user=request.user, is_active=True)
    subtotal = sum(item.product.sale_price * item.quantity for item in cart_items)
    shipping = 10  # Adjust this value as needed
    total = subtotal + shipping

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping': shipping,
        'total': total,
    }
    return render(request, 'view_cart.html', context)

@never_cache
@login_required(login_url='login')
def add_to_cart(request, id):
    product = get_object_or_404(Product1, pk=id)
    
    # Check if the product is in stock
    if product.stock <= 0:
        messages.warning(request, f"{product.product_name} is out of stock.")
    else:
        # Get or create a cart item for the user and the selected product
        cart_item, created = AddToCart2.objects.get_or_create(user=request.user, product=product)
        
        if not created:
            # If the cart item already exists, update its quantity and set it as active
            cart_item.is_active = True
            cart_item.quantity += 1
            cart_item.save()
        else:
            # If it's a new item, set it as active
            cart_item.is_active = True
            cart_item.save()
    
    return redirect('view_cart')  

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

def products_by_subcategory(request, subcategory):
    # Retrieve the Subcategory1 object based on the provided subcategory name
    subcategory_obj = get_object_or_404(Subcategory1, name=subcategory)

    # Retrieve products based on the Subcategory1 object
    products = Product1.objects.filter(subcategory=subcategory_obj)

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


def checkout(request):
    user_address = Address.objects.filter(customer=request.user).first()

    return render(request, 'checkout.html', {'user_address': user_address})
    