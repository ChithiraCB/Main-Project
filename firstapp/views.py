
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate ,login as auth_login,logout
from django.contrib import messages
from . models import CustomUser
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







    

