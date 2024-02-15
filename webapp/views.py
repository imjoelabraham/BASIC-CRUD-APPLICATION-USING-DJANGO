from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import record


def home(request):
    records = record.objects.all()
    # Check to see if loggin in
    if request.method == "POST":
        user_name = request.POST["user_name"]
        password = request.POST["password"]
        # Authenticate login
        user = authenticate(request, username=user_name, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully logged in.")
            return redirect(home)
        else:
            messages.success(request, "Incorrect username or password. Failed to login!")
            return redirect(home)
    else:
        return render(request, 'home.html', {'records': records})


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect(home)


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate and Login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have sucessfully registered.")
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})
    return render(request, 'register.html', {'form': form})


def customer_record(request, pk):
    if request.user.is_authenticated:
        # Look up record
        customer_record = record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record': customer_record})
    else:
        messages.success(request, "You must be logged in to view the page.")
        return redirect('home')


def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_rec = record.objects.get(id=pk)
        delete_rec.delete()
        messages.success(request, "Record successfully deleted.")
        return redirect('home')
    else:
        messages.success(request, "You must be logged in to delete the record.")
        return redirect('home')


def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, "Record added successfully.")
                return redirect('home')
        return render(request, 'add_record.html', {'form': form})
    else:
        messages.success(request, "You must be logged in to add a record.")
        return redirect('home')


def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            add_record = form.save()
            messages.success(request, "Record updated successfully.")
            return redirect('home')
        return render(request, 'update_record.html', {'form': form})
    else:
        messages.success(request, "You must be logged in to update a record.")
        return redirect('home')
