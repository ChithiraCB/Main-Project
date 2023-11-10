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


# Register your models here.

User = get_user_model()

class SuperuserAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return User.objects.filter(is_superuser=True)

# Register the custom admin class
admin.site.register(User,SuperuserAdmin)
