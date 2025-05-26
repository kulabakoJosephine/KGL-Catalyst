from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout as django_logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from .models import Stock, Sales  # Import your models
from .models import Sales
from .forms import SaleForm


from .models import *
from .forms import *
from .filters import StockFilter


def index(request):
    return render(request, 'index.html')


@login_required
def hom(request):
    products = Stock.objects.all().order_by('-id')
    product_filters = StockFilter(request.GET, queryset=products)
    products = product_filters.qs
    return render(request, "hom.html", {
        'products': products,
        'product_filters': product_filters,
        'is_admin': getattr(request.user, 'is_administrator', False)
    })


def register(request):
    return render(request, "register.html")


@login_required
def logout(request):
    return render(request, "logout.html")


@login_required
def log_out(request):
    django_logout(request)
    return redirect('/')


@login_required
def product_detail(request, product_id):
    product = get_object_or_404(Stock, id=product_id)
    return render(request, "product_detail.html", {'product': product})


@login_required
def delete_detail(request, product_id):
    if not request.user.is_manager:
        return HttpResponseForbidden("You are not allowed to delete products.")
    
    # rest of the code...

    """if getattr(request.user, 'is_administrator', False):
        return HttpResponseForbidden("Admins are not allowed to delete products.")"""
    
    product = get_object_or_404(Stock, id=product_id)
    product.delete()
    return HttpResponseRedirect(reverse('hom'))

@login_required
def edit_detail(request, product_id):
    if not request.user.is_manager:
        return HttpResponseForbidden("You are not allowed to edit products.")
    
    # rest of the code...

    """if getattr(request.user, 'is_administrator', False):
        return HttpResponseForbidden("Admins are not allowed to edit products.")"""
    
    
    product = get_object_or_404(Stock, id=product_id)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_detail', product_id=product.id)
    else:
        form = ProductForm(instance=product)

    return render(request, "edit_product.html", {'form': form, 'product': product})


"""@login_required
def add_product(request):
    if getattr(request.user, 'is_administrator', False):
        return HttpResponseForbidden("Admins are not allowed to add products.")
"""
@login_required
def add_product(request):
    if not request.user.is_manager :
        return HttpResponseForbidden("You are not allowed to add products.")
    
    # rest of the code...

    
    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('hom')
    else:
        form = StockForm()
    return render(request, 'add_product.html', {'form': form})


@login_required
def issue_item(request, pk):
    issued_item = get_object_or_404(Stock, id=pk)
    sales_form = SaleForm(request.POST)

    if request.method == 'POST':
        if sales_form.is_valid():
            new_sale = sales_form.save(commit=False)
            new_sale.item = issued_item
            new_sale.unit_price = issued_item.unit_price
            new_sale.save()

            issued_quantity = int(request.POST['quantity'])
            issued_item.total_quantity -= issued_quantity
            issued_item.save()

            return redirect('receipt')

    return render(request, 'issue_item.html', {'sales_form': sales_form})


@login_required
def receipt(request):
    sales = Sales.objects.all()
    sales = Sales.objects.all().order_by('-id')
    return render(request, 'receipt.html', {'sales': sales})


@login_required
def receipt_detail(request, receipt_id):
    receipt = get_object_or_404(Sales, id=receipt_id)
    return render(request, 'receipt_detail.html', {'receipt': receipt})


@login_required
def all_sales(request):
    sales = Sales.objects.all().order_by('-id')
    total_expected = sum([items.get_total() or 0 for items in sales])
    total = sum([items.amount_received or 0 for items in sales])
    total_change = sum([items.get_change() or 0 for items in sales])
    net = total_expected - total
    return render(request, 'all_sales.html', {
        'sales': sales,
        'total': total,
        'total_change': total_change,
        'net': net,
        'total_expected': total_expected
    })


def deffered_payments(request):
    if request.method == 'POST':
        form = Deffered_paymentsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('hom')
    else:
        form = Deffered_paymentsForm()
    return render(request, 'deffered_payments.html', {'form': form})


def deffered_payments_list(request):
    payment = Deffered_payments.objects.all().order_by('-id')
    return render(request, 'deffered_payments_list.html', {'payments': payment})


@login_required
def record_sales(request):
    if request.method == 'POST':
        sales_form = SaleForm(request.POST)
        if sales_form.is_valid():
            item_id = request.POST.get('item')
            issued_item = get_object_or_404(Stock, id=item_id)

            new_sale = sales_form.save(commit=False)
            new_sale.item = issued_item
            new_sale.unit_price = issued_item.unit_price
            new_sale.save()

            issued_quantity = int(request.POST['quantity'])
            issued_item.total_quantity -= issued_quantity
            issued_item.save()

            return redirect('all_sales')

    else:
        sales_form = SaleForm()

    return render(request, 'record_sales.html', {'sales_form': sales_form})


