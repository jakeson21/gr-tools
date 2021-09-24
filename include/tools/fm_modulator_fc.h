/* -*- c++ -*- */
/*
 * Copyright 2021 Jacob Miller.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_TOOLS_FM_MODULATOR_FC_H
#define INCLUDED_TOOLS_FM_MODULATOR_FC_H

#include <tools/api.h>
#include <gnuradio/sync_block.h>

namespace gr {
  namespace tools {

    /*!
     * \brief <+description of block+>
     * \ingroup tools
     *
     */
    class TOOLS_API fm_modulator_fc : virtual public gr::sync_block
    {
     public:
      typedef std::shared_ptr<fm_modulator_fc> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of tools::fm_modulator_fc.
       *
       * To avoid accidental use of raw pointers, tools::fm_modulator_fc's
       * constructor is in a private implementation
       * class. tools::fm_modulator_fc::make is the public interface for
       * creating new instances.
       */
      static sptr make(float samp_rate, float freq_deviation, float initial_phase);
    };

  } // namespace tools
} // namespace gr

#endif /* INCLUDED_TOOLS_FM_MODULATOR_FC_H */

