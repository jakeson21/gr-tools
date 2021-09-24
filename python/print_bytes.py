#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2021 Jacob Miller.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

  
import numpy as np
from gnuradio import gr

class print_bytes(gr.sync_block):
    """
    docstring for block print_bytes
    """
    def __init__(self, label='', enabled=True):
        gr.sync_block.__init__(self,
            name="print_bytes",
            in_sig=[np.byte],
            out_sig=None)
        self.label = label
        self.enabled = enabled

    def work(self, input_items, output_items):
        if self.enabled:
            x = input_items[0]
            nums = [str(v) for v in x]
            st = self.label + '=['
            st += ', '.join(nums) + '];'
            print(st)
        return len(input_items[0])
        
