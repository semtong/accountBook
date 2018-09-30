from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class AccountBooksName(models.Model):
    """
        가계부 리스트 테이블
    """
    account_id = models.AutoField(primary_key=True)
    account_name = models.CharField(max_length=100)
    p_cnt = models.IntegerField(default=0)
    language = models.CharField(max_length=30)  # 언어설정 칼럼
    create_at = models.DateTimeField(auto_now_add=True)


class PartyBelongTo(models.Model):
    """
        가계부에 소속된 사용자 테이블
    """
    user_id = models.ForeignKey(User, related_name='partyBelongTo', on_delete=models.CASCADE)
    account_id = models.ForeignKey(AccountBooksName, related_name='partyBelongTo', on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)


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
    use_list = models.ForeignKey(AccountBooksName, related_name='+', on_delete=models.CASCADE)
    price = models.IntegerField(null=False)
    user = models.ForeignKey(User, related_name='+', on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    del_user = models.ForeignKey(User, related_name='+', on_delete=models.CASCADE)