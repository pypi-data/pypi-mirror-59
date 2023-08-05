#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'zhangyue'

from django.conf import settings
from django.contrib.auth.models import User

from .models import Message, SendRecord
from utils import get_message

# def get_user(request):
#     return get_login_user(request)




# 发送消息，返回结果
def send_message(from_user=None, to_user=None, message_identity=None, title="", info="", url=""):
    try:
        record = SendRecord()
        record.from_user = from_user
        record.to_user = to_user
        record.message = get_message(message_identity)
        record.title = title
        record.info = info
        record.url = url
        record.save()
        return True
    except Exception as e:
        print('bee_django_message->send_message->error:' + e.__str__())
        return False


# 消息状态改为已读信息
# def change_message_stutas(message_record_id):
#     try:
#         record = SendRecord.objects.get(id=message_record_id)
#         record.is_view = True
#         record.save()
#     except:
#         return False
#
# # django前台显示本地时间
# def filter_local_datetime(_datetime):
#     return _datetime