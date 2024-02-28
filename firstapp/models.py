from django.db import models
from datetime import date
from django.contrib.auth.models import AbstractUser,BaseUserManager

# # Create your models here.

class UserManager(BaseUserManager):
      def create_user(self, fullName, phone, email, password=None):
          if not email:
              raise ValueError('User must have an email address')

          user = self.model(
              email=self.normalize_email(email),
              fullName=fullName,
              #last_name=last_name,
              phone=phone 
          )
          user.set_password(password)
          user.save(using=self._db)
          return user

      def create_superuser(self,username, phone,email,password=None):
        
          user = self.create_user(
               email=self.normalize_email(email),
               password=password,
               username=username,
               phone=phone
               #last_name=last_name,
               )
          user.is_admin = True
          user.is_active = True
          user.is_staff = True
          user.is_superadmin = True
          user.role=1
          user.save(using=self._db)
          return user

class CustomUser(AbstractUser):
    ADMIN = 1
    CUSTOMER = 2
    DELIVERYTEAM = 3
    #ADMIN = 4

    USER_TYPES = (
        (ADMIN, 'Admin'),
        (CUSTOMER, 'Customer'),
        (DELIVERYTEAM, 'Deliveryteam')
        #(ADMIN,'Admin'),
    )

    #username=None
    user_types = models.PositiveSmallIntegerField(choices=USER_TYPES,default='2')
    fullName = models.CharField(max_length=50)
    #last_name = models.CharField(max_length=50)
    #USERNAME_FIELD = 'email'
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=12, blank=True)
    password = models.CharField(max_length=128)
   # confirmPassword = models.CharField(max_length=128)
    #role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE, blank=True, null=True,default='1')


    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)

    
    #REQUIRED_FIELDS = ['first_name','last_name', 'phone']

    objects = UserManager()

    def str(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True



class UserProfile(models.Model):

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='media/profile_picture', blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    addressline1 = models.CharField(max_length=50, blank=True, null=True)
    addressline2 = models.CharField(max_length=50, blank=True, null=True)
    # country = models.CharField(max_length=15, default="India", blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    pin_code = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(max_length=50, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    profile_created_at = models.DateTimeField(auto_now_add=True)
    profile_modified_at = models.DateTimeField(auto_now=True)


    def calculate_age(self):
        today = date.today()
        age = today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
        return age
    age = property(calculate_age)


    def get_gender_display(self):
        return dict(self.GENDER_CHOICES).get(self.gender)

    def str(self):
        return self.user.email
    
    def get_role(self): 
        if self.user_type == 2:
            user_role = 'Customer'
        elif self.user_type == 3:
            user_role = 'Deliveryteam'
        
        return user_role
    


class CustomerProfile1(models.Model):

    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None)
    fullName = models.CharField(max_length=100)
    street_address=models.CharField(max_length=100,null=True,blank=True)
    country = models.CharField(max_length=15, default="India", blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    pincode = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=10,blank=True, null=True)

    def str(self):
        return self.user.email 
    


# class Category(models.Model):
#     #cat_id = models.AutoField(primary_key=True)
#     cat_name = models.CharField(max_length=100, primary_key=True, unique=True)

#     def __str__(self):
#         return self.cat_name

# class Subcategory(models.Model):
#     # subcat_id = models.AutoField(primary_key=True)
#      subcat_name = models.CharField(max_length=100, primary_key=True, unique=True)
#      cat_name= models.ForeignKey(Category, on_delete=models.CASCADE)

#      def __str__(self):
#         return self.subcat_name
    

# class Product(models.Model):
    
#     product_id = models.AutoField(primary_key=True)
#     product_name = models.CharField(max_length=255)
#     #category = models.ForeignKey(Category, on_delete=models.CASCADE)  # Use ForeignKey to relate to Category
#     #subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)  # Use ForeignKey to relate to Subcategory
#     stock = models.PositiveIntegerField(default=1, null=True)
#     description = models.TextField()
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
#     sale_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
#     product_image = models.ImageField(upload_to='product_images/')
#     STATUS_CHOICES = [
#         ('In Stock', 'In Stock'),
#         ('Out of Stock', 'Out of Stock'),
#     ]

#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='In Stock')

