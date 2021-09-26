/* -*- c++ -*- */
/*
 * Copyright 2021 Jacob Miller.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_TOOLS_FM_MODULATOR_FC_IMPL_H
#define INCLUDED_TOOLS_FM_MODULATOR_FC_IMPL_H

#include <tools/fm_modulator_fc.h>

namespace gr {
  namespace tools {

    class fm_modulator_fc_impl : public fm_modulator_fc
    {
    private:
        // Nothing to declare in this block.
        float last_phase = 0;
        float d_freq_deviation = 0;
        float samp_rate = 0;

    public:
        fm_modulator_fc_impl(float samp_rate, float deviation, float initial_phase);
        ~fm_modulator_fc_impl();

        void set_freq_deviation(float deviation) override;
        float freq_deviation() const override { return d_freq_deviation; }

        // Where all the action really happens
        int work(int noutput_items, gr_vector_const_void_star &input_items, gr_vector_void_star &output_items);
    };

  } // namespace tools
} // namespace gr

#endif /* INCLUDED_TOOLS_FM_MODULATOR_FC_IMPL_H */

