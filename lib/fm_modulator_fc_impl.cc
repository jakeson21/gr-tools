/* -*- c++ -*- */
/*
 * Copyright 2021 Jacob Miller.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#include <gnuradio/io_signature.h>
#include "fm_modulator_fc_impl.h"

/*
    // change the signature in gr-tools/python/bindings/fm_modulator_fc_python.cc to:
    py::class_<fm_modulator_fc, gr::sync_block,
              gr::block, gr::basic_block,
        std::shared_ptr<fm_modulator_fc>>(m, "fm_modulator_fc", D(fm_modulator_fc))

        .def(py::init(&fm_modulator_fc::make),
           py::arg("samp_rate"),
           py::arg("deviation"),
           py::arg("initial_phase"),
           D(fm_modulator_fc,make)
        )
        
        .def("set_freq_deviation", &fm_modulator_fc::set_freq_deviation, py::arg("deviation"))
        .def("freq_deviation", &fm_modulator_fc::freq_deviation);
*/


namespace gr {
  namespace tools {

    using input_type = float;
    using output_type = gr_complex;
    fm_modulator_fc::sptr
    fm_modulator_fc::make(float samp_rate=1, float deviation=1, float initial_phase=0)
    {
      return gnuradio::make_block_sptr<fm_modulator_fc_impl>(samp_rate, deviation, initial_phase);
    }


    /*
     * The private constructor
     */
    fm_modulator_fc_impl::fm_modulator_fc_impl(float samp_rate, float deviation, float initial_phase)
      : gr::sync_block("fm_modulator_fc",
              gr::io_signature::make(1, 1, sizeof(input_type)),
              gr::io_signature::make(1, 1, sizeof(output_type))),
              last_phase(initial_phase),
              d_freq_deviation(deviation),
              samp_rate(samp_rate)
    {
    }

    /*
     * Our virtual destructor.
     */
    fm_modulator_fc_impl::~fm_modulator_fc_impl()
    {
    }


    void fm_modulator_fc_impl::set_freq_deviation(float deviation)
    {
        gr::thread::scoped_lock l(this->d_setlock);
        this->d_freq_deviation = deviation;
    }

    int
    fm_modulator_fc_impl::work(int noutput_items,
        gr_vector_const_void_star &input_items,
        gr_vector_void_star &output_items)
    {
        gr::thread::scoped_lock l(this->d_setlock);
        const input_type *in = reinterpret_cast<const input_type*>(input_items[0]);
        output_type *out = reinterpret_cast<output_type*>(output_items[0]);

        // Do <+signal processing+>
        const gr_complex j(0.0, 1.0);
        const float wd = 2.0*M_PI*this->d_freq_deviation/this->samp_rate;
        for (size_t n=0; n<noutput_items; n++)
        {
            this->last_phase = this->last_phase + wd*in[n];
            out[n] = std::exp(j*this->last_phase);
        }

        // Tell runtime system how many output items we produced.
        return noutput_items;
    }

  } /* namespace tools */
} /* namespace gr */

