from django.shortcuts import render,redirect
from .forms import UserForm,UserRegisterForm
from django.contrib.auth import authenticate,get_user_model,login,logout
from django.contrib import messages
# Create your views here.

def login_view(request):
    form=UserForm(request.POST or None)
    next=request.GET.get('next')
    if form.is_valid():
        username=form.cleaned_data.get('username')
        password=form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        messages.success(request,'welcome '+user.username,extra_tags='alert alert-success')
        if next:
            return redirect(next)
        return redirect('posts:index')

    context={'form':form,'title':'login'}
    return render(request,'form.html',context)


def register_view(request):
    form=UserRegisterForm(request.POST or None)
    if form.is_valid():
        user=form.save(commit=False)
        password=form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        newUser=authenticate(username=user.username,password=password)
        login(request, newUser)
        messages.success(request, 'welcome ' + user.username, extra_tags='alert alert-success')
        return redirect('posts:index')

    context={'form':form,'title':'register'}
    return render(request,'form.html',context)



def logout_view(request):
    logout(request)
    messages.error(request, 'good bye' , extra_tags='alert alert-danger')
    return redirect('accounts:login')