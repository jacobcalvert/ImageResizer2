#####################################################
# File:         GUI.py
# Rev:          1.0
# Author:       Jacob Calvert
# Dependencies: Tkinter, time, datetime, ImageResizer
# Contains:     logging, gui
#####################################################
import Tkinter
import tkFileDialog
import time
import datetime
import ImageResizer


class MainGUI(Tkinter.Tk):

    def __init__(self):
        Tkinter.Tk.__init__(self)
        self.__frame = Tkinter.Frame(self)
        self.__frame.pack()
        self.__dest_dir_label = None
        self.__src_dir_label = None
        self.__src_dir = None
        self.__dest_dir = None
        self.__text_out = None
        self.__start_btn = None
        self.__scale = None
        self.__scale_var = None
        self.__init_time = None
        self._set_up_frame()

    def _set_up_frame(self):
        self.wm_title("ImageResizer2")
        self.__start_btn = Tkinter.Button(self.__frame, text="Start", command=self._call_run)
        choose_source = Tkinter.Button(self.__frame, text="Choose Source", command=self._create_choose_source)
        choose_dest = Tkinter.Button(self.__frame, text="Choose Destination", command=self._create_choose_dest)
        src = "Source: " + str(self.__src_dir)
        dest = "Destination: " + str(self.__dest_dir)
        self.__dest_dir_label = Tkinter.Label(self.__frame, text=dest)
        self.__src_dir_label = Tkinter.Label(self.__frame, text=src)
        self.__text_out = Tkinter.Text(self.__frame)
        self.__scale_var = Tkinter.DoubleVar()
        self.__scale = Tkinter.Scale(self.__frame, variable=self.__scale_var, orient=Tkinter.HORIZONTAL, from_=10, to=200)
        self.__src_dir_label.pack(side=Tkinter.BOTTOM)
        self.__dest_dir_label.pack(side=Tkinter.BOTTOM)
        choose_source.pack(side=Tkinter.TOP)
        choose_dest.pack(side=Tkinter.TOP)
        self.__scale.pack(side=Tkinter.TOP)

        self.__start_btn.pack(side=Tkinter.BOTTOM)
        self.__text_out.pack(side=Tkinter.BOTTOM)
        self.log("ImageResizer2 version " + str(ImageResizer.config["version"]) + ".")
        self.log("Get the latest source from the git repo at " + ImageResizer.config["github_git_link"])
        self.log("Author: %s Web Site: %s" % (ImageResizer.config["author"], ImageResizer.config["website"]))

    def _create_choose_source(self):
        self.__src_dir = tkFileDialog.askdirectory()
        self.log("Source selected ("+self.__src_dir+")")
        self.__src_dir_label.config(text="Source: " + self.__src_dir)
        self.__start_btn.config(state="normal")
        ImageResizer.do_scan_check(self)

    def _create_choose_dest(self):
        self.__dest_dir = tkFileDialog.askdirectory()
        self.log("Destination selected (" + self.__dest_dir + ")")
        self.__dest_dir_label.config(text="Destination: " + self.__dest_dir)
        self.__start_btn.config(state="normal")
        ImageResizer.do_scan_check(self)

    def _call_run(self):
        ImageResizer.queue.set_scale(self.get_scale())
        self.__init_time = time.time()
        for processor in ImageResizer.processors:
            processor.start()
            self.__start_btn.config(state="disabled")

    def start_time(self):
        return self.__init_time

    def ftime(self, t):
        t = int(t)
        m, s = 0, 0
        if t > 59:
            m = t % 60
            s = t - m*60
        else:
            s = t
        return "%dm%ds" % (m, s)

    def log(self, event):
        self.__text_out.insert(Tkinter.END, self._timestamp() + " - " + event+"\n")

    def _timestamp(self):
        return datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S')

    def get_source(self):
        return self.__src_dir

    def get_dest(self):
        return self.__dest_dir

    def get_scale(self):
        return self.__scale_var.get()/100.00