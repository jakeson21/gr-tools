#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2021 Jacob Miller.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy as np
from gnuradio import gr
import pmt
import pdb

class print_float(gr.sync_block):
    """
    docstring for block print_float
    """
    def __init__(self, variable_name='', enabled=True):
        gr.sync_block.__init__(self,
            name="print_float",
            in_sig=[],
            out_sig=[])
        self.variable_name = variable_name
        self.enabled = enabled
        self.message_port_register_in(pmt.intern("msg"))
        self.set_msg_handler(pmt.intern("msg"), self.handle_msg)

    def print_vec(self, data):
        nums = [str(v) for v in data]
        st = self.variable_name + '=['
        st += ', '.join(nums) + '];'
        print(st)

    def handle_msg(self, msg):
        if self.enabled:
            name = pmt.pmt_python.pmt_base()
            samples = pmt.pmt_python.pmt_base()
            if pmt.is_pair(msg):
                name = pmt.car(msg)
                samples = pmt.cdr(msg)
                if pmt.symbol_to_string(name) != self.variable_name:
                    print('variable_name {} doesnt match {}'.format(self.variable_name, pmt.symbol_to_string(name)))
                    return
                if pmt.is_uniform_vector(samples):
                    self.print_vec(pmt.f32vector_elements(samples))
                elif pmt.is_number(samples):
                    print('{} = {}'.format(self.variable_name, pmt.to_double(samples)))
            elif pmt.is_uniform_vector(msg):
                samples = msg
                self.print_vec(pmt.f32vector_elements(msg))
            elif pmt.is_number(msg):
                print('{} = {}'.format(self.variable_name, pmt.to_double(msg)))
            else:
                print('bad data format')
            return


    def work(self, input_items, output_items):
        # if self.enabled:
        #     x = input_items[0]
        #     nums = [str(v) for v in x]
        #     st = self.variable_name + '=['
        #     st += ', '.join(nums) + '];'
        #     print(st)
        return len(input_items[0])
