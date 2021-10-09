#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: FM TX From Audio File
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
from gnuradio import analog
from gnuradio import blocks
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
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
import numpy as np
import tools



from gnuradio import qtgui

class stereo_audio_file_fm_tx(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "FM TX From Audio File", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("FM TX From Audio File")
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

        self.settings = Qt.QSettings("GNU Radio", "stereo_audio_file_fm_tx")

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
        self.variable_gain = variable_gain = 45
        self.stereo_gain = stereo_gain = 0.9
        self.samp_rate = samp_rate = 44100
        self.pilot_gain = pilot_gain = 0.1
        self.out_gain = out_gain = 0.95
        self.mono_gain = mono_gain = 0.9
        self.fm_deviation = fm_deviation = 50000
        self.center_freq = center_freq = 108.5e6

        ##################################################
        # Blocks
        ##################################################
        self._variable_gain_range = Range(0, 70, 1, 45, 200)
        self._variable_gain_win = RangeWidget(self._variable_gain_range, self.set_variable_gain, 'RF Gain', "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._variable_gain_win)
        self._stereo_gain_range = Range(0, 2, 0.01, 0.9, 200)
        self._stereo_gain_win = RangeWidget(self._stereo_gain_range, self.set_stereo_gain, 'L-R', "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._stereo_gain_win, 2, 0, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._pilot_gain_range = Range(0, 1, 0.01, 0.1, 200)
        self._pilot_gain_win = RangeWidget(self._pilot_gain_range, self.set_pilot_gain, 'Pilot', "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._pilot_gain_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._out_gain_range = Range(0, 2, 0.01, 0.95, 200)
        self._out_gain_win = RangeWidget(self._out_gain_range, self.set_out_gain, 'Out', "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._out_gain_win, 3, 0, 1, 1)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._mono_gain_range = Range(0, 2, 0.01, 0.9, 200)
        self._mono_gain_win = RangeWidget(self._mono_gain_range, self.set_mono_gain, 'L+R', "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._mono_gain_win, 1, 0, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._fm_deviation_range = Range(2500, 100000, 500, 50000, 200)
        self._fm_deviation_win = RangeWidget(self._fm_deviation_range, self.set_fm_deviation, 'fm_deviation', "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._fm_deviation_win, 4, 0, 1, 1)
        for r in range(4, 5):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._center_freq_range = Range(80e6, 200e6, 100000, 108.5e6, 200)
        self._center_freq_win = RangeWidget(self._center_freq_range, self.set_center_freq, 'Center Frequency', "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._center_freq_win)
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
            ",".join(("serial=3102419", '')),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
            "",
        )
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate*4*2)
        self.uhd_usrp_sink_0.set_time_unknown_pps(uhd.time_spec(0))

        self.uhd_usrp_sink_0.set_center_freq(uhd.tune_request(center_freq, 0), 0)
        self.uhd_usrp_sink_0.set_antenna("TX/RX", 0)
        self.uhd_usrp_sink_0.set_bandwidth(500000, 0)
        self.uhd_usrp_sink_0.set_gain(variable_gain, 0)
        self.tools_audio_file_source_0 = tools.audio_file_source('/home/fuguru/Music/Queensryche - 11 - Anybody Listening-.mp3', samp_rate, 2, True, True)
        self.rational_resampler_xxx_0_1_0_0_0 = filter.rational_resampler_fff(
                interpolation=2,
                decimation=1,
                taps=[],
                fractional_bw=0)
        self.rational_resampler_xxx_0_1_0_0 = filter.rational_resampler_fff(
                interpolation=4,
                decimation=1,
                taps=[],
                fractional_bw=0)
        self.rational_resampler_xxx_0_1_0 = filter.rational_resampler_fff(
                interpolation=4,
                decimation=1,
                taps=[],
                fractional_bw=0)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_c(
            1024, #size
            samp_rate*4*2, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1.2, 1.2)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

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
        self.low_pass_filter_0_1_0 = filter.fir_filter_fff(
            1,
            firdes.low_pass(
                stereo_gain,
                samp_rate,
                15000,
                2000,
                window.WIN_HAMMING,
                6.76))
        self.low_pass_filter_0_1 = filter.fir_filter_fff(
            1,
            firdes.low_pass(
                mono_gain,
                samp_rate,
                15000,
                2000,
                window.WIN_HAMMING,
                6.76))
        self.low_pass_filter_0_0 = filter.fir_filter_ccf(
            1,
            firdes.low_pass(
                out_gain,
                samp_rate*4*2,
                95000,
                10000,
                window.WIN_HAMMING,
                6.76))
        self.blocks_sub_xx_0_0 = blocks.sub_ff(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vff(1)
        self.blocks_add_xx_0_0_0 = blocks.add_vff(1)
        self.blocks_add_xx_0_0 = blocks.add_vff(1)
        self.analog_sig_source_x_0_0 = analog.sig_source_f(samp_rate*4, analog.GR_SIN_WAVE, 19000., pilot_gain, 0, 0)
        self.analog_sig_source_x_0 = analog.sig_source_f(samp_rate*4, analog.GR_SIN_WAVE, 2*19000., 2.0, 0, 0)
        self.analog_frequency_modulator_fc_0 = analog.frequency_modulator_fc(2*np.pi*fm_deviation/(samp_rate*4*2))
        self.analog_fm_preemph_0_0_0_0 = analog.fm_preemph(fs=samp_rate, tau=50e-6, fh=-1.0)
        self.analog_fm_preemph_0_0_0 = analog.fm_preemph(fs=samp_rate, tau=50e-6, fh=-1.0)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_fm_preemph_0_0_0, 0), (self.blocks_add_xx_0_0, 0))
        self.connect((self.analog_fm_preemph_0_0_0, 0), (self.blocks_sub_xx_0_0, 0))
        self.connect((self.analog_fm_preemph_0_0_0_0, 0), (self.blocks_add_xx_0_0, 1))
        self.connect((self.analog_fm_preemph_0_0_0_0, 0), (self.blocks_sub_xx_0_0, 1))
        self.connect((self.analog_frequency_modulator_fc_0, 0), (self.low_pass_filter_0_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_add_xx_0_0_0, 2))
        self.connect((self.blocks_add_xx_0_0, 0), (self.rational_resampler_xxx_0_1_0, 0))
        self.connect((self.blocks_add_xx_0_0_0, 0), (self.rational_resampler_xxx_0_1_0_0_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_add_xx_0_0_0, 1))
        self.connect((self.blocks_sub_xx_0_0, 0), (self.rational_resampler_xxx_0_1_0_0, 0))
        self.connect((self.low_pass_filter_0_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.low_pass_filter_0_0, 0), (self.uhd_usrp_sink_0, 0))
        self.connect((self.low_pass_filter_0_1, 0), (self.analog_fm_preemph_0_0_0, 0))
        self.connect((self.low_pass_filter_0_1_0, 0), (self.analog_fm_preemph_0_0_0_0, 0))
        self.connect((self.rational_resampler_xxx_0_1_0, 0), (self.blocks_add_xx_0_0_0, 0))
        self.connect((self.rational_resampler_xxx_0_1_0_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.rational_resampler_xxx_0_1_0_0_0, 0), (self.analog_frequency_modulator_fc_0, 0))
        self.connect((self.tools_audio_file_source_0, 0), (self.low_pass_filter_0_1, 0))
        self.connect((self.tools_audio_file_source_0, 1), (self.low_pass_filter_0_1_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "stereo_audio_file_fm_tx")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_variable_gain(self):
        return self.variable_gain

    def set_variable_gain(self, variable_gain):
        self.variable_gain = variable_gain
        self.uhd_usrp_sink_0.set_gain(self.variable_gain, 0)

    def get_stereo_gain(self):
        return self.stereo_gain

    def set_stereo_gain(self, stereo_gain):
        self.stereo_gain = stereo_gain
        self.low_pass_filter_0_1_0.set_taps(firdes.low_pass(self.stereo_gain, self.samp_rate, 15000, 2000, window.WIN_HAMMING, 6.76))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_frequency_modulator_fc_0.set_sensitivity(2*np.pi*self.fm_deviation/(self.samp_rate*4*2))
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate*4)
        self.analog_sig_source_x_0_0.set_sampling_freq(self.samp_rate*4)
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(self.out_gain, self.samp_rate*4*2, 95000, 10000, window.WIN_HAMMING, 6.76))
        self.low_pass_filter_0_1.set_taps(firdes.low_pass(self.mono_gain, self.samp_rate, 15000, 2000, window.WIN_HAMMING, 6.76))
        self.low_pass_filter_0_1_0.set_taps(firdes.low_pass(self.stereo_gain, self.samp_rate, 15000, 2000, window.WIN_HAMMING, 6.76))
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate*4*2)
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate*4*2)

    def get_pilot_gain(self):
        return self.pilot_gain

    def set_pilot_gain(self, pilot_gain):
        self.pilot_gain = pilot_gain
        self.analog_sig_source_x_0_0.set_amplitude(self.pilot_gain)

    def get_out_gain(self):
        return self.out_gain

    def set_out_gain(self, out_gain):
        self.out_gain = out_gain
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(self.out_gain, self.samp_rate*4*2, 95000, 10000, window.WIN_HAMMING, 6.76))

    def get_mono_gain(self):
        return self.mono_gain

    def set_mono_gain(self, mono_gain):
        self.mono_gain = mono_gain
        self.low_pass_filter_0_1.set_taps(firdes.low_pass(self.mono_gain, self.samp_rate, 15000, 2000, window.WIN_HAMMING, 6.76))

    def get_fm_deviation(self):
        return self.fm_deviation

    def set_fm_deviation(self, fm_deviation):
        self.fm_deviation = fm_deviation
        self.analog_frequency_modulator_fc_0.set_sensitivity(2*np.pi*self.fm_deviation/(self.samp_rate*4*2))

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.uhd_usrp_sink_0.set_center_freq(uhd.tune_request(self.center_freq, 0), 0)




def main(top_block_cls=stereo_audio_file_fm_tx, options=None):

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
