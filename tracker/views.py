from django.shortcuts import render, redirect,get_object_or_404
from django.db import models
from .models import Category, Expense
from .forms import CategoryForm, ExpenseForm,CustomUserCreationForm
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout,login,authenticate
from django.contrib.auth.models import User
from .utils import generate_otp,send_otp_email
from django.core.cache import cache
from .models import OTP,Expense
from .utils import generate_otp, send_otp_email
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
from django.http import HttpResponse

def home(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                request.session['is_verified'] = False
                messages.success(request, 'Login successful. Please verify via OTP.')
                return redirect('send_otp') 
        else:
            messages.error(request, 'Invalid credentials. Please try again.')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            otp = generate_otp()
            OTP.objects.create(email=user.email, otp=otp)
            send_otp_email(user.email, otp)
            messages.success(request, 'Registration successful! Please verify your email.')
            request.session['email'] = user.email
            return redirect('verify_otp')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def send_otp(request):
    email = request.user.email
    otp = generate_otp()

    OTP.objects.update_or_create(email=email, defaults={'otp': otp})
    request.session['email'] = email

    send_otp_email(email, otp)
    messages.success(request, f'OTP has been sent to {email}. Please verify.')
    return redirect('verify_otp')


@login_required
def verify_otp(request):
    email = request.user.email
    if request.method == 'POST':
        otp = request.POST.get('otp')
        try:
            otp_entry = OTP.objects.get(email=email)
            if str(otp_entry.otp) == str(otp) and otp_entry.is_valid():
                request.session['is_verified'] = True
                otp_entry.delete()
                messages.success(request, 'OTP verified successfully!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid or expired OTP. Please try again.')
        except OTP.DoesNotExist:
            messages.error(request, 'No OTP found for this email. Please request a new OTP.')

    return render(request, 'registration/verify_otp.html')

@login_required
def dashboard(request):
    if not request.session.get('is_verified',False):
        messages.error(request, 'You need to verify your OTP first.')
        return redirect('send_otp')
    print(f"User: {request.user}")
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    category_data = (
        expenses.values('category__name') .annotate(total_amount=models.Sum('amount')) .order_by('-total_amount')  
    )

    categories = [entry['category__name'] for entry in category_data]
    amounts = [entry['total_amount'] for entry in category_data]
    print(expenses)
    total_expense = sum(exp.amount for exp in expenses)
    print(f"Total Expense: {total_expense}") 
    return render(request, 'tracker/dashboard.html', {
        'Expenses': expenses,
        'Total_Expense': total_expense
    })

@login_required
def add_expense(request):
    if not request.session.get('is_verified'):
        messages.error(request, 'You need to verify your OTP first.')
        return redirect('send_otp')
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user 
            expense.category = form.cleaned_data['category']
            expense.save()
            return redirect('dashboard')
    else:
        form = ExpenseForm()

    return render(request, 'tracker/add_expense.html', {'form': form})

@login_required
def add_category(request):
    if not request.session.get('is_verified'):
        messages.error(request, 'You need to verify your OTP first.')
        return redirect('send_otp')
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return redirect('dashboard')
    else:
        form = CategoryForm()

    return render(request, 'tracker/add_category.html', {'form': form})

@login_required
def pie_chart_view(request):
    # Example: Group expenses by category and sum amounts
    expenses = Expense.objects.filter(user=request.user)
    categories = expenses.values_list('category__name', flat=True).distinct()
    data = {category: expenses.filter(category__name=category).aggregate(total=models.Sum('amount'))['total'] for category in categories}

    # Generate pie chart
    plt.figure(figsize=(6, 6))
    plt.pie(data.values(), labels=data.keys(), autopct='%1.1f%%', startangle=140)
    plt.title('Spending by Category')

    # Save chart to a BytesIO buffer
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    # Serve the image
    return HttpResponse(buffer, content_type='image/png')

@login_required
def remove_expense(request,expense_id):
    expense=get_object_or_404(Expense,id=expense_id,user=request.user)
    expense.delete()
    return redirect('dashboard')

@login_required
def logout_view(request):
    if request.method == "POST":
        confirm = request.POST.get("confirm")
        if confirm == "yes":
            logout(request)
            messages.success(request, "You have been logged out.")
            return redirect("home")
        else:
            return redirect("dashboard") 

    return render(request, "registration/logout.html")
