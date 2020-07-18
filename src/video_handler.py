#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import wx
import cv2
import time
from time import strftime, localtime
from threading import Thread
from events import Events, ResultEvent
from image_processing import processing_image


class VideoHandler(Thread, wx.EvtHandler):
    __cap = None
    __out = None
    __fps = None
    __size = None

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
                if self.__cap.isOpened():
                    ret, frame = self.__cap.read()
                    if ret:
                        if self.__enable:
                            frame_res = processing_image(frame)
                        else:
                            frame_res = frame
                        if self.__save:
                            self.__out.write(frame_res)
                        else:
                            pass
                        height, width = frame_res.shape[:2]
                        frame_res = cv2.cvtColor(frame_res,
                                                 cv2.COLOR_BGR2RGB)

                        bmp = wx.ImageFromBuffer(width, height, frame_res)
                        wx.PostEvent(self.__gui,
                                     ResultEvent(Events.EVT_DISPLAY_ID,
                                                 bmp))
                    else:
                        self.Stop()
                else:
                    pass
                time.sleep(1 / int(self.__fps))
            else:
                time.sleep(0.1)

    def stop(self):
        self._stop_out()
        self._stop_cap()
        self.__running = False

    def reset(self):
        self.__start = False
        self.__enable = False
        self.__save = False

    def Start(self):
        self._start_cap()
        if self.__save:
            self._start_out()
        wx.PostEvent(self.__gui,
                     ResultEvent(Events.EVT_START_STATE_ID, 1))
        self.__start = True

    def Stop(self):
        self._stop_out()
        self._stop_cap()
        wx.PostEvent(self.__gui,
                     ResultEvent(Events.EVT_START_STATE_ID, 0))
        self.__start = False

    def next_file(self):
            self.__cap = None
            self.__out = None
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
        if control:
            self._start_out()
        else:
            self._stop_out()
        self.__save = control

    def set_files(self, files):
        self.Stop()
        self.__file_list = files
        self.__file_path = files[0]
        self.__file_number = 0
        self._stop_out()
        self._stop_cap()
        self.Start()

    # ########## private methods ##########
    def _set_video_cap(self):
        if self.__file_path:
            self.__cap = cv2.VideoCapture(self.__file_path)
            self.__fps = int(self.__cap.get(cv2.CAP_PROP_FPS))
            self.__size = (int(self.__cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                           int(self.__cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        else:
            pass

    def _set_video_out(self):
        if not self.__out:
            fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
            self.__out = cv2.VideoWriter(self._get_save_path(),
                                     fourcc, self.__fps, self.__size)
        else:
            pass

    def _start_cap(self):
        if not self.__cap:
            self._set_video_cap()
        else:
            pass

    def _stop_cap(self):
        if self.__cap:
            self.__cap.release()
            self.__cap = None
        else:
            pass

    def _start_out(self):
        if not self.__out and self.__cap:
            self._set_video_out()
        else:
            pass

    def _stop_out(self):
        if self.__out:
            self.__out.release()
            self.__out = None
        else:
            pass

    @staticmethod
    def _get_save_path():
        base_path = os.path.abspath("..")
        save_dir = os.path.join(base_path, 'result')
        os.makedirs(save_dir, exist_ok=True)
        time_str = strftime("%Y%m%d_%H%M%S", localtime())
        save_name = 'video_' + time_str + '.mp4'
        return os.path.join(save_dir, save_name)

