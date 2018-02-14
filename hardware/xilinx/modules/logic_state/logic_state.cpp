#include "ap_int.h"
#include "hls_stream.h"
#include "connect_platform.hpp"
#include "logic_state.hpp"

using namespace hls;

void logic_state(stream<axiWord>                &rxDataIn,
                 stream<axiWord>                &rxDataOut,
                 stream<axiWord>                &txDataIn,
                 stream<axiWord>                &txDataOut,
                 stream<ap_uint<CMD_WIDTH> >    &commandIn,
                 stream<ap_uint<STATE_WIDTH> >  &stateOut,
                 stream<ap_uint<1> >            &prepare_start,
                 stream<ap_uint<1> >            &prepare_done)
{
#pragma HLS DATAFLOW
#pragma HLS INTERFACE ap_ctrl_none port=return

#pragma HLS INTERFACE axis register both port=prepare_done
#pragma HLS INTERFACE axis register both port=prepare_start
#pragma HLS INTERFACE axis register both port=txDataOut
#pragma HLS INTERFACE axis register both port=txDataIn
#pragma HLS INTERFACE axis register both port=rxDataOut
#pragma HLS INTERFACE axis register both port=rxDataIn
#pragma HLS INTERFACE axis register both port=commandIn
#pragma HLS INTERFACE axis register both port=stateOut

    static enum LogicState {LS_IDLE = 0, LS_ASSIGNED, LS_PREPARING, LS_READY, LS_RUNNING, LS_CANCELLING} lState;
    static bool packet_done = true;

    if (!txDataIn.empty() && !txDataOut.full()) {
        txDataOut.write(txDataIn.read());
    }

    switch (lState) {
        case LS_IDLE:
            if (!rxDataIn.empty()) {
                axiWord rx = rxDataIn.read();
                packet_done = rx.last;
            }

            if (!commandIn.empty() && !stateOut.full()) {
                ap_uint<CMD_WIDTH> cmd;
                cmd = commandIn.read();
                if (cmd == CMD_SUBMIT) {
                    lState = LS_ASSIGNED;
                    stateOut.write(LS_ASSIGNED);
                }
            }
            break;
        case LS_ASSIGNED:
            if (!rxDataIn.empty()) {
                axiWord rx = rxDataIn.read();
                packet_done = rx.last;
            }

            if (!commandIn.empty() && !stateOut.full()) {
                ap_uint<CMD_WIDTH> cmd;
                cmd = commandIn.read();
                if (cmd == CMD_PREPARE) {
                    lState = LS_PREPARING;
                    prepare_start.write(1);
                } else if (cmd == CMD_CANCEL) {
                    lState = LS_CANCELLING;
                }
            }
            break;
        case LS_PREPARING:
            if (!rxDataIn.empty()) {
                axiWord rx = rxDataIn.read();
                packet_done = rx.last;
            }

            if (!stateOut.full() && !prepare_done.empty()) {
                if (prepare_done.read()) {
                    lState = LS_READY;
                    stateOut.write(LS_READY);
                }
            }
            break;
        case LS_READY:
            if (!rxDataIn.empty()) {
                axiWord rx = rxDataIn.read();
                packet_done = rx.last;
            }

            if (packet_done && !commandIn.empty() && !stateOut.full()) {
                ap_uint<CMD_WIDTH> cmd;
                cmd = commandIn.read();
                if (cmd == CMD_RUN) {
                    lState = LS_RUNNING;
                    stateOut.write(LS_RUNNING);
                } else if (cmd == CMD_PREPARE) {
                    lState = LS_PREPARING;
                } else if (cmd == CMD_CANCEL) {
                    lState = LS_CANCELLING;
                }
            }
            break;
        case LS_RUNNING:
            if (!rxDataIn.empty() && !rxDataOut.full()) {
                axiWord rx = rxDataIn.read();
                rxDataOut.write(rx);
                packet_done = rx.last;
            }

            if (packet_done && !commandIn.empty() && !stateOut.full()) {
                ap_uint<CMD_WIDTH> cmd;
                cmd = commandIn.read();
                if (cmd == CMD_PAUSE) {
                    lState = LS_READY;
                    stateOut.write(LS_READY);
                } else if (cmd == CMD_CANCEL) {
                    lState = LS_CANCELLING;
                }
            }
            break;
        case LS_CANCELLING:
            if (!rxDataIn.empty()) {
                axiWord rx = rxDataIn.read();
                packet_done = rx.last;
            }
            if (!stateOut.full()) {
                lState = LS_IDLE;
                stateOut.write(LS_IDLE);
            }
            break;
    }
}
