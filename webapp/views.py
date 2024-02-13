from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

def home(request):
    #Check to see if loggin in
    if request.method == "POST":
        user_name = request.POST["user_name"]
        password = request.POST["password"]
        #Authenticate login
        user = authenticate(request, username=user_name, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully logged in.")
            return redirect(home)
        else:
            messages.success(request, "Incorrect username or password. Failed to login!")
            return redirect(home)
    else:    
        return render(request, 'home.html', {})
    

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect(home)


def register_user(request):
    return render(request, 'register.html', {})