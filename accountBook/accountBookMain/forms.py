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

"""
     message = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 5, 'placeholder': 'What is on your mind?'}
        ),
        max_length=4000,
        help_text='The max length of the text is 4000.'
    )

            class Meta:
            model = Topic
            fields = ['subject', 'message']
"""