#     def save(self, *args, **kwargs):
#         # Update the status based on the quantity value
#         if self.stock == 0:                                                                                                                                                                 
#             self.status = 'Out of Stock'
#         else:
#             self.status = 'In Stock'

#         # Convert self.discount to a float and then calculate the sale price
#         self.discount = float(self.discount)  # Convert to float
#         self.price = float(self.price)  # Convert to float
#         self.sale_price = self.price - (self.price * (self.discount / 100))

#         super(Product, self).save(*args, **kwargs)


#     def _str_(self):
#         return self.product_name




class Category1(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Subcategory1(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category1, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Product1(models.Model):
    
    product_name = models.CharField(max_length=255)
    category = models.ForeignKey(Category1, on_delete=models.CASCADE)  # Use ForeignKey to relate to Category
    subcategory = models.ForeignKey(Subcategory1, on_delete=models.CASCADE)  # Use ForeignKey to relate to Subcategory
    stock = models.PositiveIntegerField(default=1, null=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    product_image = models.ImageField(upload_to='product_images/')
    STATUS_CHOICES = [
        ('In Stock', 'In Stock'),
        ('Out of Stock', 'Out of Stock'),
    ]


    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='In Stock')

    def save(self, *args, **kwargs):
        # Update the status based on the quantity value
        if self.stock == 0:                                                                                                                                                                 
            self.status = 'Out of Stock'
        else:
            self.status = 'In Stock'

        # Convert self.discount to a float and then calculate the sale price
        self.discount = float(self.discount)  # Convert to float
        self.price = float(self.price)  # Convert to float
        self.sale_price = self.price - (self.price * (self.discount / 100))

        super(Product1, self).save(*args, **kwargs)


    def _str_(self):
        return self.product_name
    
class WishlistItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey('Product1', on_delete=models.CASCADE)

    def __str__(self):
        return self.product.product_name
    
class AddToCart2(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product1, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
     return f"{self.quantity} x {self.product.product_name} in {self.user.username}'s cart"
    
class Profile(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None)
    fullName = models.CharField(max_length=255)
    gender = models.CharField(max_length=10, choices=[("male", "Male"), ("female", "Female")])
    date_of_birth = models.DateField(null=True, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.email
    
class Address(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE,default=None)
    fullName = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    pincode = models.CharField(max_length=10)
    address = models.TextField()
    landmark = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    address_type = models.CharField(
        max_length=10,
        choices=[('home', 'Home'), ('work', 'Work'), ('other', 'Other')]
    )
    def __str__(self):
        return self.fullName


class UserProfile1(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address_line_1 = models.CharField(blank=True, max_length=100)
    address_line_2 = models.CharField(blank=True, max_length=100)
    city = models.CharField(blank=True, max_length=20)
    state = models.CharField(blank=True, max_length=20)
    country = models.CharField(blank=True, max_length=20)
    pincode = models.CharField(blank=True,max_length=10)

    def __str__(self):
        return self.user.fullName

    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'

class CartItem(models.Model):
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)
    product = models.ForeignKey(Product1, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.product_name}"

class Cart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product1, through='CartItem')

    def __str__(self):
        return f"Cart for {self.user.fullName}"
    
# class Payments(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     payment_id = models.CharField(max_length=100)
#     payment_method = models.CharField(max_length=100)
#     amount_paid = models.CharField(max_length=100) # this is the total amount paid
#     payment_status = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.payment_id
    
# class Payment2(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     payment_id = models.CharField(max_length=100)
#     payment_method = models.CharField(max_length=100)
#     amount_paid = models.CharField(max_length=100) # this is the total amount paid
#     payment_status = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.payment_id
    
    

class Order(models.Model):
     
     STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )
     
     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
     products = models.ManyToManyField(Product1, through='OrderItem')
     total_amount = models.DecimalField(max_digits=10, decimal_places=2)
     #payment = models.ForeignKey(Payment2, on_delete=models.SET_NULL, blank=True, null=True)
     payment_id= models.CharField(blank=True, max_length=100, null=True)
     payment_status= models.BooleanField(default=False)
     status = models.CharField(max_length=10, choices=STATUS, default='New')
     created_at = models.DateTimeField(auto_now_add=True)
    
     def __str__(self):
        return f"Order {self.id} by {self.user.fullName}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    #payment = models.ForeignKey(Payment2, on_delete=models.SET_NULL, blank=True, null=True)
    product = models.ForeignKey(Product1, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    item_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.product_name} in Order {self.order.id}"
    

class ProfileUser(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    fullName = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)  # New field
    state = models.CharField(max_length=50, blank=True, null=True)  # New field

    def _str_(self):
        return self.user.fullName
    

    
class RentalProduct(models.Model):
    rental_product_name = models.CharField(max_length=255)
    category = models.ForeignKey(Category1, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory1, on_delete=models.CASCADE)
    stock = models.IntegerField()
    description = models.TextField()
    rental_price = models.DecimalField(max_digits=10, decimal_places=2)
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=(('active', 'Active'), ('inactive', 'Inactive')))
    image = models.ImageField(upload_to='rental_product_images/')

    def __str__(self):
        return self.name
    
class RentalAddToCart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rental_product = models.ForeignKey(RentalProduct, on_delete=models.CASCADE)  # Changed to RentalProduct
    quantity = models.PositiveIntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.quantity} x {self.rental_product.rental_product_name} in {self.user.username}'s cart"
    

    

