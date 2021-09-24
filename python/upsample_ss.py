#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2021 Jacob Miller.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy as np
from gnuradio import gr

class upsample_ss(gr.sync_block):
    """
    docstring for block upsample_ss
    """
    def __init__(self, N=1):
        gr.sync_block.__init__(self,
            name="upsample_ss",
            in_sig=[np.int16],
            out_sig=[np.int16])
        self.set_output_multiple(N)
        self._N = N

    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
        # <+signal processing here+>
        out[:] = 0
        out[::self._N] = in0
        return len(output_items[0])

