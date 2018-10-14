from django.shortcuts import render, get_object_or_404, redirect
# Create your views here.

from django.http import Http404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *
from django.utils import timezone

from .forms import *


def save_account_user(request, user, history):
    print('kkkkk')


@login_required
def add_account_user(request, history):
    account_obj = AccountBooksName.objects.get(account_id=history)

    all_user = User.objects.all()

    return render(request, "addAccountUser.html", {'account': account_obj, 'users': all_user})


@login_required
def account_user_list(request, history):
    get_obj = PartyBelongTo.objects.filter(account_id=history)

    info_account = get_obj[0].account_id

    user_list = list()
    for i in get_obj:
        user_id = i.user_id
        user_info = User.objects.get(username=user_id)
        user_list.append(user_info)

    if len(user_list) == 1:
        user_list = False
    else:
        pass

    return render(request, 'party_list.html', {'user_list': user_list, 'info': info_account})


@login_required
def write_history(request, history_pk):

    book_name = AccountBooksName.objects.get(pk=history_pk)
    temp_p = AccountBooksName.objects.filter(account_id=history_pk)
    people = str(temp_p[0].p_cnt)

    if request.method == 'POST':
        form = WriteHistory(request.POST)
        if form.is_valid():
            regi = form.save(commit=False)
            regi.book_name = AccountBooksName.objects.get(account_id=history_pk)
            regi.user = request.user
            regi.num = people
            regi.create_at = timezone.now()
            regi.save()

            return redirect('history_main', history_pk=history_pk)

    else:
        # form = WriteHistory(my_arge=history_pk)
        form = WriteHistory()
    return render(request, 'write_history.html', {'form': form, 'book_name': book_name, 'people': people})


@login_required
def history_main(request, history_pk):

    try:
        history = UseList.objects.filter(book_name=history_pk).order_by('-create_at')
        if len(history) > 0:
            for i in history:
                price = i.price
                divide = i.division
                my_val = int(price/divide)
                i.val = my_val

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
