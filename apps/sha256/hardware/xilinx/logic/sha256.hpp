#include "ap_int.h"
#include "hls_stream.h"

void sha256(hls::stream<ap_uint<1024> > &eventIn,
            hls::stream<ap_uint<32> >   &resultOut,
            hls::stream<ap_uint<1> >    &prepare_start,
            hls::stream<ap_uint<1> >    &prepare_done);
            //ap_uint<256>                &final_hash);
