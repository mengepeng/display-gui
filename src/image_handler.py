#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import wx
import cv2
import time
from threading import Thread
from events import Events, ResultEvent
from image_processing import processing_image


class ImageHandler(Thread, wx.EvtHandler):
    def __init__(self, gui):
        Thread.__init__(self)
        wx.EvtHandler.__init__(self)
        self.__gui = gui
        self.__running = True
        self.__start = False
        self.__enable = False
        self.__save = False
        self.__file_path = None
        self.__file_list = None
        self.__file_number = 0
        self.start()

    def run(self):
        while self.__running:
            if self.__start:
                try:
                    img = cv2.imread(self.__file_path)

                    if self.__enable:
                        img_res = processing_image(img)
                    else:
                        img_res = img
                    if self.__save:
                        self._save_image(self._get_save_path(self.__file_path),
                                         img_res)
                    else:
                        pass
                    height, width = img_res.shape[:2]
                    img_res = cv2.cvtColor(img_res, cv2.COLOR_BGR2RGB)
                    bmp = wx.ImageFromBuffer(width, height, img_res)
                    wx.PostEvent(self.__gui,
                                 ResultEvent(Events.EVT_DISPLAY_ID, bmp))
                except Exception:
                    pass
                self.Stop()
            else:
                pass
            time.sleep(0.1)

    def stop(self):
        self.__running = False

    def reset(self):
        self.__start = False
        self.__enable = False
        self.__save = False

    def Start(self):
        self.__start = True
        wx.PostEvent(self.__gui,
                     ResultEvent(Events.EVT_START_STATE_ID, 1))

    def Stop(self):
        self.__start = False
        wx.PostEvent(self.__gui,
                     ResultEvent(Events.EVT_START_STATE_ID, 0))

    def next_file(self):
        self.__file_number += 1
        if self.__file_number == len(self.__file_list) - 1:
            wx.PostEvent(self.__gui, ResultEvent(Events.EVT_NEXT_DONE_ID, 1))
        if self.__file_number == len(self.__file_list):
            wx.PostEvent(self.__gui, ResultEvent(Events.EVT_NEXT_DONE_ID, 0))
            self.__file_number = 0
        try:
            self.__file_path = self.__file_list[self.__file_number]
        except ImportError:
            pass

    def enable_processing(self, control):
        self.__enable = control

    def save_file(self, control):
        self.__save = control

    def set_files(self, files):
        self.__file_list = files
        self.__file_path = files[0]
        self.__file_number = 0
        self.Start()

    @staticmethod
    def _save_image(path, img):
        cv2.imwrite(path, img)

    @staticmethod
    def _get_save_path(path):
        base_path = os.path.abspath("..")
        save_dir = os.path.join(base_path, 'result')
        os.makedirs(save_dir, exist_ok=True)
        (file_path, file_full_name) = os.path.split(path)
        (file_name, file_type) = os.path.splitext(file_full_name)
        save_name = file_name + '_res' + '.jpg'
        return os.path.join(save_dir, save_name)
