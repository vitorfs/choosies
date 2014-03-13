# coding: utf-8
from django.contrib import messages
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from auth.forms import SignUpForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if not form.is_valid():
            context = RequestContext(request, {'form': form})
            return render_to_response('auth/signup.html', context)
        else:
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            User.objects.create_user(username=username, password=password)
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect('/')
    else:
        context = RequestContext(request,  {'form': SignUpForm() })
        return render_to_response('auth/signup.html', context)


def signin(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/')
                else:
                    '''Your account is desactivated.'''
                    context = RequestContext(request)
                    return render_to_response('auth/signin.html', context)
            else:
                '''Username or password invalid.'''
                context = RequestContext(request)
                return render_to_response('auth/signin.html', context)
        else:
            context = RequestContext(request)
            return render_to_response('auth/signin.html', context)

def signout(request):
    logout(request)
    return HttpResponseRedirect('/')