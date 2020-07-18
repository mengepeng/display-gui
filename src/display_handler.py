#!/usr/bin/env python
# -*- coding: utf-8 -*-
import wx
import inspect
from image_handler import ImageHandler
from video_handler import VideoHandler
from camera_handler import CameraHandler


def whoami():
    return inspect.stack()[1][3]


class DisplayHandler(wx.EvtHandler):
    __image_handler = None
    __video_handler = None
    __camera_handler = None
    __display_handler = None

    def __init__(self, gui):
        wx.EvtHandler.__init__(self)
        self.__gui = gui
        self._start_threads()

    def _start_threads(self):
        self.__image_handler = ImageHandler(self.__gui)
        self.__video_handler = VideoHandler(self.__gui)
        self.__camera_handler = CameraHandler(self.__gui)
        self.__display_handler = self.__image_handler

    # ########## Interface to GUI ##########
    def start_display(self):
        print(whoami())
        self.__display_handler.Start()

    def stop_display(self):
        print(whoami())
        self.__display_handler.Stop()

    def next_file(self):
        print(whoami())
        self.__display_handler.Stop()
        self.__display_handler.next_file()
        self.__display_handler.Start()

    def enable_processing(self, control=False):
        print(whoami())
        self.__display_handler.enable_processing(control)

    def save_file(self, control=False):
        print(whoami())
        self.__display_handler.save_file(control)

    def set_image(self):
        print(whoami())
        self.__display_handler.Stop()
        self.__display_handler = self.__image_handler
        self.__display_handler.reset()

    def set_video(self):
        print(whoami())
        self.__display_handler.Stop()
        self.__display_handler = self.__video_handler
        self.__display_handler.reset()

    def set_camera(self):
        print(whoami())
        self.__display_handler.Stop()
        self.__display_handler = self.__camera_handler
        self.__display_handler.reset()

    def load_files(self, files):
        print(whoami())
        self.__display_handler.set_files(files)

    def CleanUp(self):
        print(whoami())
        if self.__display_handler:
            self.__display_handler.stop()
        if self.__image_handler:
            self.__image_handler.stop()
        if self.__video_handler:
            self.__video_handler.stop()
        if self.__camera_handler:
            self.__camera_handler.stop()
