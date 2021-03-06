#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 1.0.0a7 on Thu Sep 10 18:12:59 2020
#

import configparser
import os
import subprocess
import sys
import time
import threading
import unicodedata
import wx
import wx.adv
import wx.lib.newevent

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from queue import Queue

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode
# end wxGlade

APP_VER = u"[v1.0.1]"
APP_NAME = u"棒読みちゃんバイパス" + u" " + APP_VER
APP_NAME_RUNNING = APP_NAME + u" (監視中)"
DLG_DIR_MESSAGE = u"フォルダを選択してください"
DLG_FIL_MESSAGE = u"RemoteTalk.exe ファイルを選択してください"
DLG_FIL_FILTER = u"exe files (*.exe)|*.exe"
DLG_CLS_MESSAGE = u"タスクトレイに常駐します"
FILE_EXT = ".ducktxt"
DUCK_FILE_ENCODING = "utf-8-sig"
FILE_ENCODING = "utf-8"
INI_FILE = "config.ini"
TRAY_TOOLTIP = u"棒読みちゃんバイパス"
TRAY_ICON = "resources/logo.ico"
# https://www.iconspedia.com/icon/sound-recorder-app-icon-43617.html

_queue = Queue()


class MyFrame(wx.Frame):
    """ Main Frame class """

    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame.__init__
        kwds["style"] = kwds.get("style", 0)\
                        | wx.RESIZE_BORDER\
                        | wx.MINIMIZE_BOX\
                        | wx.SYSTEM_MENU\
                        | wx.CAPTION\
                        | wx.CLOSE_BOX\
                        | wx.CLIP_CHILDREN
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((640, 150))
        self.SetMinSize((480, 150))
        self.SetMaxSize((2048, 150))
        self.SetTitle(APP_NAME)
        self.show_notice = True

        self.panel_1 = wx.Panel(self, wx.ID_ANY)

        sizer_1 = wx.BoxSizer(wx.VERTICAL)

        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1.Add(sizer_2, 1, wx.EXPAND, 0)

        label_1 = wx.StaticText(self.panel_1, wx.ID_ANY, u"監視フォルダ：")
        sizer_2.Add(label_1, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.text_ctrl_1 = wx.TextCtrl(self.panel_1, wx.ID_ANY, "")
        self.text_ctrl_1.Enable(False)
        sizer_2.Add(self.text_ctrl_1, 2, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.btn_chooser = wx.Button(self.panel_1, wx.ID_ANY, "...")
        sizer_2.Add(self.btn_chooser, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1.Add(sizer_3, 1, wx.EXPAND, 0)

        label_2 = wx.StaticText(self.panel_1, wx.ID_ANY, u"RemoteTalk：")
        sizer_3.Add(label_2, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.text_ctrl_2 = wx.TextCtrl(self.panel_1, wx.ID_ANY, "")
        self.text_ctrl_2.Enable(False)
        sizer_3.Add(self.text_ctrl_2, 2, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        self.btn_command = wx.Button(self.panel_1, wx.ID_ANY, "...")
        sizer_3.Add(self.btn_command, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1.Add(sizer_4, 1, wx.EXPAND, 0)

        self.btn_save = wx.Button(self.panel_1, wx.ID_ANY, u"設定を保存")
        sizer_4.Add(self.btn_save, 0, wx.ALL, 5)

        self.panel_2 = wx.Panel(self.panel_1, wx.ID_ANY)
        sizer_4.Add(self.panel_2, 1, wx.EXPAND, 0)

        self.btn_stop = wx.Button(self.panel_1, wx.ID_ANY, u"停止")
        self.btn_stop.Enable(False)
        sizer_4.Add(self.btn_stop, 0, wx.ALL, 5)

        self.btn_start = wx.Button(self.panel_1, wx.ID_ANY, u"転送開始")
        sizer_4.Add(self.btn_start, 0, wx.ALL, 5)

        self.panel_1.SetSizer(sizer_1)

        self.Layout()

        self.Bind(wx.EVT_BUTTON, self.on_choose_target_dir, self.btn_chooser)
        self.Bind(wx.EVT_BUTTON, self.on_choose_command_exe, self.btn_command)
        self.Bind(wx.EVT_BUTTON, self.on_save, self.btn_save)
        self.Bind(wx.EVT_BUTTON, self.on_stop, self.btn_stop)
        self.Bind(wx.EVT_BUTTON, self.on_exec, self.btn_start)
        self.Bind(wx.EVT_CLOSE, self.on_close)
        # end wxGlade

        self.tb_icon = wx.adv.TaskBarIcon()
        self.tb_icon.Bind(wx.adv.EVT_TASKBAR_LEFT_DCLICK, self.on_left_d_click)
        self.tb_icon.Bind(wx.adv.EVT_TASKBAR_RIGHT_UP, self.on_right_click)
        icon_path = resourcePath(TRAY_ICON)
        self.icon = wx.Icon(wx.Bitmap(icon_path))
        self.tb_icon.SetIcon(self.icon, TRAY_TOOLTIP)

        self.menu = wx.Menu()
        self.create_menu_item(self.menu, "Start", self.on_exec, menu_id=1)
        self.create_menu_item(self.menu, "Stop", self.on_stop, menu_id=2)
        self.menu.AppendSeparator()
        self.create_menu_item(self.menu, "Exit", self.on_exit)
        self.menu.Enable(id=1, enable=True)
        self.menu.Enable(id=2, enable=False)

        ini_full_path = os.path.join(os.getcwd(), INI_FILE)
        self.setting = ConfigSetting(ini_full_path)
        self.setting.loadConfig()
        if self.setting.active:
            self.text_ctrl_1.SetValue(self.setting.duck_dir)
            self.text_ctrl_2.SetValue(self.setting.remote_exe)

        self.watch_thread = None  # initialize by None

        self.signal_queue = True
        self.queue_thread = threading.Thread(target=self.queue_watcher)
        self.queue_thread.setDaemon(True)
        self.queue_thread.start()
        # end __init__

    def create_menu_item(self, menu, label, func, menu_id=-1):
        """ PopUpMenu item creator """

        item = wx.MenuItem(menu, menu_id, label)
        menu.Bind(wx.EVT_MENU, func, id=item.GetId())
        menu.Append(item)
        return item

    def directory_watcher(self, watch_path):
        """ File Observing controller """

        # print("directory_watcher START")
        event_handler = WatchDirectory(watch_path)
        observer = Observer()
        observer.schedule(event_handler, watch_path, recursive=True)
        observer.start()

        try:
            while self.signal_dir:
                time.sleep(1)
                # print("[dir_watch] "+threading.currentThread().name)

            observer.stop()

        except KeyboardInterrupt:
            observer.stop()
        except Exception as e:
            observer.stop()
            wx.MessageBox(u"エラーが発生しました。\nツールを再起動してください。", APP_NAME)
            self.signal_queue = False
            raise e
        finally:
            # print("directory_watcher END")
            observer.join()

    def queue_watcher(self):
        """ Queue watching controller """

        # print("queue_watcher START")
        try:
            while self.signal_queue:
                if _queue.empty():
                    time.sleep(1.3)
                    continue

                new_data_path: str = _queue.get(False)
                # print(new_data_path + u" をキューから取得しました")

                if new_data_path.lower().endswith(FILE_EXT):
                    pass
                else:
                    # print("拡張子が異なるため無視します")
                    continue

                if os.path.isfile(new_data_path):
                    with open(new_data_path, encoding=DUCK_FILE_ENCODING) as f:
                        lines = f.readlines()
                        # [0] User name
                        name = lines[0].replace('\n', '')
                        # [1] User Account (@abc)
                        account = lines[1].replace('\n', '')
                        # [2+] Tweet text (contain '\n' codes)
                        tweet_text = ''.join(map(str, lines[2:])).replace('\n', "　")
                        self.send_bouyomi_exe(name, account, tweet_text)
                else:
                    pass

                time.sleep(1.3)
                # print("[Queue] "+threading.currentThread().name)

        except Exception as e:
            # print("queue_watcher Exception")
            wx.MessageBox(u"エラーが発生しました。\nツールを再起動してください。", APP_NAME)
            self.signal_dir = False
            raise e

        # print("queue_watcher END")

    def send_bouyomi_exe(self, name: str, account: str, tweet: str):
        """ Send to BOUYOMI-CHAN for exe """

        # print("[" + name + "] (" + account + ") : " + tweet + "\n--------")
        self.bouyomi_exe.speak(tweet)
        return

    def on_choose_target_dir(self, event):  # wxGlade: MyFrame.<event_handler>
        """ Select Directory """

        path = self.text_ctrl_1.GetValue()
        watchPath = None
        if len(path) > 0:
            watchPath = self.show_dir_dialog(dpath=path)
        else:
            watchPath = self.show_dir_dialog()

        if watchPath is None:
            return
        self.text_ctrl_1.SetValue(watchPath)

    def on_choose_command_exe(self, event):  # wxGlade: MyFrame.<event_handler>
        """ Select exe """

        path = self.text_ctrl_2.GetValue()
        exePath = None
        if len(path) > 0:
            defDir, defFile = os.path.split(path)
            exePath = self.show_exe_dialog(ddir=defDir, dfile=defFile)
        else:
            exePath = self.show_exe_dialog()

        if exePath is None:
            return
        self.text_ctrl_2.SetValue(exePath)

    def on_save(self, event):  # wxGlade: MyFrame.<event_handler>
        """ Save """

        self.setting.duck_dir = self.text_ctrl_1.GetValue()
        self.setting.remote_exe = self.text_ctrl_2.GetValue()

        try:
            self.setting.saveConfig()

        except Exception as e:
            wx.MessageBox(u"INIファイルの書き込みに失敗しました\n管理者権限やファイルのロック状態を確認してください。", APP_NAME)
            raise e

        return

    def on_stop(self, event):  # wxGlade: MyFrame.<event_handler>
        """ Stop """

        self.signal_dir = False
        self.btn_stop.Disable()

        if (self.watch_thread is None):
            pass
        else:
            if (self.watch_thread.isAlive):
                self.watch_thread.join()

        self.SetTitle(APP_NAME)
        self.btn_chooser.Enable()
        self.btn_command.Enable()
        self.btn_start.Enable()
        self.menu.Enable(id=1, enable=True)
        self.menu.Enable(id=2, enable=False)

    def on_exec(self, event):  # wxGlade: MyFrame.<event_handler>
        """ Start """

        self.signal_dir = True
        self.btn_chooser.Disable()
        self.btn_command.Disable()
        self.btn_start.Disable()

        watchPath = self.text_ctrl_1.GetValue()
        exePath = self.text_ctrl_2.GetValue()
        if len(watchPath) == 0 | len(exePath) == 0:
            self.btn_chooser.Enable()
            self.btn_command.Enable()
            self.btn_start.Enable()
            return

        if self.watch_thread is None:
            pass
        else:
            if self.watch_thread.isAlive:
                self.watch_thread.join()

        self.bouyomi_exe = BouyomiExe(exePath)
        self.watch_thread = threading.Thread(target=self.directory_watcher, args=([watchPath]))
        self.watch_thread.setDaemon(True)
        self.watch_thread.start()

        self.SetTitle(APP_NAME_RUNNING)
        self.btn_stop.Enable()
        self.menu.Enable(id=1, enable=False)
        self.menu.Enable(id=2, enable=True)

    def on_close(self, event):
        """ Close [x] """

        self.Show(False)

        if self.show_notice == True:
            self.show_notice = False  # Once
        else:
            return

        wx.MessageBox(DLG_CLS_MESSAGE, APP_NAME)

    def show_dir_dialog(self, dpath=""):
        with wx.DirDialog(
                self, DLG_DIR_MESSAGE,
                style=wx.DD_DEFAULT_STYLE
                      | wx.DD_DIR_MUST_EXIST
                      | wx.DD_CHANGE_DIR,
                defaultPath=dpath) as dialog:
            if dialog.ShowModal() == wx.ID_CANCEL:
                return

            normalizePath = unicodedata.normalize("NFC", dialog.GetPath())
            return normalizePath

    def show_exe_dialog(self, ddir="", dfile=""):
        with wx.FileDialog(
                self, DLG_FIL_MESSAGE,
                wildcard=DLG_FIL_FILTER,
                style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST,
                defaultDir=ddir,
                defaultFile=dfile) as dialog:
            if dialog.ShowModal() == wx.ID_CANCEL:
                return

            normalizePath = unicodedata.normalize("NFC", dialog.GetPath())
            return normalizePath

    def on_left_d_click(self, event):
        """ [TaskBarIcon] Left double click """

        if self.IsShown():
            self.Show(False)
        else:
            self.Show()
            self.Raise()

    def on_right_click(self, event):
        """ [TaskBarIcon] Right click """

        self.tb_icon.PopupMenu(self.menu)

    def on_exit(self, event):
        """ [PopupMenu] Exit """

        self.signal_dir = False
        if self.watch_thread is None:
            pass
        else:
            if self.watch_thread.isAlive:
                self.watch_thread.join()

        self.signal_queue = False
        if self.queue_thread is None:
            pass
        else:
            if self.queue_thread.isAlive:
                self.queue_thread.join()

        self.tb_icon.RemoveIcon()
        wx.Exit()

# end of class MyFrame


class ConfigSetting:
    SECTION = "PATH"
    KEY_DUCK = "duck_dir"
    KEY_TALK = "remote_exe"

    def __init__(self, filename):
        self.config_file = filename
        self.active = False
        self.duck_dir = ""
        self.remote_exe = ""

    def loadConfig(self):

        if not os.path.exists(self.config_file):
            # print("[Error] Not found config file.")
            return
        else:
            self.active = True

        config = configparser.SafeConfigParser()
        config.read(self.config_file)

        if not self.SECTION in config.sections():
            self.active = False
            return

        read_default = config[self.SECTION]
        self.duck_dir = read_default[self.KEY_DUCK].replace("\\\\", "\\")
        self.remote_exe = read_default[self.KEY_TALK].replace("\\\\", "\\")

    def saveConfig(self):
        config = configparser.SafeConfigParser()
        if os.path.exists(self.config_file):
            config.read(self.config_file)

        if not self.SECTION in config.sections():
            config.add_section(self.SECTION)

        if len(self.duck_dir) == 0:
            self.duck_dir = ""
        else:
            self.duck_dir = self.duck_dir.replace("\\", "\\\\")
            pass

        # print("duck = " + self.duck_dir)
        config.set(self.SECTION, self.KEY_DUCK, self.duck_dir)

        if len(self.remote_exe) == 0:
            self.remote_exe = ""
        else:
            self.remote_exe = self.remote_exe.replace("\\", "\\\\")
            pass

        # print("talk = " + self.remote_exe)
        config.set(self.SECTION, self.KEY_TALK, self.remote_exe)

        with open(self.config_file, "w") as file_obj:
            config.write(file_obj)

# end of class ConfigSetting


class WatchDirectory(FileSystemEventHandler):
    # サブディレクトリ内のファイル追加も検知するため今後の改造内容によっては注意

    def __init__(self, watch_path):
        super(WatchDirectory, self).__init__()
        self.watch_path = watch_path

    def on_created(self, event):
        file_path = event.src_path
        # file_name = os.path.basename(file_path)
        # print(u"%s が追加されました" % file_name)
        _queue.put(file_path)  # add queue

    def on_moved(self, event):
        pass

    def on_modified(self, event):
        pass

    def on_deleted(self, event):
        pass

# end of class WatchDirectory


class BouyomiExe:
    def __init__(self, exePath):
        self.exePath = exePath

    def speak(self, message):
        try:
            subprocess.run([repr(self.exePath)[1:-1], "/Talk", message], **subprocess_args(True))
        except (subprocess.CalledProcessError, IndexError, OSError):
            pass

# end of class BouyomiExe


class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True

# end of class MyApp


def resourcePath(filename):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(os.path.abspath("."), filename)


def subprocess_args(include_stdout=True):
    if hasattr(subprocess, "STARTUPINFO"):
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        env = os.environ
    else:
        si = None
        env = None

    if include_stdout:
        ret = {"stdout": subprocess.PIPE}
    else:
        ret = {}

    ret.update({"stdin": subprocess.PIPE,
                "stderr": subprocess.PIPE,
                "startupinfo": si,
                "env": env})
    return ret


if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()
