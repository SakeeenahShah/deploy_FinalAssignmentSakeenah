from django.shortcuts import render, redirect, get_object_or_404
from UniformUniverse.models import Customer, Uniform, Order_Details, Review
from datetime import datetime
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.

def index(request):
    return render (request, "index.html")

def sign_up(request):
    user=Customer.objects.all().values()
    if request.method=='POST':
        email=request.POST.get('Email')
        password=request.POST.get('Password')
        CusName=request.POST.get('CustomerName')
        Cusnumber=request.POST.get('PhoneNo')
        address=request.POST.get('Address')

        user=Customer(Email=email, Password=password, CustomerName=CusName, PhoneNo=Cusnumber, Address=address)
        user.save()

        return redirect('sign_in')
    
    return render (request, "sign_up.html")

def sign_in(request):
    if request.method == 'POST':
        email=request.POST.get('Email')
        password=request.POST.get('Password')

        try:
            user=Customer.objects.get(Email=email)
            if user.Password==password:
                return redirect('homepage')
            else:
                return render(request, 'sign_in.html', {'error': 'Invalid Password'})
        except Customer.DoesNotExist:
            return render(request, 'sign_in.html', {'error': 'Account does not exist'})
        
    return render (request,"sign_in.html")

#Direct sign in from index
def sign_in_page(request):
    if request.method == 'POST':
        email=request.POST.get('Email')
        password=request.POST.get('Password')

        try:
            user=Customer.objects.get(Email=email)
            if user.Password==password:
                return redirect('homepage')
            else:
                return render(request, 'sign_in.html', {'error': 'Invalid Password'})
        except Customer.DoesNotExist:
            return render(request, 'sign_in.html', {'error': 'Account does not exist'})
        
    return render(request, "sign_in.html")

def homepage(request):
    uniforms = Uniform.objects.all()
    if not uniforms.exists():
        return render(request, "homepage.html", {'error': 'No Uniforms available for now'})
    return render(request, "homepage.html", {'uniforms': uniforms})  


def checkout(request, uniform_id):
    uniform = get_object_or_404(Uniform, UniformID=uniform_id)
    
    if request.method == 'POST':
        customer_id = request.POST.get('CustomerID') 
        customer_name = request.POST.get('CustomerName')
        address = request.POST.get('Address')
        quantity = int(request.POST.get('Quantity')) 
        total_price = uniform.Price * quantity

        customer = get_object_or_404(Customer, pk=customer_id)
        customer.CustomerName = customer_name
        customer.Address = address
        customer.save()

        # Create order
        order = Order_Details(
            CustomerID=customer,
            UniformID=uniform,
            Quantity=quantity,
            Total_Price=total_price,
            Status='Pending'
        )
        order.save()

        # Update stock
        uniform.Stock -= quantity
        uniform.save()

        return redirect('myorder')  
    
    return render(request, 'checkout.html', {'uniform': uniform})

def myorder(request):
    orders = Order_Details.objects.all()

    for order in orders:
        order.Status = 'Payment Successful'
        order.save()

    orders_with_names = []

    for order in orders:
        customer_name = order.CustomerID.CustomerName
        uniform_name = order.UniformID.UniformName
        orders_with_names.append({
            'OrderID': order.OrderID,
            'CustomerName': customer_name,
            'Address': order.CustomerID.Address,
            'UniformName': uniform_name,
            'Price': order.UniformID.Price,
            'Quantity': order.Quantity,
            'Total_Price': order.Total_Price,
            'Status': order.Status
        })

    return render(request, 'myorder.html', {'orders': orders_with_names})


def update_order_address(request, order_id):
    order = get_object_or_404(Order_Details, OrderID=order_id)
    if request.method == 'POST':
        new_address = request.POST.get('Address')
        order.Address = new_address
        order.save()
        return redirect('myorder')
    return render(request, 'update_order_address.html', {'order': order})

def delete_order(request, order_id):
    order = get_object_or_404(Order_Details, OrderID=order_id)
    order.delete()
    return redirect('myorder')

