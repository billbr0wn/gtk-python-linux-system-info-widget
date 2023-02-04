#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, Gdk
import cairo
import psutil
import os

class _MyWidget_(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self)

##        self.win = Gtk.Window()
##        self.win.set_opacity(0.5) # set the opacity to 50%

        #attributes for window:
        self.set_decorated(False)
        self.set_opacity(0.6)
        self.set_app_paintable(True)
##        self.connect("draw", self.area_draw__)
        
        #location of window
        self.move(400, 400)
##        _MyWidget_.put(self, 120, 95)
        
        #create vbox
        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=1)
        self.add(self.vbox)

        #create labels
        self.kernel_label = Gtk.Label()
        self.cpu_label = Gtk.Label()
        self.memory_label = Gtk.Label()
        self.temperature_label = Gtk.Label()
        self.disc_usage_label = Gtk.Label()
        self.cpu_count_label = Gtk.Label()
        self.cpu_frequency_label = Gtk.Label()
        self.system_boot_label = Gtk.Label()
        #---------------
        #make labels available to vbox\
        self.vbox.add(self.kernel_label)
        self.vbox.add(self.cpu_label)
        self.vbox.add(self.memory_label)
        self.vbox.add(self.temperature_label)
        self.vbox.add(self.disc_usage_label)
        self.vbox.add(self.cpu_count_label)
        self.vbox.add(self.cpu_frequency_label)
        self.vbox.add(self.system_boot_label)

        #pack labels into the vbox layout
        self.vbox.pack_start(self.kernel_label, True, True, 0)
        self.vbox.pack_start(self.cpu_label, True, True, 0)
        self.vbox.pack_start(self.memory_label, True, True, 0)
        self.vbox.pack_start(self.temperature_label, True, True, 0)
        self.vbox.pack_start(self.disc_usage_label, True, True, 0)
        self.vbox.pack_start(_TransparentLabel_, True, True, 0)
        self.vbox.pack_start(self.cpu_count_label, True, True, 0)
        self.vbox.pack_start(self.cpu_frequency_label, True, True, 0)
        self.vbox.pack_start(self.system_boot_label, True, True, 0)
        
        #show the labels
        self.cpu_label.show()
        self.memory_label.show()
        self.temperature_label.show()
        self.kernel_label.show()
        self.disc_usage_label.show()
        self.cpu_count_label.show()
        self.cpu_frequency_label.show()
        self.system_boot_label.show()
        
        self.update_labels__()
        
    def update_labels__(self):
    
        # get CPU usage
        cpu_percent = psutil.cpu_percent()
        self.cpu_label.set_text("CPU: " + str(cpu_percent) + "%")

        # get memory usage
        memory_info = psutil.virtual_memory()
        memory_percent = memory_info.percent
        self.memory_label.set_text("Memory: " + str(memory_percent) + "%")

        #get temp info
        self.temps_text = psutil.sensors_temperatures()
        #set temp label
        self.temp_current_value = str(self.temps_text['k10temp'])
        self.parsed_temperature_value = self.temp_current_value.split("current=")[1].split(",")[0]
        self.temperature_label.set_text("temps: " + str(self.parsed_temperature_value) + " °C")   

        #set kernel label
        self.kernel_text = str(os.uname().release)
        self.kernel_label.set_text("""   Kernel : %s
---------------------------------------""" % self.kernel_text)

        disc_usage = psutil.disk_usage("/")
        self.disc_usage = disc_usage
        self.disc_usage_text = f"""
disc usage-->
Total: {self.disc_usage.total/1024**3:.2f} GB\nUsed: {self.disc_usage.used/1024**3:.2f} GB\nFree: {self.disc_usage.free/1024**3:.2f} GB"""
        self.disc_usage_label.set_text(self.disc_usage_text)
        

        #NUMBER OF CORES/THREADS ON CPU
        self.cpu_count_info = psutil.cpu_count()
        self.cpu_count_text = "core/thread count: " + str(self.cpu_count_info)
        print()
        self.cpu_count_label.set_text("""
core/thread count: """ + str(self.cpu_count_info))


        #display the CPU frequency:
        self.cpu_frequency_info = psutil.cpu_freq()
        self.cpu_freq_text = """CPU frequency: """ + str(self.cpu_frequency_info)
        self.parsed_frequency_value = self.cpu_freq_text.split("current=")[1].split(".")[0]
        self.cpu_frequency_label.set_text("""CPU frequency: """ + str(self.parsed_frequency_value))
        
        #display boot time
        self.system_boot_info = psutil.boot_time()
        self.system_boot_adjust = self.system_boot_info / 100000000
        self.system_boot_text = """
Boot Time: """ + str(self.system_boot_adjust)
        self.system_boot_label.set_text(self.system_boot_text)


        self.timer__()
        

    def timer__(self):
        # update labels every second
        GLib.timeout_add(1250, self.update_labels__)
        

        
#############extra label class 
class _TransparentLabel_(Gtk.Overlay):
    def __init__(self, text):
        Gtk.Overlay.__init__(self)
        self.label = Gtk.Label(text)
        self.add(self.label)
        self.set_overlay_pass_through(self.label, True)
        self.set_opacity(1.0)
##        self.label.set_text("_TransparentLabel_class")

_TransparentLabel_ = _TransparentLabel_("")
_TransparentLabel_.show()



win = _MyWidget_()
win.set_default_size(100, 500)## set window size
win.move(400, 400)
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
