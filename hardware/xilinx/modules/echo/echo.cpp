#include "connect_platform.hpp"

using namespace hls;

void echo(stream<ap_uint<64> >  &eventIn,
          stream<ap_uint<64> >  &resultOut,
          stream<ap_uint<1> >   &prepare_start,
          stream<ap_uint<1> >   &prepare_done)
{
#pragma HLS INTERFACE axis register both port=eventIn
#pragma HLS INTERFACE axis register both port=resultOut
#pragma HLS INTERFACE axis register both port=prepare_start
#pragma HLS INTERFACE axis register both port=prepare_done
#pragma HLS INTERFACE ap_ctrl_none port=return


    if (!prepare_start.empty() && !prepare_done.full()) {
        prepare_done.write(prepare_start.read());
    }

    if (!eventIn.empty() && !resultOut.full()) {
        resultOut.write(eventIn.read());
    }

    return;
}
