#include "hls_stream.h"
#include "ap_int.h"
#include "connect_platform.hpp"

void logic_state(hls::stream<axiWord>                &rxDataIn,
                 hls::stream<axiWord>                &rxDataOut,
                 hls::stream<axiWord>                &txDataIn,
                 hls::stream<axiWord>                &txDataOut,
                 hls::stream<ap_uint<CMD_WIDTH> >    &commandIn,
                 hls::stream<ap_uint<STATE_WIDTH> >  &stateOut,
                 hls::stream<ap_uint<1> >            &prepare_start,
                 hls::stream<ap_uint<1> >            &prepare_done);