@login_required
def add_to_stock(request, pk):
    issued_item = get_object_or_404(Stock, id=pk)
    form = AddForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            added_quantity = int(request.POST['total_quantity'])
            issued_item.total_quantity += added_quantity
            issued_item.save()
            return redirect('hom')
    return render(request, 'add_to_stock.html', {'form': form})

@login_required
def signup(request):
    if not getattr(request.user, 'is_administrator', False):  # assuming admin = owner
        return HttpResponseForbidden("Only the owner can add users.")
    ...

    if request.method == 'POST':
        form = UserCreation(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/Login')
    else:
        form = UserCreation()
    return render(request, 'signup.html', {'form': form})


def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_administrator:
            login(request, user)
            return redirect('/owner_dashboard')

        if user is not None and user.is_manager:
            login(request, user)
            return redirect('/manager_dashboard')

        if user is not None and user.is_salesagent:
            login(request, user)
            return redirect('/salesagent_dashboard')

        print("Sorry!, something went wrong")

    form = AuthenticationForm()
    return render(request, 'login.html', {"form": form})


@login_required
def owner_dashboard(request):
    receipts = Receipt.objects.all().order_by('-date')
    total_sales = receipts.aggregate(total=Sum('amount_received'))['total'] or 0
    return render(request, 'owner_dashboard.html', {
        'receipts': receipts,
        'total_sales': total_sales
    })


@login_required
def manager_dashboard(request):
    return render(request, 'manager_dashboard.html')


@login_required
def salesagent_dashboard(request):
    return render(request, 'salesagent_dashboard.html')


@login_required
def final_receipt(request, receipt_id):
    if not (request.user.is_administrator or
            (hasattr(request.user, 'profile') and request.user.profile.role == 'owner')):
        return HttpResponseForbidden("You are not authorized to view this receipt.")

    receipt = get_object_or_404(Receipt, id=receipt_id)
    return render(request, 'final_receipt.html', {'receipt': receipt})


#for recording sales

def sales_add(request):
    """View function to handle the sales form submission."""
    
    # Get all available stock items for the dropdown
    stocks = Stock.objects.all()
    
    if request.method == 'POST':
        try:
            # Get form data
            item_id = request.POST.get('item')
            quantity = int(request.POST.get('quantity'))
            unit_price = float(request.POST.get('unit_price'))
            amount_received = float(request.POST.get('amount_received'))
            
            # Validate item exists
            stock = Stock.objects.get(id=item_id)
            
            # Check if sufficient quantity is available
            if quantity > stock.total_quantity:
                return render(request, 'sales/record_sales.html', {
                    'stocks': stocks,
                    'preselected_item': item_id,
                    'quantity_error': f"Only {stock.total_quantity} units available for {stock.item_name}!"
                })
            
            # Calculate total amount
            total_amount = quantity * unit_price
            
            # Check if amount received is sufficient
            if amount_received < total_amount:
                messages.error(request, "Amount received cannot be less than the total amount")
                return render(request, 'sales_form.html', {
                    'stocks': stocks,
                    'preselected_item': item_id
                })
            
            # Save the sale with atomic transaction
            with transaction.atomic():
                # Create sale record
                sale = Sales.objects.create(
                    item=stock,
                    quantity=quantity,
                    unit_price=unit_price,
                    amount_received=amount_received,
                    total_amount=total_amount
                )
                
                # Update stock quantity
                stock.total_quantity -= quantity
                stock.save()
            
            messages.success(request, f"Sale recorded successfully. Change: ${amount_received - total_amount:.2f}")
            return redirect('sales_list')  # Redirect to sales list page
            
        except Stock.DoesNotExist:
            messages.error(request, "Selected product does not exist")
        except ValueError:
            messages.error(request, "Please enter valid numeric values")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
    
    # If GET request or form submission failed, render the form again
    return render(request, 'sales_form.html', {
        'stocks': stocks
    })
#sales list view
def sales_list(request):
    sales = Sales.objects.all()  # Get all sales objects
    return render(request, 'home/sales_list.html', {'sales': sales})


#recording sales
#def record_sales(request):
#    if request.method == 'POST':
#        form = SaleForm(request.POST)
#        if form.is_valid():
 #           form.save()
#            # This redirect is likely missing in your code
 #           return redirect('sales_list')  # or whatever URL you want to go to
   # else:
   ##     form = SaleForm()
    
    #return render(request, 'sales/record_sales.html', {'form': form})

#