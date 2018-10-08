from django import forms
from .models import *

MONEY_COUNTRY = (
        ('k', "kor"),
        ('j', "jp")
    )


class MakeAccountForm(forms.ModelForm):
    account_name = forms.CharField(
        max_length=100,
        required=True,
        help_text="가계부 이름을 입력해 주세요."
    )

    money = forms.ChoiceField(choices=MONEY_COUNTRY)

    class Meta:
        model = AccountBooksName
        fields = ['account_name', 'money']


class WriteHistory(forms.ModelForm):

    use_history = forms.CharField(
        max_length=450,
        required=True,
        help_text="사용내용을 입력해 주세요."
    )

    price = forms.IntegerField(
        required=True,
        help_text="사용금액을 입력해 주세요.",
    )

    division = forms.IntegerField(
        required=True,
        help_text="사용자 수를 입력해 주세요."
    )

    class Meta:
        model = UseList
        fields = ['use_history', 'price', 'division']