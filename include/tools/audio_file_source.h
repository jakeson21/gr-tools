/* -*- c++ -*- */
/*
 * Copyright 2021 Jacob Miller.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_TOOLS_AUDIO_FILE_SOURCE_H
#define INCLUDED_TOOLS_AUDIO_FILE_SOURCE_H

#include <tools/api.h>
#include <gnuradio/sync_block.h>

namespace gr {
  namespace tools {

    /*!
     * \brief <+description of block+>
     * \ingroup tools
     *
     */
    class TOOLS_API audio_file_source : virtual public gr::sync_block
    {
     public:
      typedef std::shared_ptr<audio_file_source> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of tools::audio_file_source.
       *
       * To avoid accidental use of raw pointers, tools::audio_file_source's
       * constructor is in a private implementation
       * class. tools::audio_file_source::make is the public interface for
       * creating new instances.
       */
      static sptr make(std::string file_name, float samp_rate_out, int channels=1, bool loop=true, bool normalize=false);
    };

  } // namespace tools
} // namespace gr

#endif /* INCLUDED_TOOLS_AUDIO_FILE_SOURCE_H */

