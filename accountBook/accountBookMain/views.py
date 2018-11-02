from django.shortcuts import render, get_object_or_404, redirect
# Create your views here.

from django.http import Http404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *
from django.utils import timezone

from .forms import *
from datetime import datetime
from django.db.models import Avg, Count, Min, Sum


@login_required
def accept_account(request, book_list):
    # return redirect('history_main', history_pk=history_pk)

    book_pk = book_list.split("_")
    pk = request.user.pk

    length = len(book_pk)

    for i in range(0, length-1):
        # 초대테이블 승인업데이트
        invit = Invitation.objects.get(id=book_pk[i])
        invit.auth_ac = 1
        invit.save()

        # 테이블리스트에 인원수 추가
        account_book = AccountBooksName.objects.get(pk=invit.account.account_id)
        person_num = account_book.p_cnt + 1

        account_book.p_cnt = person_num
        account_book.save()

        # 소속 유저 추가
        PartyBelongTo.objects.create(user_id=request.user, account_id=account_book)

    return redirect('myAccount', pk=pk)


@login_required
def invitation_list(request):

    user = request.user.pk

    val = Invitation.objects.filter(receiver=user, auth_ac=0)
    return render(request, 'invitationList.html', {'val': val})


@login_required
def my_account(requst, pk):

    card = Invitation.objects.filter(receiver=pk, auth_ac=0)
    length = len(card)

    return render(requst, "myAccountMain.html", {'card': length})


@login_required
def send_account_invite(request, history, user_list):

    add_user = user_list.split("_")
    temp_pk = request.user.pk
    user = User.objects.get(pk=temp_pk)

    account = AccountBooksName.objects.get(pk=history)

    length = len(add_user)
    for i in range(0, length-1):
        name = User.objects.get(pk=add_user[i])
        Invitation.objects.create(sender=user, receiver=name, account=account)

    account_obj = AccountBooksName.objects.get(account_id=history)
    invit_module = MethodModule()
    val = invit_module.filter_invitation_user(history)

    return render(request, "addAccountUser.html", {'account': account_obj, 'user_list': val})


@login_required
def add_account_user(request, history):
    account_obj = AccountBooksName.objects.get(account_id=history)

    invit_module = MethodModule()
    val = invit_module.filter_invitation_user(history)
    return render(request, "addAccountUser.html", {'account': account_obj, 'user_list': val})


@login_required
def account_user_list(request, history):
    get_obj = PartyBelongTo.objects.filter(account_id=history)

    info_account = get_obj[0].account_id

    length = len(get_obj)
    if length < 2:
        get_obj = False

    return render(request, 'party_list.html', {'user_list': get_obj, 'info': info_account})


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
        save = int()
        current_year = datetime.now().year
        current_month = datetime.now().month

        history = UseList.objects.filter(book_name=history_pk).order_by('-create_at')
        this_month = UseList.objects.filter(book_name=history_pk, create_at__year=current_year, create_at__month=current_month)

        if len(history) > 0:
            for i in history:
                price = i.price
                divide = i.division
                my_val = int(price/divide)
                i.val = my_val

            # 이번달 총액수
            save = 0
            for money in this_month:
                save += money.price

        elif len(history) == 0:
            history = None
            save = 0

        history_name = AccountBooksName.objects.get(pk=history_pk)

    except UseList.DoesNotExist:
        raise Http404
    return render(request, 'history_main.html', {'history': history, 'name': history_name, 'sum': save, 'month': current_month})


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


class MethodModule:

    @staticmethod
    def filter_invitation_user(history):

        all_user = User.objects.all()

        invitation = Invitation.objects.filter(account=history)

        invit = list()
        for i in invitation:
            invit.append(i.receiver)

        all_party = PartyBelongTo.objects.filter(account_id=history)

        party = list()
        for i in all_party:
            party.append(i.user_id)

        show_user = list()
        for i in all_user:
            if not i in invit:
                if not i in party:
                    show_user.append(i)

        length = len(show_user)

        if length == 0:
            val = 0
        else:
            val = show_user

        return val