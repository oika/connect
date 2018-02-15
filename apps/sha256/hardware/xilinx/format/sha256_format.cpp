#include "sha256_format.hpp"
#include "connect_platform.hpp"
#include "hls_stream.h"

using namespace hls;
using namespace std;

void sha256_format(stream<axiWord>          &rxDataIn,
                   stream<ap_uint<1024> >   &rxEventOut,
                   stream<ap_uint<32> >     &txEventIn,
                   stream<axiWord>          &txDataOut)
{
#pragma HLS DATAFLOW
#pragma HLS INTERFACE ap_ctrl_none port=return

#pragma HLS resource core=AXI4Stream variable=rxDataIn
#pragma HLS resource core=AXI4Stream variable=rxEventOut
#pragma HLS resource core=AXI4Stream variable=txEventIn
#pragma HLS resource core=AXI4Stream variable=txDataOut

#pragma HLS DATA_PACK variable=rxEventOut
#pragma HLS DATA_PACK variable=txDataOut
#pragma HLS DATA_PACK variable=txEventIn
#pragma HLS DATA_PACK variable=rxDataIn

    static ap_uint<64>  rxEvent[16];
#pragma HLS ARRAY_PARTITION variable=rxEvent complete dim=1
    static ap_uint<4>   rx_count = 0;

    if (!rxDataIn.empty() && !rxEventOut.full()) {
        axiWord word = rxDataIn.read();
        rxEvent[rx_count] = word.data;
        if (word.last) {
            rx_count = 0;
            ap_uint<1024> rxEventFull = (rxEvent[0], (rxEvent[1], (rxEvent[2], (rxEvent[3],
            							 rxEvent[4], (rxEvent[5], (rxEvent[6], (rxEvent[7],
            							 rxEvent[8], (rxEvent[9], (rxEvent[10], (rxEvent[11],
            							 rxEvent[12], (rxEvent[13], (rxEvent[14], rxEvent[15]))))))))))));
            rxEventOut.write(rxEventFull);
        } else {
            ++rx_count;
        }
    }

    if (!txEventIn.empty() && !txDataOut.full()) {
        axiWord word;

        ap_uint<32> txEvent = txEventIn.read();
        word.data = (ap_uint<64>)txEvent;
        word.keep = 0x0f;
        word.last = 1;
        txDataOut.write(word);
    }
}
