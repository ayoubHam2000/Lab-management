from django.shortcuts import render, redirect

from django.urls import reverse


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect( reverse('Account:home') )
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func



def allowed_users(allowed_roles = []):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            #print("--Check")
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name  
            print(group)
            if group in allowed_roles: 
                return view_func(request, *args, **kwargs)
            else:
                return render(request, 'Error/unauthorized.html')
        return wrapper_func
    return decorator


def dedicated(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name  
        if group == 'admin':
            return redirect(reverse('Account:home'))
        if group == 'encadrant':
            return redirect(reverse('Account:home'))
        if group == 'doctorant':
            return redirect(reverse('Account:home'))
        return redirect(reverse('Account:home'))
    return wrapper_func