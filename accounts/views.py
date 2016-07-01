from django.shortcuts import render,redirect,reverse,get_object_or_404
from .forms import UserForm,UserRegisterForm
from django.contrib.auth import authenticate,login,logout,get_user_model
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
# Create your views here.

def login_view(request):
    if request.user.is_authenticated:
        return redirect('posts:index')
    form=UserForm(request.POST or None)
    next=request.GET.get('next')
    if form.is_valid():
        username=form.cleaned_data.get('username')
        password=form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user.is_staff:
            login(request, user)
            messages.success(request,'welcome '+user.username,extra_tags='alert alert-success')
            if next:
                return redirect(next)
        return redirect('posts:index')

    context={'form':form,'title':'login'}
    return render(request,'form.html',context)


def register_view(request):
    if request.user.is_authenticated:
        return redirect('posts:index')
    form=UserRegisterForm(request.POST or None)
    if form.is_valid():
        user=form.save(commit=False)
        password=form.cleaned_data.get('password')
        user.set_password(password)
        user.is_active=False
        user.save()
        send_confirmation_email(user)

        #newUser=authenticate(username=user.username,password=password)
        #login(request, newUser)
        #messages.success(request, 'welcome ' + user.username, extra_tags='alert alert-success')
        messages.info(request, 'check email for confirm ' + user.username, extra_tags='alert alert-info')
        return redirect('posts:index')

    context={'form':form,'title':'register'}
    return render(request,'form.html',context)

def confirm(request,id):
    User=get_user_model()
    user=get_object_or_404(User,id=id)
    if not user.is_staff:
        user.is_staff=True
        user.save()
        messages.success(request,'congratulations your are a member',extra_tags='alert alert-success')
        return redirect('posts:index')



def send_confirmation_email(user):
    subject='confirm your email'
    message="http://127.0.0.1:8000%s" % reverse('accounts:confirm',kwargs={'id': user.id})
    from_email=settings.EMAIL_HOST_USER
    to_list=[user.email]
    send_mail(subject,message,from_email,to_list,fail_silently=True)

def logout_view(request):
    logout(request)
    messages.error(request, 'good bye' , extra_tags='alert alert-danger')
    return redirect('accounts:login')