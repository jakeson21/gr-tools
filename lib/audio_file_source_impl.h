/* -*- c++ -*- */
/*
 * Copyright 2021 Jacob Miller.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#ifndef INCLUDED_TOOLS_AUDIO_FILE_SOURCE_IMPL_H
#define INCLUDED_TOOLS_AUDIO_FILE_SOURCE_IMPL_H

#include <tools/audio_file_source.h>

#define DR_MP3_IMPLEMENTATION
#include "dr_mp3.h"

namespace gr {
    namespace tools {

    class audio_file_source_impl : public audio_file_source
    {
    private:
        // Nothing to declare in this block.
        std::string file_name;
        int num_outputs;
        float samp_rate_out;
        bool loop;

        float* mp3_audio = NULL;
        drmp3_config mp3_config;
        drmp3_uint32 channels = 0;
        drmp3_uint32 sampleRate = 0;
        drmp3_uint64 totalFrameCount = 0;
        int64_t frameNum = 0;
      
    public:
        audio_file_source_impl(std::string file_name, float samp_rate_out, int channels, bool loop, bool normalize);
        ~audio_file_source_impl();

        // Where all the action really happens
        int work(int noutput_items, gr_vector_const_void_star &input_items, gr_vector_void_star &output_items);
    };

    } // namespace tools
} // namespace gr

#endif /* INCLUDED_TOOLS_AUDIO_FILE_SOURCE_IMPL_H */

