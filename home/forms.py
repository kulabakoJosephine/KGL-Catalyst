from django.forms import ModelForm
from .models import *
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm

class SaleForm(ModelForm):
    class Meta:
        model = Sales
        fields = ['branch_name', 'seller', 'issued_to', 'quantity', 'unit_price', 'amount_received']


class Deffered_paymentsForm(ModelForm):
    class Meta:
        model = Deffered_payments
        fields = '__all__'  # ✅ Correct special value

        
class StockForm(ModelForm):
    class Meta:
        model = Stock
        fields =   '__all__'

class AddForm(ModelForm):
    class Meta:
        model = Stock
        fields = ['total_quantity']

class UserCreation(UserCreationForm):
    class Meta:
        model = Userprofile
        fields = '__all__'
    def save(self, commit=True):
        user=super( UserCreation,self).save(commit=False)
        if commit:
            user.is_active =True
            user.is_staff =True
            user.save()
            return user
        
from django import forms
from .models import Stock  # Make sure Stock is your model name

class ProductForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['item_name', 'stock_branch_name', 'unit_cost', 'unit_price', 'total_quantity']

        widgets = {
            'item_name': forms.TextInput(attrs={'class': 'form-control'}),
            'stock_branch_name': forms.TextInput(attrs={'class': 'form-control'}),
            'unit_cost': forms.NumberInput(attrs={'class': 'form-control'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_quantity': forms.NumberInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'item_name': 'Item Name',
            'stock_branch_name': 'Branch Name',
            'unit_cost': 'Unit Cost (UGX)',
            'unit_price': 'Unit Price (UGX)',
            'total_quantity': 'Total Quantity (Kgs)',
        }
from django import forms
 # Make sure Stock is your model name

class ProductForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['item_name', 'stock_branch_name', 'unit_cost', 'unit_price', 'total_quantity']

        widgets = {
            'item_name': forms.TextInput(attrs={'class': 'form-control'}),
            'stock_branch_name': forms.TextInput(attrs={'class': 'form-control'}),
            'unit_cost': forms.NumberInput(attrs={'class': 'form-control'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_quantity': forms.NumberInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'item_name': 'Item Name',
            'stock_branch_name': 'Branch Name',
            'unit_cost': 'Unit Cost (UGX)',
            'unit_price': 'Unit Price (UGX)',
            'total_quantity': 'Total Quantity (Kgs)',
        }