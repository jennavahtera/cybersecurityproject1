from django.contrib.auth import login, authenticate, logout, get_user_model
from django.shortcuts import render, redirect, reverse
from .forms import UserRegisterForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# FLAW: OWASP A09:2021 – Security Logging and Monitoring Failures; CWE-778 Insufficient Logging
# (No logging at all is happening)
# FIX: adding a logger and logger warnings when someone tries to login with invalid credentials

#import logging
#logger = logging.getLogger(__name__)

User = get_user_model()

def index(request):
    return render(request, 'polls/all_polls.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect(reverse('polls:all_polls'))
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':

        # FLAW: OWASP A01:2021 – Broken Access Control; CWE-200 Exposure of Sensitive Information to an Unauthorized Actor
        # (An unauthorised user can get information about other users when not logged in, message shows "Invalid username" or "Invalid password")
        # FIX: Using Django's own authentication and using error messages that don't give out information

        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, "Invalid username.")
            form = AuthenticationForm(request)
            return render(request, 'users/login.html', {'form': form})
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse('polls:all_polls'))
        else:
            messages.error(request, "Invalid password.")
            form = AuthenticationForm(request)
            return render(request, 'users/login.html', {'form': form})

        #form = AuthenticationForm(request, data=request.POST)
        #if form.is_valid():
        #    username = form.cleaned_data.get('username')
        #    password = form.cleaned_data.get('password')
        #    user = authenticate(username=username, password=password)

        #    if user is not None:
        #       login(request, user)
        #        return redirect(reverse('polls:all_polls'))
        #    else:
        #        messages.error(request, "Invalid username or password.")
        #        #logger.warning("User " + username + " tried logging in with wrong credentials")
        #else:
        #    #username = form.cleaned_data.get('username')
        #    #logger.warning("User " + username + " tried logging in with wrong credentials")
        #    messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('/users/login')