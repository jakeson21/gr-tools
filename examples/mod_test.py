#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Modulator Testing
# Author: fuguru
# GNU Radio version: 3.9.2.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import blocks
from gnuradio import digital
from gnuradio import filter
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import uhd
import time
import numpy as np
import scipy.signal
import tools



from gnuradio import qtgui

class mod_test(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Modulator Testing", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Modulator Testing")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "mod_test")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 48000
        self.symb_rate = symb_rate = samp_rate/10
        self.sps = sps = int(samp_rate/symb_rate)
        self.variable_qtgui_dial_control_0 = variable_qtgui_dial_control_0 = samp_rate/2
        self.variable_constellation_0 = variable_constellation_0 = digital.constellation_calcdist([-1+0j, -1/3+0j, 1/3+0j, 1+0j], [0, 1, 2, 3],
        2, 1, digital.constellation.NO_NORMALIZATION).base()
        self.rrc_filter_taps = rrc_filter_taps = firdes.root_raised_cosine(sps*2/np.pi, sps,1, 0.35, 20*sps+1)
        self.rf_gain = rf_gain = 25
        self.fd = fd = 12000

        ##################################################
        # Blocks
        ##################################################
        if "real" == "int":
        	isFloat = False
        	scaleFactor = 1
        else:
        	isFloat = True
        	scaleFactor = 1

        _variable_qtgui_dial_control_0_dial_control = qtgui.GrDialControl('FM Deviation', self, 1000,samp_rate/2,samp_rate/2,"default",self.set_variable_qtgui_dial_control_0,isFloat, scaleFactor, 50, True, "'value'")
        self.variable_qtgui_dial_control_0 = _variable_qtgui_dial_control_0_dial_control

        self.top_layout.addWidget(_variable_qtgui_dial_control_0_dial_control)
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
            ",".join(("serial=3102419", '')),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
            "",
        )
        self.uhd_usrp_sink_0.set_samp_rate(240000)
        self.uhd_usrp_sink_0.set_time_unknown_pps(uhd.time_spec(0))

        self.uhd_usrp_sink_0.set_center_freq(900.5e6, 0)
        self.uhd_usrp_sink_0.set_antenna("TX/RX", 0)
        self.uhd_usrp_sink_0.set_gain(rf_gain, 0)
        self.tools_fm_modulator_fc_0 = tools.fm_modulator_fc(samp_rate, variable_qtgui_dial_control_0, 0)
        self.tools_audio_file_source_0 = tools.audio_file_source('/home/fuguru/Music/311-beautiful_disaster.mp3', 41000, 2, True)
        self.rational_resampler_xxx_0_0 = filter.rational_resampler_ccc(
                interpolation=5,
                decimation=1,
                taps=[],
                fractional_bw=0.4)
        self.rational_resampler_xxx_0 = filter.rational_resampler_fff(
                interpolation=160,
                decimation=147,
                taps=[],
                fractional_bw=0.4)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_c(
            1024, #size
            symb_rate*sps/4, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-2, 2)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', 'FSK')

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(True)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(0.5)
        self.blocks_add_xx_0 = blocks.add_vff(1)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.tools_fm_modulator_fc_0, 0))
        self.connect((self.rational_resampler_xxx_0_0, 0), (self.uhd_usrp_sink_0, 0))
        self.connect((self.tools_audio_file_source_0, 1), (self.blocks_add_xx_0, 1))
        self.connect((self.tools_audio_file_source_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.tools_fm_modulator_fc_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.tools_fm_modulator_fc_0, 0), (self.rational_resampler_xxx_0_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "mod_test")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_sps(int(self.samp_rate/self.symb_rate))
        self.set_symb_rate(self.samp_rate/10)

    def get_symb_rate(self):
        return self.symb_rate

    def set_symb_rate(self, symb_rate):
        self.symb_rate = symb_rate
        self.set_sps(int(self.samp_rate/self.symb_rate))
        self.qtgui_time_sink_x_0.set_samp_rate(self.symb_rate*self.sps/4)

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.set_rrc_filter_taps(firdes.root_raised_cosine(self.sps*2/np.pi, self.sps, 1, 0.35, 20*self.sps+1))
        self.qtgui_time_sink_x_0.set_samp_rate(self.symb_rate*self.sps/4)

    def get_variable_qtgui_dial_control_0(self):
        return self.variable_qtgui_dial_control_0

    def set_variable_qtgui_dial_control_0(self, variable_qtgui_dial_control_0):
        self.variable_qtgui_dial_control_0 = variable_qtgui_dial_control_0
        self.tools_fm_modulator_fc_0.set_freq_deviation(self.variable_qtgui_dial_control_0)

    def get_variable_constellation_0(self):
        return self.variable_constellation_0

    def set_variable_constellation_0(self, variable_constellation_0):
        self.variable_constellation_0 = variable_constellation_0

    def get_rrc_filter_taps(self):
        return self.rrc_filter_taps

    def set_rrc_filter_taps(self, rrc_filter_taps):
        self.rrc_filter_taps = rrc_filter_taps

    def get_rf_gain(self):
        return self.rf_gain

    def set_rf_gain(self, rf_gain):
        self.rf_gain = rf_gain
        self.uhd_usrp_sink_0.set_gain(self.rf_gain, 0)

    def get_fd(self):
        return self.fd

    def set_fd(self, fd):
        self.fd = fd




def main(top_block_cls=mod_test, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
