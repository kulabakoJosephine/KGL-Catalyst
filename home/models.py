from django.db import models
from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser,Group,Permission  
from django.utils import timezone


# Create your models here.

class Userprofile(AbstractUser):
    is_salesagent = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    is_administrator = models.BooleanField(default=False)
    username = models.CharField(max_length=150, unique=True)
    user_email = models.EmailField(max_length= 25, unique=False)
    user_address = models.CharField(max_length=50, blank=False)
    gender = models.CharField(max_length=20, blank=False)
    phonenumber = models.CharField(max_length=20,blank=False)


    def _str_(self):
        return self.username

        # Override default reverse accessors to avoid conflicts
    groups = models.ManyToManyField(
        Group,
        related_name="userprofile_groups",
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups"
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="userprofile_permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions"
    )
    
class Stock(models.Model):
    item_name=models.CharField(max_length=50, null = True, blank=False)
    stock_branch_name=models.CharField(max_length=50, null = True, blank=False)
    stock_type=models.CharField(max_length=50, null = True, blank=False)
    stock_time_of_arrival=models.CharField(max_length=50, null = True, blank=False)
    created_at =models.DateTimeField(auto_now_add=True,null=True)
    supplier_contact=models.CharField(max_length=50, null = True, blank=False)
    stock_source = models.CharField(max_length=50, null = True, blank=False)
    unit_cost = models.IntegerField(default=10, null = True, blank=False)
    unit_price = models.IntegerField(default=0, null = True, blank=False)
    total_quantity = models.IntegerField(default=0, null = True, blank=False)
    issued_quantity = models.IntegerField(default=0, null = True, blank=False)
    def _str_(self):
        return self.item_name

   
#we have created one classs that suites a given table
#above is a table head

#used by the sales agent.
# associating property "item" wz the stock kept in the "Stockx" model or table.
class Sales(models.Model):
    branch_name = models.CharField(max_length=50, null =True, blank=False)
    seller = models.CharField(max_length=50, null =True, blank=False)
    item = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=10, null=True, blank=False)
    amount_received = models.IntegerField(default=10, null=True, blank=False)
    issued_to = models.CharField(max_length=50, null=True, blank=False)
    unit_price = models.IntegerField(default=10, null=True, blank=False)
    date_of_sales = models.DateField(default=datetime.now())


#defining a method

    def get_total(self):
        # Ensure both quantity and unit_price are valid
        if self.quantity is None or self.item.unit_price is None:
            return 0  # Return 0 if either value is None
        total = self.quantity * self.item.unit_price
        return int(total)


    def get_change(self):
        if self.quantity is None or self.item.unit_price is None:
            return 0 
        change = self.get_total() - self.amount_received
        return abs(int(change))
    

    def _str_(self):
        return self.item.item_name


class Deffered_payments(models.Model):
    customer_name = models.CharField(max_length=50, null=True, blank=False)
    contact = models.IntegerField(null=True, blank=False)
    address = models.CharField(max_length=50, null=True, blank=False)
    nin = models.CharField(max_length=50, null=True, blank=True)
    item_bought = models.CharField(max_length=50, null=True, blank=False)
    quantity = models.IntegerField(default=10, null=True, blank=False)
    unit_price = models.IntegerField(default=10, null=True, blank=False)
    amount = models.IntegerField(default=0, null=True, blank=False)
    balance = models.IntegerField(default=0, null=True, blank=False)
    date_of_payment = models.DateTimeField(auto_now_add=True, null=True)
    branch = models.CharField(max_length=50, null=True, blank=False)
    agent = models.CharField(max_length=50, null=True, blank=False)
    # if i use created_at i eliminate time field
    created_at =models.DateTimeField(auto_now_add=True,null=True)



    def _str_(self):
        return self.customer_name
     

class Receipt(models.Model):
    issued_to = models.CharField(max_length=100)  # Customer name
    item = models.CharField(max_length=100)       # Item name
    quantity = models.FloatField()                # e.g. in kilograms
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    amount_received = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(default=timezone.now)

    def get_total(self):
        return round(self.quantity * self.price_per_unit, 2)

    def get_change(self):
        return round(self.amount_received - self.get_total(), 2)

    def _str_(self):
        return f"Receipt for {self.issued_to} on {self.date.strftime('%Y-%m-%d')}"


