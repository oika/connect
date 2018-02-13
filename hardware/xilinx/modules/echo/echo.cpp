#include "connect_platform.hpp"

using namespace hls;

void echo(stream<axiWord>       &tx_data,
          stream<metadata>      &tx_meta,
          stream<ap_uint<16> >  &tx_length,
          stream<axiWord>       &rx_data,
          stream<metadata>      &rx_meta,
          stream<ap_uint<16> >  &open_port_request,
          stream<ap_uint<1> >   &open_port_reply)
{
#pragma HLS INTERFACE axis register both port=open_port_reply
#pragma HLS INTERFACE axis register both port=open_port_request
#pragma HLS DATA_PACK variable=tx_meta
#pragma HLS DATA_PACK variable=rx_meta
#pragma HLS INTERFACE axis register both port=rx_meta
#pragma HLS INTERFACE axis register both port=rx_data
#pragma HLS INTERFACE axis register both port=tx_meta
#pragma HLS INTERFACE axis register both port=tx_data
#pragma HLS INTERFACE axis register both port=tx_length
#pragma HLS INTERFACE ap_ctrl_none port=return

    static enum State {INIT_WAIT = 0, PORT_OPEN, PORT_WAIT, DO_JOB} state;
    static ap_uint<16> wait_count = 0;

    switch (state) {
        case INIT_WAIT:
            if (wait_count++ == 0xffff) {
                state = PORT_OPEN;
            }
            break;
        case PORT_OPEN:
            if (!open_port_request.full()) {
                open_port_request.write(5440);
                state = PORT_WAIT;
            }
            break;
        case PORT_WAIT:
            if (!open_port_reply.empty()) {
                ap_uint<1> open_success = open_port_reply.read();
                if (open_success) {
                    state = DO_JOB;
                }
            }
            break;
        case DO_JOB:
            if (!tx_data.full() && !rx_data.empty()) {
                axiWord w = rx_data.read();
                tx_data.write(w);
            }

            if (!tx_meta.full() && !rx_meta.empty() && !tx_length.full()) {
                ap_uint<32> tmp_src_addr;
                ap_uint<16> tmp_src_port;

                metadata meta = rx_meta.read();
                tmp_src_addr = meta.sourceSocket.addr;
                tmp_src_port = meta.sourceSocket.port;
                meta.sourceSocket.addr = meta.destinationSocket.addr;
                meta.sourceSocket.port = meta.destinationSocket.port;
                meta.destinationSocket.addr = tmp_src_addr;
                meta.destinationSocket.port = 5430;
                tx_meta.write(meta);
                tx_length.write(8);
            }
            break;
    }


    return;
}
