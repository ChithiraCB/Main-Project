from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import CustomUser
#from .models import CustomerProfile1
from .models import Category1
from .models import Subcategory1
from .models import Product1
from .models import WishlistItem
from .models import AddToCart2
from .models import Profile
from .models import Address
from .models import Cart
from .models import CartItem
from .models import Order
from .models import OrderItem
from .models import UserProfile1
from .models import ProfileUser,RentalProduct,RentalAddToCart
#from .models import Payment2



# Register your models here.

# User = get_user_model()

# class SuperuserAdmin(admin.ModelAdmin):
#     def get_queryset(self, request):
#         return User.objects.filter(is_superuser=True)

# Register the custom admin class
#admin.site.register(User,SuperuserAdmin)
admin.site.register(Category1)
admin.site.register(Subcategory1)
admin.site.register(CustomUser)
admin.site.register(Product1)
admin.site.register(AddToCart2)
admin.site.register(WishlistItem)
admin.site.register(Profile)
admin.site.register(Address)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(UserProfile1)
admin.site.register(ProfileUser)
#admin.site.register(Payment2)
admin.site.register(RentalProduct)
admin.site.register(RentalAddToCart)
