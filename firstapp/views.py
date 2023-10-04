
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate ,login as auth_login,logout
from django.contrib import messages
from . models import CustomUser
from . models import CustomerProfile
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
                    return redirect('/')
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

def product(request):
    return render(request,'product.html')

def adminpanel(request):
    return render(request, 'adminpanel.html')


def logout_user(request):
    # if request.user.is_authenticated:
    # if 'username' in request.session:
    #     request.session.flush()
    logout(request)
    messages.success(request,("logged out"))
    return render(request, 'logout.html')

# def logout_page(request):
#     return render(request, 'logout.html')

def Customer_Profile(request):
    # Ensure that the user is authenticated
    if not request.user.is_authenticated:
        # Handle the case where the user is not authenticated, e.g., redirect to the login page.
        return redirect('login')  # Replace 'login' with the name of your login view.

    # Get or create the user's profile
    user_profile, created = CustomerProfile.objects.get_or_create(customer=request.user)

    if request.method == 'POST':
        # Handle the POST request for updating user profile fields
        name = request.POST.get('name')
        street_address=request.POST.get('street_address')
        country=request.POST.get('country')
        state=request.POST.get('state')
        pincode=request.POST.get('pincode')
        #last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')

        # Update the user profile fields
        user_profile.name = name
        user_profile.street_address=street_address
        user_profile.country=country
        user_profile.state=state
        user_profile.pincode=pincode
        
        user_profile.phone= phone
        user_profile.save()

        messages.success(request, 'Profile updated successfully')  # Display a success message
        return redirect('Customer_Profile')  # Redirect to the same page or another page after update

    # Handle the GET request for displaying the user profile form
    context = {
        'user_profile': user_profile,
        'form_submitted': False,
    }
    return render(request, 'Customer_Profile.html',context)




    