def review_detail(request, order_id):
    order = get_object_or_404(Order_Details, OrderID=order_id)
    review = Review.objects.filter(OrderID=order).first()
    
    if request.method == 'POST':
        review_id = request.POST.get('review_id')
        review_id_input = request.POST.get('review_id_input')
        
        if review_id:
            review = Review.objects.filter(id=review_id).first()
        elif review_id_input:
            review = Review.objects.filter(ReviewID=review_id_input).first()
    
        description = request.POST.get('description')
        review_date_str = request.POST.get('review_date')
        
        if not description:
            return render(request, 'review_detail.html', {'order': order, 'review': review, 'error': 'Description is required.'})
        
        if not review_date_str:
            return render(request, 'review_detail.html', {'order': order, 'review': review, 'error': 'Review date is required.'})
        
        try:
            review_date = datetime.strptime(review_date_str, '%Y-%m-%d').date()
        except ValueError:
            return render(request, 'review_detail.html', {'order': order, 'review': review, 'error': 'Invalid date format. Please use YYYY-MM-DD.'})
        
        if review:
            # Update existing review
            review.Description = description
            review.Date = review_date
            review.save()
        else:
            # Create new review
            review = Review(
                OrderID=order,
                ReviewID=review_id if review_id else review_id_input,
                Description=description,
                Date=review_date
            )
            review.save()
        
        return redirect('review_detail', order_id=order_id)  
    
    return render(request, 'review_detail.html', {'order': order, 'review': review})


def delete_review(request, order_id):
    order = get_object_or_404(Order_Details, OrderID=order_id)
    review = Review.objects.filter(OrderID=order).first()
    
    if review:
        review.delete()
    
    return redirect('review_detail', order_id=order_id)

def search_uniform(request):
    if request.method == 'GET':
        uniform_id = request.GET.get("c_UniformID")
        if uniform_id:
            try:
                uniform = Uniform.objects.get(UniformID=uniform_id)
                return render(request, 'search_uniform.html', {'data': [uniform]})
            except Uniform.DoesNotExist:
                msg = 'Uniform ID is invalid. Please try again.'
                return render(request, 'search_uniform.html', {'msg': msg})
        else:
            return render(request, 'search_uniform.html')
    else:
        return render(request, 'search_uniform.html')

def search_order(request):
    if request.method == 'GET':
        order_id = request.GET.get('c_OrderID')
        if order_id:
            try:
                order = Order_Details.objects.get(OrderID=order_id)
                return render(request, 'search_order.html', {'data': [order]})
            except Order_Details.DoesNotExist:
                msg = 'Order ID is invalid. Please try again.'
                return render(request, 'search_order.html', {'msg': msg})
        else:
            return render(request, 'search_order.html')
    else:
        return render(request, 'search_order.html')
    
@login_required
def profile(request):
    customer = get_object_or_404(Customer, pk=request.user.pk)
    if request.method == 'POST':
        new_password = request.POST.get('NewPassword')
        customer.Password = make_password(new_password)
        customer.save()
    return render(request, 'profile.html', {'customer': customer})


@login_required
def update_customername(request):
    if request.method == 'POST':
        new_name = request.POST.get('CustomerName')
        customer = get_object_or_404(Customer, pk=request.user.pk)
        customer.CustomerName = new_name
        customer.save()
        return redirect('profile')
    return render(request, 'profile.html')

@login_required
def update_phoneno(request):
    if request.method == 'POST':
        new_phone = request.POST.get('PhoneNo')
        customer = get_object_or_404(Customer, pk=request.user.pk)
        customer.PhoneNo = new_phone
        customer.save()
        return redirect('profile')
    return render(request, 'profile.html')

@login_required
def update_address(request):
    if request.method == 'POST':
        new_address = request.POST.get('Address')
        customer = get_object_or_404(Customer, pk=request.user.pk)
        customer.Address = new_address
        customer.save()
        return redirect('profile')
    return render(request, 'profile.html')

@login_required
def delete_account(request):
    customer = get_object_or_404(Customer, pk=request.user.pk)

    Order_Details.objects.filter(CustomerID=customer).delete()
    Review.objects.filter(OrderID__CustomerID=customer).delete()

    customer.delete()
  
    User.objects.filter(pk=request.user.pk).delete()  

    return redirect('index')  

def uniform_reviews(request, uniform_id):
    uniform = get_object_or_404(Uniform, UniformID=uniform_id)
    reviews = Review.objects.filter(OrderID__UniformID=uniform)
    return render(request, 'uniform_reviews.html', {'uniform': uniform, 'reviews': reviews})



