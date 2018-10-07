from django.shortcuts import render, get_object_or_404, redirect
# Create your views here.

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *


@login_required
def MainView(request):

    get_user = request.user
    get_list = PartyBelongTo.objects.filter(user_id=get_user)

    if len(get_list) == 0:
        get_list = False

    return render(request, 'home.html', {'list': get_list})
