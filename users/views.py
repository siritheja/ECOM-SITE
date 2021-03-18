from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistrationForm

# Create your views here.

def register(request):
    if request.method == "POST":
        #POST REQUEST
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            messages.success(request,f'Welcome {username} , your account is created')
            form.save()
            return redirect('login')
    else :
        form = RegistrationForm()
    return render(request,'users/register.html',{'form':form})