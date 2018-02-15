#include "connect_platform.hpp"
#include "hls_stream.h"
#include "ap_int.h"

using namespace hls;

void axis_timer(stream<ap_uint<1> >  &intr_stream)
{
#pragma HLS DATAFLOW
#pragma HLS INTERFACE ap_ctrl_none port=return

#pragma HLS INTERFACE axis register both port=intr_stream

    static ap_uint<7> count = 0;

    if (count++ == 0b1111111 && !intr_stream.full()) {
        intr_stream.write(1);
    }
}
