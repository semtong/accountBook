from django.shortcuts import render, get_object_or_404, redirect
# Create your views here.

from django.http import Http404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *
from django.utils import timezone

from .forms import *


# @login_required
# def write_history(request, history_pk):
#     try:
#         history = UseList.objects.filter(pk=history_pk)
#         history_name = AccountBooksName.objects.get(pk=history_pk)
#         if len(history) == 0:
#             history = False
#     except UseList.DoesNotExist:
#         raise Http404
#     return render(request, 'history_main.html', {'history': history, 'name': history_name})

@login_required
def write_history(request, history_pk):

    book_name = AccountBooksName.objects.get(pk=history_pk)

    if request.method == 'POST':
        form = WriteHistory(request.POST)
        if form.is_valid():
            regi = form.save(commit=False)
            regi.book_name = AccountBooksName.objects.get(account_id=history_pk)
            regi.user = request.user
            regi.create_at = timezone.now()
            regi.save()

            return redirect('history_main', history_pk=history_pk)
    else:
        form = WriteHistory()
    return render(request, 'write_history.html', {'form': form, 'book_name': book_name})


@login_required
def history_main(request, history_pk):

    try:
        history = UseList.objects.filter(book_name=history_pk).order_by('-create_at')
        history_name = AccountBooksName.objects.get(pk=history_pk)
        if len(history) == 0:
            history = None
    except UseList.DoesNotExist:
        raise Http404
    return render(request, 'history_main.html', {'history': history, 'name': history_name})


@login_required
def main_view(request):

    get_user = request.user
    get_list = PartyBelongTo.objects.filter(user_id=get_user)

    if len(get_list) == 0:
        get_list = False

    # my_list = AccountBooksName.objects.filter(account_name=get_list.account_id)

    return render(request, 'home.html', {'list': get_list})


@login_required
def make_account(request):
    if request.method == 'POST':

        form = MakeAccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.p_cnt = 1
            account.create_at = timezone.now()
            account.create_user = request.user
            account.save()

            PartyBelongTo.objects.create(
                user_id=request.user,
                account_id=form.save(commit=False)
            )

            return redirect('home')
    else:
        form = MakeAccountForm()
    return render(request, 'makeAccount.html', {'form': form})
