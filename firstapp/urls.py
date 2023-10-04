from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    #path('admin/', admin.site.urls),
     path('', views.index,name="index"),
     path('login/', views.login_user,name="login"),
     path('register/', views.register_user,name="register"),
     path('product/',views.product,name="product"),
     path('logout/', views.logout_user,name="logout"),
     path('adminpanel/', views.adminpanel,name="adminpanel"),
     path('Customer_Profile/', views.Customer_Profile,name="Customer_Profile"),

  


     path('reset_password/', auth_views.PasswordResetView.as_view(), name="reset_password"),
     path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
     path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
     path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
     


    
]

