#!/usr/bin/env python
# -*- coding: utf-8 -*-
import wx


class Events:
    EVT_RESIZE_ID = wx.NewId()
    EVT_NEXT_DONE_ID = wx.NewId()
    EVT_DISPLAY_ID = wx.NewId()
    EVT_START_STATE_ID = wx.NewId()


def EVT_INIT(instance, id, func):
    instance.Connect(-1, -1, id, func)


class ResultEvent(wx.PyEvent):
    def __init__(self, id, data):
        wx.PyEvent.__init__(self)
        self.SetEventType(id)
        self.__data = data

    def GetData(self):
        return self.__data
