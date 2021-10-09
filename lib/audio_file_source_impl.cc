/* -*- c++ -*- */
/*
 * Copyright 2021 Jacob Miller.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

#include <gnuradio/io_signature.h>
#include "audio_file_source_impl.h"
#include <stdexcept>
#include <sstream>

namespace gr {
  namespace tools {

    using output_type = float;
    audio_file_source::sptr
    audio_file_source::make(std::string file_name, float samp_rate_out, int channels, bool loop, bool normalize)
    {
        return gnuradio::make_block_sptr<audio_file_source_impl>(file_name, samp_rate_out, channels, loop, normalize);
    }

    static bool abs_compare(float a, float b)
    {
        return (std::abs(a) < std::abs(b));
    }

    template<class Compare>
    float max_abs_element(const float* first, size_t length, Compare comp)
    {
        if (length == 1) return *first;
    
        float largest = *first;
        const float* last = first + length;
        ++first;
        for (; first != last; ++first) {
            if (comp(largest, *first)) {
                largest = *first;
            }
        }
        return largest;
    }

    /*
     * The private constructor
     */
    audio_file_source_impl::audio_file_source_impl(std::string file_name, float samp_rate_out, int channels, bool loop, bool normalize=true)
      : gr::sync_block("audio_file_source",
        gr::io_signature::make(0, 0, 0),
        gr::io_signature::make(1 /* min outputs */, channels /*max outputs */, sizeof(output_type)))
    {
        this->file_name = file_name;
        this->samp_rate_out = samp_rate_out;
        this->num_outputs = channels;
        this->loop = loop;

        this->mp3_audio = drmp3_open_file_and_read_pcm_frames_f32(this->file_name.c_str(), &this->mp3_config, &this->totalFrameCount, NULL);
        this->channels = mp3_config.channels;
        drmp3_uint32 sampleRate = mp3_config.sampleRate;

        if (normalize)
        {
            float max_abs = max_abs_element(this->mp3_audio, this->totalFrameCount*this->channels, abs_compare);
            for (size_t n=0; n<this->totalFrameCount*this->channels; ++n)
            {
                *this->mp3_audio /= max_abs;
            }
        }

        if (this->num_outputs > this->channels)
        {
            std::stringstream ss;
            ss << "Audio contains only " << this->channels << " channels";
            throw std::out_of_range(ss.str());
        }

        if (this->samp_rate_out > sampleRate)
        {
            std::stringstream ss;
            ss << "Audio is sampled at " << sampleRate << " Hz";
            throw std::out_of_range(ss.str());
        }

        set_output_multiple(this->num_outputs);

        std::cout << "Loaded " << this->file_name << std::endl;
        std::cout << "  " << this->channels << " channels" << std::endl;
        std::cout << "  " << this->totalFrameCount << " samples per channel" << std::endl;
        std::cout << "  " << sampleRate << " sample rate" << std::endl;

        std::cout << "Using " << this->num_outputs << " channels" << std::endl;
        std::cout << "Looping " << this->loop << std::endl;
    }

    /*
     * Our virtual destructor.
     */
    audio_file_source_impl::~audio_file_source_impl()
    {
    }

    int
    audio_file_source_impl::work(int noutput_items,
        gr_vector_const_void_star &input_items,
        gr_vector_void_star &output_items)
    {
        output_type *out = reinterpret_cast<output_type*>(output_items[0]);

        unsigned int n, i;
        size_t noutputs = output_items.size();
        float* in = this->mp3_audio + frameNum*this->channels;
        float zeros[2] = {0.0, 0.0};

        // Do <+signal processing+>
        for (n = 0; n < noutput_items; n++) {
            if (!this->loop && frameNum >= totalFrameCount)
            {
                for (i = 0; i < this->num_outputs; i++) {
                    out = reinterpret_cast<output_type*>(output_items[i]);
                    out[n] = zeros[i];
                }
                continue;
            }

            for (i = 0; i < this->num_outputs; i++) {
                out = reinterpret_cast<output_type*>(output_items[i]);
                out[n] = in[i];
            }

            in += this->channels;
            frameNum++;
            frameNum = frameNum % totalFrameCount;
        }
        // Tell runtime system how many output items we produced.
        return noutput_items;
    }

  } /* namespace tools */
} /* namespace gr */

