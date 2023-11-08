from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    #path('admin/', admin.site.urls),
     path('', views.index,name="index"),
     path('login/', views.login_user,name="login"),
     path('register/', views.register_user,name="register"),
    #  path('product/',views.product_grid,name="product"),
     path('logout/', views.logout_user,name="logout"),
     path('adminpanel/', views.adminpanel,name="adminpanel"),
     path('Customer_Profile/', views.Customer_Profile,name="Customer_Profile"),
     path('add_product/', views.add_product,name="add_product"),
     path('viewproduct/', views.view_product, name='viewproduct'),
     path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
     path('userhome/',views.user_home,name='userhome'),
     #path('addtocart/',views.add_to_cart,name='addtocart'),
    path('product/<int:id>/', views.product_details, name='product_details'),
    path('edit_product/<int:id>/', views.edit_product, name='edit_product'),
     path('change_password/', views.change_password, name='change_password'),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('add_to_cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
     path('user_r', views.user_r, name='user_r'),
     path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    #path('products/<str:subcategory>/Neckpieces/', views.products_by_subcategory, name='products_by_subcategory'),
    path('products-by-subcategory/<str:subcategory>/', views.products_by_subcategory, name='products_by_subcategory'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('add_to_wishlist/<int:id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove_from_wishlist/<int:wishlist_item_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('profile/', views.profile_view, name='profile_view'),



     path('reset_password/', auth_views.PasswordResetView.as_view(), name="reset_password"),
     path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
     path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
     path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
     


    
]

