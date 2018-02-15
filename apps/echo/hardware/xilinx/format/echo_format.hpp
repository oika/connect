#include <stdio.h>
#include <hls_stream.h>
#include "ap_int.h"

#define EV_WIDTH 64

struct evWord {
    ap_uint<EV_WIDTH> field0;
};

void echo_format(hls::stream<axiWord>    &rxDataIn,
                 hls::stream<evWord>     &rxEventOut,
                 hls::stream<evWord>     &txEventIn,
                 hls::stream<axiWord>    &txDataOut);
