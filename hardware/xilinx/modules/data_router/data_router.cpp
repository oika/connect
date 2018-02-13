#include "connect_platform.hpp"

using namespace hls;

void data_router(stream<axiWord>                &rxDataIn,
                 stream<metadata>               &rxMetadataIn,
                 stream<axiWord>                &rxDataOut,
                 stream<axiWord>                &txDataIn,
                 stream<axiWord>                &txDataOut,
                 stream<metadata>               &txMetadataOut,
                 stream<ap_uint<16> >           &txLengthOut,
                 stream<ap_uint<CMD_WIDTH> >    &commandOut,
                 stream<nwif_ports>             &portsOut,
                 stream<bool>                   &commandReplyIn)
{
#pragma HLS INTERFACE ap_ctrl_none port=return
#pragma HLS DATAFLOW

#pragma HLS INTERFACE axis register both port=rxDataIn
#pragma HLS INTERFACE axis register both port=rxMetadataIn
#pragma HLS INTERFACE axis register both port=rxDataOut
#pragma HLS INTERFACE axis register both port=txDataIn
#pragma HLS INTERFACE axis register both port=txDataOut
#pragma HLS INTERFACE axis register both port=txMetadataOut
#pragma HLS INTERFACE axis register both port=txLengthOut
#pragma HLS INTERFACE axis register both port=commandOut
#pragma HLS INTERFACE axis register both port=portsOut
#pragma HLS INTERFACE axis register both port=commandReplyIn

#pragma HLS DATA_PACK variable=txMetadataOut
#pragma HLS DATA_PACK variable=rxMetadataIn
#pragma HLS DATA_PACK variable=portsOut

    static const ap_uint<16> tm_port = 5440;

    static enum RxState {MYSTR_RX_FIRST = 0, MYSTR_RX_TM_SECOND, MYSTR_RX_TM_WAIT, MYSTR_RX_LOGIC} rxState;
    static enum TxState {MYSTR_TX_FIRST = 0, MYSTR_TX} txState;

    static ap_uint<16> logic_self_port;
    static ap_uint<16> logic_dest_port;
    static ap_uint<32> self_addr;
    static ap_uint<32> dest_addr;
    static ap_uint<16> out_len = 0;
    static ap_uint<16> packetLength = 0;

    switch(rxState) {
        case MYSTR_RX_FIRST:
            if (!rxDataIn.empty() && !rxMetadataIn.empty() &&
                !rxDataOut.full() && !commandOut.full() && !portsOut.full()) {

                axiWord word = rxDataIn.read();
                metadata in_meta = rxMetadataIn.read();
                self_addr = in_meta.destinationSocket.addr;

                if (in_meta.destinationSocket.port == tm_port) {
                    ap_uint<32> in_command = word.data.range(31, 0);
                    nwif_ports ports;
                    if (in_command == CMD_SUBMIT) {
                        logic_self_port = word.data.range(47, 32);
                        logic_dest_port = word.data.range(63, 48);
                        ports.selfPort = logic_self_port;
                        ports.destPort = logic_dest_port;
                        portsOut.write(ports);
                        rxState = MYSTR_RX_TM_SECOND;
                    } else {
                        rxState = MYSTR_RX_TM_WAIT;
                    }
                    commandOut.write(in_command);
                } else if (in_meta.destinationSocket.port == logic_self_port) {
                    rxDataOut.write(word);
                    if (!word.last) {
                        rxState = MYSTR_RX_LOGIC;
                    }
                }
            }
            break;
        case MYSTR_RX_TM_SECOND:
            if (!rxDataIn.empty()) {
                axiWord word = rxDataIn.read();
                dest_addr = word.data.range(31, 0);
                rxState = MYSTR_RX_TM_WAIT;
            }
            break;
        case MYSTR_RX_TM_WAIT:
            if (!commandReplyIn.empty()) {
                if (commandReplyIn.read()) {
                   rxState = MYSTR_RX_FIRST;
                }
            }
            break;
        case MYSTR_RX_LOGIC:
            if (!rxDataIn.empty() && !rxDataOut.full()) {
                axiWord word = rxDataIn.read();
                rxDataOut.write(word);
                if (word.last) {
                    rxState = MYSTR_RX_FIRST;
                }
            }
            break;
    }

    switch(txState) {
        case MYSTR_TX_FIRST:
            if (!txDataIn.empty() && !txDataOut.full() &&
                !txMetadataOut.full() && !txLengthOut.full()) {

                axiWord word = txDataIn.read();
                txDataOut.write(word);

                metadata out_meta;
                out_meta.sourceSocket.addr = self_addr;
                out_meta.sourceSocket.port = logic_self_port;
                out_meta.destinationSocket.addr = dest_addr;
                out_meta.destinationSocket.port = logic_dest_port;
                txMetadataOut.write(out_meta);

                ap_uint<4> counter = 0;
                for (ap_uint<8> i = 0; i < 8; ++i) {
#pragma HLS UNROLL
                    if (word.keep.bit(i) == 1) {
                        ++counter;
                    }
                }
                packetLength += counter;
                if (word.last) {
                    txLengthOut.write(packetLength);
                    packetLength = 0;
                } else {
                    txState = MYSTR_TX;
                }
            }
            break;
        case MYSTR_TX:
            if (!txDataIn.empty() && !txDataOut.full() && !txLengthOut.full()) {

                axiWord word = txDataIn.read();
                txDataOut.write(word);

                ap_uint<4> counter = 0;
                for (ap_uint<8> i = 0; i < 8; ++i) {
#pragma HLS UNROLL
                    if (word.keep.bit(i) == 1) {
                        ++counter;
                    }
                }
                packetLength += counter;
                if (word.last) {
                    txLengthOut.write(packetLength);
                    packetLength = 0;
                    txState = MYSTR_TX_FIRST;
                }
            }
            break;
    }
}