class RentalCartItem(models.Model):
    cart = models.ForeignKey('RentalCart', on_delete=models.CASCADE)
    rental_product = models.ForeignKey(RentalProduct, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.rental_product.rental_product_name}"

class RentalCart(models.Model):
    rental_cart_user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    rental_products = models.ManyToManyField(RentalProduct, through='RentalCartItem')

    def __str__(self):
        return f"RentalCart for {self.rental_cart_user.fullName}"

class RentalOrder(models.Model):
     
     STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )
     
     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
     rental_products = models.ManyToManyField(RentalProduct, through='RentalOrderItem')
     total_amount = models.DecimalField(max_digits=10, decimal_places=2)
     #payment = models.ForeignKey(Payment2, on_delete=models.SET_NULL, blank=True, null=True)
     payment_id= models.CharField(blank=True, max_length=100, null=True)
     payment_status= models.BooleanField(default=False)
     status = models.CharField(max_length=10, choices=STATUS, default='New')
     created_at = models.DateTimeField(auto_now_add=True)
    
     def __str__(self):
        return f"RentalOrder {self.id} by {self.user.fullName}"
    
class RentalOrderItem(models.Model):
    order = models.ForeignKey(RentalOrder, on_delete=models.CASCADE)
    #payment = models.ForeignKey(Payment2, on_delete=models.SET_NULL, blank=True, null=True)
    rental_product = models.ForeignKey(RentalProduct, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    item_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.rental_product.rental_product_name} in RentalOrder {self.order.id}"
    
# class RentalOrder1(models.Model):
     
#      STATUS = (
#         ('New', 'New'),
#         ('Accepted', 'Accepted'),
#         ('Completed', 'Completed'),
#         ('Cancelled', 'Cancelled'),
#     )
     
#      user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#      #rental_products = models.ManyToManyField(RentalProduct, through='RentalOrderItem')
#      total_amount = models.DecimalField(max_digits=10, decimal_places=2)
#      #payment = models.ForeignKey(Payment2, on_delete=models.SET_NULL, blank=True, null=True)
#      payment_id= models.CharField(blank=True, max_length=100, null=True)
#      payment_status= models.BooleanField(default=False)
#      status = models.CharField(max_length=10, choices=STATUS, default='New')
#      created_at = models.DateTimeField(auto_now_add=True)
    
#      def __str__(self):
#         return f"RentalOrder1 {self.id} by {self.user.fullName}"
    
# class RentalOrderItem1(models.Model):
#     order = models.ForeignKey(RentalOrder1, on_delete=models.CASCADE)
#     #payment = models.ForeignKey(Payment2, on_delete=models.SET_NULL, blank=True, null=True)
#     rental_product = models.ForeignKey(RentalProduct, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)
#     item_total = models.DecimalField(max_digits=10, decimal_places=2)

#     def __str__(self):
#         return f"{self.quantity} x {self.rental_product.rental_product_name} in Order {self.order.id}"
    
