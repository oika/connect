#include "sha256.hpp"
#include "ap_int.h"
#include "hls_stream.h"
#include <iostream>

using namespace std;
using namespace hls;

int main(void)
{
    stream<ap_uint<1024> >  in_stream;
    stream<ap_uint<32> >    out_stream;
    stream<ap_uint<1> >     prepare_start;
    stream<ap_uint<1> >     prepare_done;
    //ap_uint<256>            final_hash;

    ap_uint<1024> header = ((ap_uint<64>)0x0001020304050607,
                           ((ap_uint<64>)0x08090a0b0c0d0e0f,
                           ((ap_uint<64>)0x1011121314151617,
                           ((ap_uint<64>)0x18191a1b1c1d1e1f,
                           ((ap_uint<64>)0x2021222324252627,
                           ((ap_uint<64>)0x28292a2b2c2d2e2f,
                           ((ap_uint<64>)0x3031323334353637,
                           ((ap_uint<64>)0x38393a3b3c3d3e3f,
                           ((ap_uint<64>)0x4041424344454647,
                           ((ap_uint<64>)0x200000ff00000000,
                           ((ap_uint<64>)0x8000000000000000,
                           ((ap_uint<64>)0x0000000000000000,
                           ((ap_uint<64>)0x0000000000000000,
                           ((ap_uint<64>)0x0000000000000000,
                           ((ap_uint<64>)0x0000000000000000,
                           ((ap_uint<64>)0x0000000000000280))))))))))))))));

    //cout << hex << header << endl;
    in_stream.write(header);
    prepare_start.write(1);
    
    while (1) {
        sha256(in_stream, out_stream, prepare_start, prepare_done);
        //cout << hex << final_hash << endl;
        if (!out_stream.empty()) {
            break;
        }
    }
    cout << hex << out_stream.read() << endl;

    return 0;
}

