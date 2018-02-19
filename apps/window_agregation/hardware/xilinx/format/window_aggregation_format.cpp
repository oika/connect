#include "connect_platform.hpp"
#include "window_aggregation_format.hpp"

using namespace hls;

void window_aggregation_format(stream<axiWord>    &rxDataIn,
                               stream<evWord>     &rxEventOut,
                               stream<evWord>     &txEventIn,
                               stream<axiWord>    &txDataOut)
{
#pragma HLS DATAFLOW
#pragma HLS INTERFACE ap_ctrl_none port=return

#pragma HLS INTERFACE axis register both port=rxDataIn
#pragma HLS INTERFACE axis register both port=rxEventOut
#pragma HLS INTERFACE axis register both port=txEventIn
#pragma HLS INTERFACE axis register both port=txDataOut

    static enum RxState {S_RX_FIRST = 0, S_RX} rxState;
    static enum TxState {S_TX_FIRST = 0, S_TX} txState;

    switch (rxState) {
        case S_RX_FIRST:
            if (!rxDataIn.empty() && !rxEventOut.full()) {
                axiWord word;
                evWord event;

                word = rxDataIn.read();
                event.field0 = word.data;
                rxEventOut.write(event);
            }
            break;
        case S_RX:
            break;
    }

    switch (txState) {
        case S_TX_FIRST:
            if (!txEventIn.empty() && !txDataOut.full()) {
                axiWord word;
                evWord event;

                event = txEventIn.read();
                word.data = event.field0;
                word.keep = 0xff;
                word.last = 1;
                txDataOut.write(word);
            }
            break;
        case S_TX:
            break;
    }
}
