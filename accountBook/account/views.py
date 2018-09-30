from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import SignUpForm
from django.contrib.auth import login as auth_login

# Create your views here.


def sign_up(request):

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})