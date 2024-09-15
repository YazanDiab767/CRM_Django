from errno import ELOOP

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from  django.contrib import messages

from .forms import SignupForm, AddRecordForm
from .models import Record

def home(request):

    records = Record.objects.all()

    if request.method == 'POST': # If the request is POST
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if (user is not None):
            login(request, user)
            messages.success(request, 'You are now logged in')
        else:
            messages.success(request, 'Invalid Credentials')
        return redirect('home')

    return render(request, 'home.html', {'records': records})



def logout_user(request):
    logout(request)
    messages.success(request, 'You are now logged out')
    return redirect('home')

def register_user(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('home')
    else:
        form = SignupForm()

    return render(request, 'register.html', {"form": form})


def customer_record(request, pk):
    if request.user.is_authenticated:
        record = Record.objects.get(pk=pk)
        return render(request, 'record.html', {"customer_record": record})
    else:
        messages.success(request, 'You must Be Logged In')
        return redirect('home')

def delete_record(request, pk):
    if request.user.is_authenticated:
        record = Record.objects.get(pk=pk)
        record.delete()
        messages.success(request, 'Record Deleted')
        return redirect('home')

def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid():
                record = form.save()
                messages.success(request, 'Record Added')
                return redirect('home')
        return render(request, 'add_record.html', {'form': form})
    else:
        messages.success(request, 'You must Be Logged In')
        return redirect('home')

def update_record(request, pk):
    if request.user.is_authenticated:
        record = Record.objects.get(pk=pk)
        form = AddRecordForm(request.POST or None, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Record Updated')
            return redirect('home')
        return render(request, 'update_record.html', {'form': form})
    else:
        messages.success(request, 'You must Be Logged In')
        return redirect('home')

