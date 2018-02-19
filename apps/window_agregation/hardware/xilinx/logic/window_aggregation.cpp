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

void window_aggregation(stream<ap_uint<64> >    &eventIn,
                        stream<ap_uint<64> >    &resultOut,
                        stream<ap_uint<1> >     &prepare_start,
                        stream<ap_uint<1> >     &prepare_done)
{
#pragma HLS DATAFLOW
#pragma HLS INTERFACE ap_ctrl_none port=return

#pragma HLS INTERFACE axis register both port=eventIn
#pragma HLS INTERFACE axis register both port=resultOut
#pragma HLS INTERFACE axis register both port=prepare_start
#pragma HLS INTERFACE axis register both port=prepare_done

    static enum LogicState {RUNNING = 0, PREPARING} lState;
    static enum OutputState {OS_DONE = 0, OS_FLUSHING} oState;

    static ap_uint<8>   counts[2][N_CAMPAIGNS];
    static ap_uint<1>   in_buf = 0;
    static ap_uint<1>   out_buf = 1;

    static ap_uint<1>   initialized = 0;
    static ap_uint<32>  checkpoint[2];
    static ap_uint<32>  out_index = 0;

    if (!prepare_start.empty()) {
        prepare_start.read();
        lState = PREPARING;
        oState = OS_DONE;
        out_index = 0;
        initialized = 0;
    }

    switch (lState) {
        case PREPARING:
            if (out_index == N_CAMPAIGNS && !prepare_done.full()) {
                out_index = 0;
                lState = RUNNING;
                prepare_done.write(1);
            } else {
                counts[0][out_index] = 0;
                counts[1][out_index] = 0;
                ++out_index;
            }
            break;
        case RUNNING:
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
            break;
    }
}
