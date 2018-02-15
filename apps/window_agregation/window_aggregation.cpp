#include "window_aggregation.hpp"

using namespace hls;

void switch_buf(ap_uint<1> &in_buf, ap_uint<1> &out_buf)
{
#pragma HLS INLINE
    if (in_buf == 1) {
        in_buf = 0;
        out_buf = 1;
    } else {
        in_buf = 1;
        out_buf = 0;
    }
}

window_event extract_event(ap_uint<64> uint_event)
{
#pragma HLS INLINE
    window_event event;
    event.timestamp = uint_event.range(31, 0);
    event.campaign = uint_event.range(63, 32);
    return event;
}

ap_uint<64> pack_result(window_result result)
{
#pragma HLS INLINE
    ap_uint<64> uint_result;
    uint_result = (result.count, (result.campaign, result.timestamp));
    return uint_result;
}

void window_aggregation(stream<ap_uint<64> >            &eventIn,
                        stream<ap_uint<64> >            &resultOut,
                        stream<ap_uint<CMD_WIDTH> >     &commandIn,
                        stream<ap_uint<STATE_WIDTH> >   &stateOut,
                        ap_uint<3>                      *logic_state_out,
                        ap_uint<1>                      *output_state_out)
{
#pragma HLS INTERFACE ap_vld port=output_state_out
#pragma HLS INTERFACE ap_vld port=logic_state_out
#pragma HLS DATAFLOW
#pragma HLS INTERFACE ap_ctrl_none port=return

#pragma HLS INTERFACE axis register both port=eventIn
#pragma HLS INTERFACE axis register both port=resultOut
#pragma HLS INTERFACE axis register both port=commandIn
#pragma HLS INTERFACE axis register both port=stateOut

    static enum LogicState {LS_IDLE = 0, LS_ASSIGNED, LS_PREPARING, LS_READY, LS_RUNNING, LS_CANCELLING} lState;
    static enum OutputState {OS_DONE = 0, OS_FLUSHING} oState;

    static ap_uint<8>  counts[2][N_CAMPAIGNS];
    static ap_uint<1>   in_buf = 0;
    static ap_uint<1>   out_buf = 1;

    static ap_uint<1>   initialized = 0;
    static ap_uint<32>  checkpoint[2];
    static ap_uint<32>  out_index = 0;

    switch (lState) {
        case LS_IDLE:
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
            if (!commandIn.empty() && !stateOut.full()) {
                ap_uint<CMD_WIDTH> cmd;
                cmd = commandIn.read();
                if (cmd == CMD_PREPARE) {
                    lState = LS_PREPARING;
                    stateOut.write(LS_PREPARING);
                } else if (cmd == CMD_CANCEL) {
                    lState = LS_CANCELLING;
                    stateOut.write(LS_CANCELLING);
                }
            }
            break;
        case LS_PREPARING:
            if (!stateOut.full()) {
                for (int i = 0; i < 2; ++i) {
                    for (int j = 0; j < N_CAMPAIGNS; ++j) {
                        counts[i][j] = 0;
                    }
                }
                lState = LS_READY;
                stateOut.write(LS_READY);
            }
            break;
        case LS_READY:
            if (!commandIn.empty() && !stateOut.full()) {
                ap_uint<CMD_WIDTH> cmd;
                cmd = commandIn.read();
                if (cmd == CMD_RUN) {
                    lState = LS_RUNNING;
                    stateOut.write(LS_RUNNING);
                } else if (cmd == CMD_PREPARE) {
                    lState = LS_PREPARING;
                    stateOut.write(LS_PREPARING);
                } else if (cmd == CMD_CANCEL) {
                    lState = LS_CANCELLING;
                    stateOut.write(LS_CANCELLING);
                }
            }
            break;
        case LS_RUNNING:
            if (!eventIn.empty()) {
                window_event event;
                event = extract_event(eventIn.read());

                if (!initialized) {
                    checkpoint[in_buf] = event.timestamp;
                    initialized = 1;
                }

                if (event.timestamp >= checkpoint[in_buf] + WINDOW_SIZE) {
                    oState = OS_FLUSHING;
                    ap_uint<32> new_checkpoint = (event.timestamp - checkpoint[in_buf]) / WINDOW_SIZE * WINDOW_SIZE
                                               + checkpoint[in_buf];
                    switch_buf(in_buf, out_buf);
                    checkpoint[in_buf] = new_checkpoint;
                }

                counts[in_buf][event.campaign] += 1;
            }
            switch (oState) {
                case OS_DONE:
                    break;
                case OS_FLUSHING:
                    if (!resultOut.full()) {
                        window_result result;
                        result.timestamp = checkpoint[out_buf];
                        result.campaign = out_index;
                        result.count = (ap_uint<28>)counts[out_buf][out_index];
                        counts[out_buf][out_index] = 0;
                        if (out_index == N_CAMPAIGNS - 1) {
                            out_index = 0;
                            oState = OS_DONE;
                        } else {
                            ++out_index;
                        }
                        resultOut.write(pack_result(result));
                    }
                    break;
            }
            if (!commandIn.empty() && !stateOut.full()) {
                ap_uint<CMD_WIDTH> cmd;
                cmd = commandIn.read();
                if (cmd == CMD_PREPARE) {
                    lState = LS_PREPARING;
                    stateOut.write(LS_PREPARING);
                } else if (cmd == CMD_PAUSE) {
                    lState = LS_READY;
                    stateOut.write(LS_READY);
                } else if (cmd == CMD_CANCEL) {
                    lState = LS_CANCELLING;
                    stateOut.write(LS_CANCELLING);
                }
            }
            break;
        case LS_CANCELLING:
            if (!stateOut.full()) {
                lState = LS_IDLE;
                stateOut.write(LS_IDLE);
            }
            break;
    }
    *logic_state_out = lState;
    *output_state_out = oState;
}
