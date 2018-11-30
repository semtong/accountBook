from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(AccountBooksName)   # 가계부리스트
admin.site.register(PartyBelongTo)      # 가계부 소속 유저
admin.site.register(Invitation)         # 가계부 초대
admin.site.register(UseList)            # 가계부 사용내역
admin.site.register(DemoUser)           # 가상사용자