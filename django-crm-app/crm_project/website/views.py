from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm , AddRecordForm
from .models import Record


def home(request):
    records = Record.objects.all()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        ## Authenticate
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('home')
    
    return render(request, 'home.html' , {'records':records})
    

def logout_user(request):
    logout(request)
    messages.success(request, 'You are now logged out')
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User created successfully')
            return redirect('home')
        else:
            messages.error(request, 'An error has occurred during registration')
            return redirect('register')
    else:
        form = SignUpForm()
        return render(request, 'register.html' , {'form': form})

def customer_record(request, pk):
    if request.user.is_authenticated:
        try:
            customer_record = Record.objects.get(id=pk)
        except:
            messages.error(request, 'id is wrong.')
            return redirect('home')
        return render(request, 'record.html', {'customer_record':customer_record})
    else:
        messages.error(request, 'Please log in...')
        return redirect('home')

def delete_record(request,pk):
    if request.user.is_authenticated:
        this_record = Record.objects.get(id=pk)
        this_record.delete()
        messages.success(request, "Record Deleted Successfully.")
        return redirect('home')
    else :
        messages.success(request, "Please log in your account.")
        return redirect('home')
    
def add_record(request):
    if request.user.is_authenticated:
        form = AddRecordForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, "Record Added...")
                return redirect('home')

        return render(request, 'add_record.html', {'form':form})
    else:
        messages.error(request, "You Must Be Logged In...")
        return redirect('home')

def update_record(request , pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None , instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record Has Been Updated!")
            return redirect('home')
        return render(request, 'update_record.html', {'form':form})
    else:
	    messages.error(request, "You Must Be Logged In...")
	    return redirect('home')