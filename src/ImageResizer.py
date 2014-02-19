#####################################################
# File:         ImageResizer.py
# Rev:          1.0
# Author:       Jacob Calvert
# Dependencies: PIL, threading, os, GUI
# Contains:     ImageObject, ImageQueue, ImageProcessor
#####################################################
import Image
import threading
import os
import GUI


class ImageObject:

    def __init__(self, file_name, scale_to, save_to):
        self.__fn = file_name
        self.__scale = scale_to
        self.__save_to = save_to
        self.__status = "Queued."
        i = self.__fn.rindex("/")
        self.__nm = self.__fn[i:]

    def resize(self):
        self.__status = "Resizing."
        orig = Image.open(self.__fn)
        w = orig.size[0]*self.__scale
        h = orig.size[1]*self.__scale
        new_img = orig.resize((int(w), int(h)), Image.ANTIALIAS)
        new_img.save(self.__save_to)
        self.__status = "Resized."
        
    def status(self):
        return self.__status

    def name(self):
        return self.__nm

    def scale(self, scale):
        self.__scale = scale


class ImageQueue():
    EXTENSIONS = [".jpg", ".png", ".gif", ".bmp", ".tiff"]

    def __init__(self, source_dir, dest_dir, scale=0.5, _gui=None):
        self.__src = source_dir
        self.__dest = dest_dir
        self.__stack = []
        self.__scale = scale
        self.__gui = _gui
        self.log("ImageQueue loading...")
        if not os.path.exists(source_dir):
            self.__gui.log("ERROR: Source directory does not exist!")
        if not os.path.exists(dest_dir):
            self.__gui.log("Warning: Destination directory does not exist.")
            os.makedirs(dest_dir)
            self.__gui.log("Info: created directory (" + dest_dir + ")")

    def pop(self):
        item = self.__stack[-1]
        self.__stack.remove(item)
        return item

    def scan(self):
        files = os.listdir(self.__src)
        self.log("Scanning '"+self.__src+"'.")
        for fn in files:
            for extension in self.EXTENSIONS:
                if not fn.lower().endswith(extension):
                    files.remove(fn)
                    break
                else:
                    f0 = self.__src + "/" + fn
                    f1 = self.__dest + "/" + fn
                    img = ImageObject(f0, self.__scale, f1)
                    self.__stack.append(img)
                    self.log("File: %-20s %s %-15s" % (fn, "Status: ", img.status()))
        l = len(self.__stack)
        self.log("Found %d valid files." % (l))
        self.log("Files ready for resizing. Click start to begin.")

    def set_scale(self, scale):
        self.__scale = scale
        for img in self.__stack:
            img.scale(scale)

    def is_empty(self):
        return len(self.__stack) == 0

    def log(self, event):
        if self.__gui is not None:
            self.__gui.log(event)


class ImageProcessor(threading.Thread):
    threadLock = threading.Lock()

    def __init__(self, image_queue, _gui=None):
        threading.Thread.__init__(self)
        self.__stack = image_queue
        self.__gui = _gui

    def run(self):
        while not self.__stack.is_empty():
            self.threadLock.acquire()
            item = self.__stack.pop()
            self.threadLock.release()
            self.log("Resizing " + item.name())
            item.resize()
        self.log("ImageProcessor finished.")
        processors.remove(self)
        if len(processors) == 0:
            self.log("Processing finished.")

    def log(self, event):
        if self.__gui is not None:
            self.threadLock.acquire()
            self.__gui.log(event)
            self.threadLock.release()


queue = None
processors = []

config = {"threads": 4}

if __name__ == "__main__":
    gui = GUI.MainGUI()
    gui.mainloop()


def do_scan_check(gui_ref):
    global queue, processors
    if gui_ref.get_source() is not None and gui_ref.get_dest() is not None:
        scale = gui_ref.get_scale()
        if scale == 0.0:
            scale = 0.01
        queue = ImageQueue(gui_ref.get_source(), gui_ref.get_dest(), scale, gui_ref)
        l = config["threads"]
        gui_ref.log("Adding " + str(l) + " ImageProcessors...")
        for i in range(l):
            processors.append(ImageProcessor(queue, gui_ref))
        queue.scan()



