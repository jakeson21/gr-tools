#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2021 Jacob Miller.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy as np
from gnuradio import gr

class apsk_modulator_bc(gr.sync_block):
    """
    docstring for block apsk_modulator_bc
    """
    def __init__(self, constellation):
        gr.sync_block.__init__(self,
            name="apsk_modulator_bc",
            in_sig=[np.byte],
            out_sig=[np.csingle])
        self._constellation = constellation
        self.set_output_multiple(len(constellation))

    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
        # <+signal processing here+>
        out[:] = self._constellation[in0]
        return len(output_items[0])

