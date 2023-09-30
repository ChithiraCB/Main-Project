# from django.shortcuts import render,redirect
# from django.contrib.auth import authenticate ,login
# from django.contrib import messages
# from django.contrib.auth.models import User
# # Create your views here.
# def index(request):
#     return render(request, 'index.html')

# def register(request):
#     if request.method == 'POST':
#         username = request.POST.get('fullName')
#         email = request.POST.get('email')  # Add email field
#         phone = request.POST.get('phone')
#         password = request.POST.get('password')
#         confirmPassword = request.POST.get('confirmPassword')
#         my_user = User.objects.create_user(username=username, email=email, password=password)
#         my_user.save()
#         return redirect('login')
           
#     #     # Process the registration form data
#     #     username = request.POST['username']
#     #     email = request.POST['email']
#     #     phone = request.POST['phone']
#     #     password = request.POST['pass']
#     #     confirm_password = request.POST['cpass']
#     #     role = CustomUser.PATIENT  # Set the user role as needed

#     #     if username and email and phone and password and role:
#     #         if CustomUser.objects.filter(email=email).exists():
#     #             error_message = "Email is already registered."
#     #         elif password != confirm_password:
#     #             error_message = "Passwords do not match."
#     #         else:
#     #             # Create a new user
#     #             user = CustomUser(username=username, email=email, phone=phone, role=role)
#     #             user.set_password(password)  # Set the password securely
#     #             user.save()
#     #             # You may want to activate the user's account here or send a confirmation email
#     #             return redirect('login')
#     #     else:
#     #         error_message = "All fields are required."

#     #     return render(request, 'registerUser.html', {'error_message': error_message})

#     # Handle GET request to render the registration form
#     return render(request, 'register.html')

# def login_view(request):
#     if request.method =='POST':
#         email = request.POST["email"]
#         password = request.POST["password"]
#         user = authenticate(request, email=email, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('/index')
#         else:
#             messages.error(request,("there was an error"))
#             return redirect('/login')
#     else:
#         return render(request, 'login.html')
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate ,login as auth_login
from django.contrib import messages
from . models import CustomUser
#from django.contrib.auth.models import User

def index(request):
    return render(request, 'index.html')

# def register_user(request):
#     if request.method == 'POST':
#         username = request.POST.get('email', None)
#         fullName = request.POST.get('fullName', None)
#         phone = request.POST.get('phone', None)
#         password = request.POST.get('password', None)
#         confirmPassword = request.POST.get('confirmPassword', None)
#         # role = CustomUser.CUSTOMER
#         if fullName and username and phone and password:
#              if CustomUser.objects.filter(email=username,username=fullName).exists():
#                  error_message = "Email is already registered."
#                  return render(request, 'register.html', {'error_message': error_message})
#              elif password!=confirmPassword:
#                  error_message = "Password's Don't Match, Enter correct Password"
#                  return render(request, 'register.html', {'error_message': error_message})
#              else:
#                 user = CustomUser(fullName=fullName, email=username, phone=phone)
#                 user.set_password(password)  # Set the password securely
#                 user.is_active=False
#                 user.save()
#                 user_profile = UserProfile(user=user)
#                 user_profile.save()
#                 # activateEmail(request, user, email)
#                 return redirect('login')  
            
#     return render(request, 'register.html')


# def login_user(request):
#      if request.method == 'POST':
#         username = request.POST["username"]
#         password = request.POST["password"]
#          # if user is not None:
#          #     auth_login(request, user)
#          #     return redirect('/userhome')
#          # else:
#          #    messages.success(request,("Invalid credentials."))
#          # print(username)  # Print the email for debugging
#          # print(password)  # Print the password for debugging

#         if username and password:
#              user = authenticate(request,  username=username, password=password)
#              if user is not None:
#                  auth_login(request,user)
            
#                  if request.user.user_type == CustomUser.CUSTOMER:
                
#                      return redirect('/index')
#                  # elif request.user.user_typ == CustomUser.VENDOR:
#                  #     print("user is therapist")
#                  #     return redirect(reverse('therapist'))
#                  elif request.user.user_type == CustomUser.ADMIN:
#                      print("user is admin")                   
#                      return redirect('http://127.0.0.1:8000/admin/')
#                  # else:
#                  #     print("user is normal")
#                  #     return redirect('')

#              else:
#                  messages.success(request,("Invalid credentials."))
#         else:
#              messages.success(request,("Please fill out all fields."))
        
#      return render(request, 'login.html')
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
    
#def login_user(request):
    # if request.user.is_authenticated:
    #     if request.user.user_types == 'CUSTOMER':
    #         return redirect("/")
    #     elif request.user.user_types == 'ADMIN':
    #         return redirect("http://127.0.0.1:8000/admin/")
    #     else:
    #         return redirect("login")

    # from django.contrib.auth import authenticate, login as auth_login
#from django.shortcuts import render, redirect

# def login_user(request):
#     if request.method == "POST":
#         email = request.POST.get("email")
#         password = request.POST.get("password")

#         if email and password:
#             user = authenticate(request, email=email, password=password)

#             if user is not None:
#                 auth_login(request, user)
#                 if user.user_types == 'CUSTOMER':
#                     return redirect('/')
#                 elif user.user_types == 'DELIVERYTEAM':
#                     return redirect("delivery_team_dashboard")  # Replace with the correct URL
#                 else:
#                     return redirect("login")
#             else:
#                 error_message = "Invalid login credentials."
#                 return render(request, "login.html", {"error_message": error_message})
#         else:
#             error_message = "Please fill out all fields."
#             return render(request, "login.html", {"error_message": error_message})

#     return render(request, "login.html")
def login_user(request):
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
                
                    return redirect('/')
                # elif request.user.user_typ == CustomUser.VENDOR:
                #     print("user is therapist")
                #     return redirect(reverse('therapist'))
                elif request.user.user_types == CustomUser.ADMIN:
                    print("user is admin")                   
                    return redirect('http://127.0.0.1:8000/admin/')
                # else:
                #     print("user is normal")
                #     return redirect('')

            else:
                messages.success(request,("Invalid credentials."))
        else:
            messages.success(request,("Please fill out all fields."))
        
    return render(request, 'login.html')


# def logout_user(request):






# def login_user(request):
#      if request.method == 'POST':
#          username = request.POST.get('username')
#          password = request.POST.get('password')
#          print(username,password)

#          if username and password:
#              user = authenticate(request, username=username, password=password)
#              print("authenticated")

#              if user is not None:
               
#                  auth_login(request, user)
#                  # Redirect based on user_type
#                  if user.user_types == CustomUser.ADMIN:
#                      return redirect(reverse('admin'))
#                  elif user.user_types == CustomUser.CUSTOMER:
#                      return redirect(reverse('index'))
#                  # elif user.role == CustomUser.DOCTOR:
#                  #     return redirect(reverse('doctordashbord'))
#                  else:
#                      return redirect('/')
                
#              else:
#                  return HttpResponseRedirect(reverse('login') + '?alert=invalid_credentials')
#          else:
#              return HttpResponseRedirect(reverse('login') + '?alert=fill_fields')

#      # For GET requests or if authentication fails, display the login form
#      return render(request, 'login.html')
# # def userLogout(request):
# #     logout(request)
# #     return redirect('http://127.0.0.1:8000/') 



# # def logout_user(request):
# #     logout(request)
# #     messages.success(request,("Logged out"))
# #     return  redirect('userhome')

    

