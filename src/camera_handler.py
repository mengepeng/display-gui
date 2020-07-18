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


def get_base_path(relative):
    base_path = os.path.abspath("..")
    return os.path.join(base_path, relative)


def get_resource_path():
    return get_base_path('resource')


class CameraHandler(Thread, wx.EvtHandler):
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
        self.start()

    def run(self):
        while self.__running:
            if self.__start:
                if self.__cap.isOpened():
                    ret, frame = self.__cap.read()
                    if ret:
                        frame = cv2.flip(frame, 1)
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
                        print(0)
                else:
                    pass
                time.sleep(1 / self.__fps)
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
        pass

    # ########## private methods ##########
    def _set_camera_cap(self):
        self.__cap = cv2.VideoCapture(0)
        self.__fps = int(self.__cap.get(cv2.CAP_PROP_FPS))
        self.__size = (int(self.__cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                       int(self.__cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    def _set_video_out(self):
        fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        self.__out = cv2.VideoWriter(self._get_save_path(),
                                     fourcc, self.__fps, self.__size)

    def _start_cap(self):
        if not self.__cap:
            self._set_camera_cap()
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
