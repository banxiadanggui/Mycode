# -*- coding: utf-8 -*-
from wxauto import *
wx=WeChat()
print(wx)
msgs = wx.GetAllMessage()
for msg in msgs:
    if msg.type == 'self':  # 消息类型
        print(msg.content)
