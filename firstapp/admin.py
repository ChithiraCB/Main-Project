from django.contrib import admin
from .models import CustomUser
from .models import CustomerProfile
from .models import Category
from .models import Subcategory
from .models import Product


# Register your models here.
admin.site.register(CustomUser),
admin.site.register(CustomerProfile),
admin.site.register(Category),
admin.site.register(Subcategory),
admin.site.register(Product)
