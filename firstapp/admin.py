from django.contrib import admin
from .models import CustomUser
#from .models import CustomerProfile1
from .models import Category1
from .models import Subcategory1
from .models import Product1
from .models import WishlistItem
from .models import AddToCart2
from .models import Profile


# Register your models here.
admin.site.register(CustomUser)
#admin.site.register(CustomerProfile1)
admin.site.register(Category1)
admin.site.register(Subcategory1)
admin.site.register(Product1)
admin.site.register(WishlistItem)
admin.site.register(AddToCart2)
admin.site.register(Profile)
