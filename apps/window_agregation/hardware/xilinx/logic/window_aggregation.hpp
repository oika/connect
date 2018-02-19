#include "connect_platform.hpp"
#include "hls_stream.h"
#include "ap_int.h"

#define N_CAMPAIGNS 10
#define WINDOW_SIZE 8

struct window_event {
    ap_uint<32> timestamp;
    ap_uint<32> campaign;
};

struct window_result {
    ap_uint<16> timestamp;
    ap_uint<20> campaign;
    ap_uint<28> count;
};

void window_aggregation(hls::stream<ap_uint<64> >   &eventIn,
                        hls::stream<ap_uint<64> >   &resultOut,
                        hls::stream<ap_uint<1> >    &prepare_start,
                        hls::stream<ap_uint<1> >    &prepare_done);
