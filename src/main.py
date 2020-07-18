#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Project     : display_gui
@Author      : Meng Peng
@Date        : 20-06-2020
@Description : select image or video or camera and display in GUI
"""
import os
import sys
import wx
import wx.adv
try:
    from agw import aui
except ImportError:
    import wx.lib.agw.aui as aui

from display_panel import DisplayPanel
from events import Events, EVT_INIT
from display_handler import DisplayHandler


BASE_DIR = os.path.dirname(__file__)


ID_QUIT = wx.ID_EXIT
ID_START = wx.NewId()
ID_NEXT = wx.NewId()
ID_SAVE = wx.NewId()
ID_ENABLE = wx.NewId()
ID_IMAGE = wx.NewId()
ID_VIDEO = wx.NewId()
ID_CAMERA = wx.NewId()
ID_SELECT = wx.NewId()


def get_base_path(relative):
    base_path = os.path.abspath("..")
    return os.path.join(base_path, relative)


def get_image_path(filename):
    return get_base_path(os.path.join('image', filename))


def get_resource_path():
    return get_base_path('resource')


class DisplayGUI(wx.Frame):
    __start = False
    __resource_id = None
    __image_files = None
    __video_files = None
    __image_wildcard = u"JPG and PNG files(*.jpg;*.png)|*.jpg;*.png|" \
                       u"JPG files(*.jpg)|*.jpg|" \
                       u"PNG files(*.png)|*.png|" \
                       u"BMP files(*.bmp)|*.bmp|" \
                       u"All files (*.*)|*.*"
    __video_wildcard = u"MP4 and AVI files(*.mp4;*.avi)|*.mp4;*.avi|" \
                       u"MP4 files(*.mp4)|*.mp4|" \
                       u"AVI files(*.avi)|*.avi|" \
                       u"All files (*.*)|*.*"

    def __init__(self):
        wx.Frame.__init__(self, None,
                          title='Display Tool',
                          size=((wx.DisplaySize()[0]), (wx.DisplaySize()[1])),
                          pos=(0, 0))

        self._init_gui()

        self.__handler = DisplayHandler(self)
        EVT_INIT(self, Events.EVT_DISPLAY_ID, self.OnDisplay)
        EVT_INIT(self, Events.EVT_NEXT_DONE_ID, self.OnNextDone)
        EVT_INIT(self, Events.EVT_START_STATE_ID, self.OnStartState)

        self.SetIcon(wx.Icon(get_image_path("icon.png"), wx.BITMAP_TYPE_ANY))

    def _init_gui(self):
        print('Running ', str(sys.argv))

        self._create_menu()

        self.__mgr = aui.AuiManager()
        self.__mgr.SetManagedWindow(self)
        self.__mgr.SetDockSizeConstraint(0.5, 0.5)

        self._create_toolbar()
        self._create_display_panel()

        self.__mgr.Update()

        self._default_size = (600, 500)
        self._min_size = (350, 350)
        self.SetSize(self._default_size)
        self.SetMinSize(self._min_size)
        self.Center()
        self.Show()

    def _create_menu(self):
        self.__menubar = wx.MenuBar()

        file_menu = wx.Menu()
        quit_item = file_menu.Append(ID_QUIT, '&Quit')

        help_menu = wx.Menu()
        about_item = help_menu.Append(wx.NewId(), '&About')

        self.__menubar.Append(file_menu, '&File')
        self.__menubar.Append(help_menu, '&Help')

        self.SetMenuBar(self.__menubar)
        self.Bind(wx.EVT_MENU, self._on_quit, quit_item)
        self.Bind(wx.EVT_MENU, self._on_about, about_item)
        self.Bind(wx.EVT_SIZE, self._on_size)
        self.Bind(wx.EVT_CLOSE, self._on_quit)

    def _create_toolbar(self):
        self.__toolbar = wx.ToolBar(self, style=wx.HORIZONTAL)

        self.img_start = wx.Image(get_image_path("start.png"))
        self.img_start.Rescale(width=self.img_start.GetWidth() / 4,
                               height=self.img_start.GetHeight() / 4)
        self.img_stop = wx.Image(get_image_path("stop.png"))
        self.img_stop.Rescale(width=self.img_stop.GetWidth() / 4,
                              height=self.img_stop.GetHeight() / 4)
        btn_start = self.__toolbar.AddTool(ID_START,
                                           label='Start',
                                           bitmap=wx.Bitmap(self.img_start))
        self.__toolbar.EnableTool(ID_START, False)
        self.Bind(wx.EVT_TOOL, self.on_button_start, btn_start)

        self.img_next = wx.Image(get_image_path("next.png"))
        self.img_next.Rescale(width=self.img_next.GetWidth() / 4,
                              height=self.img_next.GetHeight() / 4)
        self.img_replay = wx.Image(get_image_path("replay.png"))
        self.img_replay.Rescale(width=self.img_replay.GetWidth() / 4,
                                height=self.img_replay.GetHeight() / 4)
        btn_next = self.__toolbar.AddTool(ID_NEXT,
                                          label='Next',
                                          bitmap=wx.Bitmap(self.img_next))
        self.__toolbar.EnableTool(ID_NEXT, False)
        self.Bind(wx.EVT_TOOL, self.on_button_next, btn_next)

        self.__toolbar.AddSeparator()

        image = wx.Image(get_image_path("enable.png"))
        image.Rescale(width=image.GetWidth() / 4, height=image.GetHeight() / 4)
        cb_enable = self.__toolbar.AddCheckTool(ID_ENABLE, 'Enable',
                                                wx.Bitmap(image))
        self.__toolbar.EnableTool(ID_ENABLE, True)
        self.Bind(wx.EVT_TOOL, self.on_button_enable, cb_enable)

        self.__toolbar.AddSeparator()

        image = wx.Image(get_image_path("save.png"))
        image.Rescale(width=image.GetWidth() / 4, height=image.GetHeight() / 4)
        cb_save = self.__toolbar.AddCheckTool(ID_SAVE, 'Save',
                                              wx.Bitmap(image))
        self.__toolbar.EnableTool(ID_SAVE, True)
        self.Bind(wx.EVT_TOOL, self.on_button_save, cb_save)

        self.__toolbar.AddSeparator()

        image = wx.Image(get_image_path("image.png"))
        image.Rescale(width=image.GetWidth() / 4, height=image.GetHeight() / 4)
        rb_image = self.__toolbar.AddRadioTool(ID_IMAGE, 'Image',
                                               wx.Bitmap(image))
        self.__toolbar.EnableTool(ID_IMAGE, True)
        self.Bind(wx.EVT_TOOL, self.on_button_image, rb_image)

        image = wx.Image(get_image_path("video.png"))
        image.Rescale(width=image.GetWidth() / 4, height=image.GetHeight() / 4)
        rb_video = self.__toolbar.AddRadioTool(ID_VIDEO, 'Video',
                                               wx.Bitmap(image))
        self.__toolbar.EnableTool(ID_VIDEO, True)
        self.Bind(wx.EVT_TOOL, self.on_button_video, rb_video)

        image = wx.Image(get_image_path("camera.png"))
        image.Rescale(width=image.GetWidth() / 4, height=image.GetHeight() / 4)
        rb_camera = self.__toolbar.AddRadioTool(ID_CAMERA, 'Camera',
                                                wx.Bitmap(image))
        self.__toolbar.EnableTool(ID_CAMERA, True)
        self.Bind(wx.EVT_TOOL, self.on_button_camera, rb_camera)

        self.__resource_id = ID_IMAGE

        self.__toolbar.AddSeparator()

        image = wx.Image(get_image_path("select.png"))
        image.Rescale(width=image.GetWidth() / 4, height=image.GetHeight() / 4)
        btn_select = self.__toolbar.AddTool(ID_SELECT,
                                            label='Select',
                                            bitmap=wx.Bitmap(image))
        self.__toolbar.EnableTool(ID_SELECT, True)
        self.Bind(wx.EVT_TOOL, self.on_button_select, btn_select)

        self.__toolbar.Realize()

        self.__mgr.AddPane(self.__toolbar, aui.AuiPaneInfo().
                           Name('Toolbar').Caption('Settings').
                           ToolbarPane().Top().Dockable(False))

    def _create_display_panel(self):
        self.__display_panel = DisplayPanel(self)
        self.__mgr.AddPane(self.__display_panel, aui.AuiPaneInfo().
                           Name('Display').Caption('Display').
                           CenterPane().Center().Dockable(False))

    def _on_size(self, event):
        if self.__display_panel:
            self.__display_panel.resize()
        event.Skip()

    def _on_quit(self, event):
        if self.__handler:
            self.__handler.CleanUp()
        self.Destroy()

    def _on_about(self, event):
        info = wx.adv.AboutDialogInfo()
        info.Name = "Image Display Tool"
        info.Description = "It is a display tool for image, video or camera"
        info.Developers = ["Meng Peng"]
        info.Copyright = "(c) 2020 mengepeng"
        wx.adv.AboutBox(info)

    def _reset_tool_state(self):
        self.__toolbar.EnableTool(ID_START, False)
        self.__toolbar.EnableTool(ID_NEXT, False)
        self.__toolbar.EnableTool(ID_ENABLE, True)
        self.__toolbar.ToggleTool(ID_ENABLE, False)
        self.__toolbar.EnableTool(ID_SAVE, True)
        self.__toolbar.ToggleTool(ID_SAVE, False)
        self.__toolbar.EnableTool(ID_SELECT, True)
        self.__toolbar.SetToolNormalBitmap(ID_START,
                                           wx.Bitmap(self.img_start))
        self.__toolbar.SetToolNormalBitmap(ID_NEXT,
                                           wx.Bitmap(self.img_next))

    def _set_tool_state(self):
        self._reset_tool_state()
        if self.__resource_id == ID_IMAGE:
            if self.__image_files:
                self.__toolbar.EnableTool(ID_START, True)
                if len(self.__image_files) > 1:
                    self.__toolbar.EnableTool(ID_NEXT, True)
                else:
                    self.__toolbar.EnableTool(ID_NEXT, False)
            else:
                self.__toolbar.EnableTool(ID_START, False)
                self.__toolbar.EnableTool(ID_NEXT, False)

        if self.__resource_id == ID_VIDEO:
            if self.__video_files:
                self.__toolbar.EnableTool(ID_START, True)
                if len(self.__video_files) > 1:
                    self.__toolbar.EnableTool(ID_NEXT, True)
                else:
                    self.__toolbar.EnableTool(ID_NEXT, False)
            else:
                self.__toolbar.EnableTool(ID_START, False)
                self.__toolbar.EnableTool(ID_NEXT, False)

        if self.__resource_id == ID_CAMERA:
            self.__toolbar.EnableTool(ID_START, True)
            self.__toolbar.EnableTool(ID_NEXT, False)
            self.__toolbar.EnableTool(ID_SELECT, False)

    def on_button_start(self, event):
        if self.__start:
            self.__start = False
            self.__toolbar.SetToolNormalBitmap(ID_START,
                                               wx.Bitmap(self.img_start))

            self.__handler.stop_display()
        else:
            self.__start = True
            self.__toolbar.SetToolNormalBitmap(ID_START,
                                               wx.Bitmap(self.img_stop))

            self.__handler.start_display()

    def on_button_next(self, event):
        self.__toolbar.SetToolNormalBitmap(ID_NEXT,
                                           wx.Bitmap(self.img_next))
        self.__handler.next_file()

    def on_button_enable(self, event):
        if event.GetInt():
            self.__handler.enable_processing(True)
        else:
            self.__handler.enable_processing(False)

    def on_button_save(self, event):
        if event.GetInt():
            self.__handler.save_file(True)
        else:
            self.__handler.save_file(False)
        pass

    def on_button_image(self, event):
        self.__resource_id = ID_IMAGE
        self._set_tool_state()
        self.__handler.set_image()
        self.__display_panel.clear()

    def on_button_video(self, event):
        self.__resource_id = ID_VIDEO
        self._set_tool_state()
        self.__handler.set_video()
        self.__display_panel.clear()

    def on_button_camera(self, event):
        self.__resource_id = ID_CAMERA
        self._set_tool_state()
        self.__handler.set_camera()
        self.__display_panel.clear()

    def on_button_select(self, event):
        path = get_resource_path()
        if self.__resource_id == ID_IMAGE:
            files = self._open_file(path, self.__image_wildcard)
            if files:
                self.__toolbar.EnableTool(ID_START, True)
                if len(files) > 1:
                    self.__toolbar.EnableTool(ID_NEXT, True)
                else:
                    self.__toolbar.EnableTool(ID_NEXT, False)
                self.__image_files = files
                self.__handler.load_files(files)
        if self.__resource_id == ID_VIDEO:
            files = self._open_file(path, self.__video_wildcard)
            if files:
                self.__toolbar.EnableTool(ID_START, True)
                if len(files) > 1:
                    self.__toolbar.EnableTool(ID_NEXT, True)
                else:
                    self.__toolbar.EnableTool(ID_NEXT, False)
                self.__video_files = files
                self.__handler.load_files(files)

    @staticmethod
    def _open_file(path, file_wildcard):
        dialog = wx.FileDialog(None, 'select',
                               path, '', file_wildcard,
                               wx.FD_OPEN | wx.FD_MULTIPLE)
        paths = None
        if dialog.ShowModal() == wx.ID_OK:
            paths = dialog.GetPaths()
        dialog.Destroy()
        return paths

    def OnNextDone(self, event):
        if event.GetData():
            self.__toolbar.SetToolNormalBitmap(ID_NEXT,
                                               wx.Bitmap(self.img_replay))
        else:
            self.__toolbar.SetToolNormalBitmap(ID_NEXT,
                                               wx.Bitmap(self.img_next))

    def OnDisplay(self, event):
        self.__display_panel.display(event.GetData())

    def OnStartState(self, event):
        self.__start = event.GetData()
        if self.__start:
            self.__toolbar.SetToolNormalBitmap(ID_START,
                                               wx.Bitmap(self.img_stop))
        else:
            self.__toolbar.SetToolNormalBitmap(ID_START,
                                               wx.Bitmap(self.img_start))


if __name__ == '__main__':
    app = wx.App()
    gui = DisplayGUI()
    gui.Show()
    app.SetTopWindow(gui)
    app.MainLoop()
