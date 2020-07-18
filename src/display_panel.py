#!/usr/bin/env python
# -*- coding: utf-8 -*-
import wx


class DisplayPanel(wx.Panel):
    __img = None
    __bmp = None

    def __init__(self, gui):
        wx.Panel.__init__(self, gui)
        self.__gui = gui
        self.__sizer = wx.BoxSizer()
        self.__panel = wx.Panel(self, -1, style=wx.BORDER_DEFAULT)
        self.__sizer.Add(self.__panel,
                         proportion=10,
                         flag=wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL,
                         border=2)

        self.SetSizerAndFit(self.__sizer)

        self.Bind(wx.EVT_PAINT, self._on_paint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self._on_erase)

    def _on_erase(self, event):
        pass

    def _on_paint(self, event):
        if self.__bmp:
            wx.BufferedPaintDC(self, self.__bmp)
        else:
            wx.BufferedPaintDC(self).Clear()

    def _draw_image(self):
        image = wx.Image(self.__img).Rescale(self.GetSize().width,
                                             self.GetSize().height)
        self.__bmp = wx.Bitmap(image.ConvertToBitmap())
        self.Refresh(False)

    def resize(self):
        if self.__img:
            self._draw_image()
        else:
            pass

    def clear(self):
        self.__img = None
        self.__bmp = None
        self.Refresh(False)

    def display(self, img):
        if img:
            self.__img = img
            self._draw_image()
        else:
            pass
