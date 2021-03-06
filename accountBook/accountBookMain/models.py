from django.db import models

from django.contrib.auth.models import User

# Create your models here.


class AccountBooksName(models.Model):
    """
        가계부 리스트 테이블
    """

    MONEY_COUNTRY = (
        ('k', "kor"),
        ('j', "jp")
    )

    account_id = models.AutoField(primary_key=True)
    account_name = models.CharField(max_length=100)
    p_cnt = models.IntegerField(default=0)
    money = models.CharField(max_length=1, choices=MONEY_COUNTRY)  # 언어설정 칼럼
    create_at = models.DateTimeField(auto_now_add=True)
    create_user = models.CharField(max_length=100, null=False)


class PartyBelongTo(models.Model):
    """
        가계부에 소속된 사용자 테이블
    """
    user_id = models.ForeignKey(User, related_name='partyBelongTo', on_delete=models.CASCADE)
    account_id = models.ForeignKey(AccountBooksName, related_name='partyBelongTo', on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)


class DemoUser(models.Model):
    """
        데모 사용자 테이블
    """
    account_book = models.ForeignKey(AccountBooksName, related_name="DemoUser", on_delete=models.CASCADE)
    demo_user_id = models.CharField(max_length=100)

    class Meta:
        unique_together = (('account_book', 'demo_user_id'),)


class Invitation(models.Model):
    """
        소속 가계부로 초대
    """
    sender = models.ForeignKey(User, related_name='Invitations', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='+', on_delete=models.CASCADE)
    account = models.ForeignKey(AccountBooksName, related_name='AccountBooksName', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    auth_ac = models.IntegerField(default=0)

    class Meta:
        unique_together = (("sender", "receiver", "account"),)


class UseList(models.Model):
    """
        가계부 사용내역
    """
    book_name = models.ForeignKey(AccountBooksName, related_name='+', on_delete=models.CASCADE)
    use_history = models.CharField(max_length=450, null=False)
    price = models.IntegerField(null=False)
    division = models.IntegerField(null=False)
    num = models.IntegerField(null=False)
    user = models.ForeignKey(User, related_name='+', on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    del_user = models.CharField(max_length=200, blank=True)