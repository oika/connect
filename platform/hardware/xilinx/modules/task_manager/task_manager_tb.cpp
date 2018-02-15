#include "connect_platform.hpp"

using namespace hls;

void task_manager(stream<ap_uint<CMD_WIDTH> >   &commandIn,
                  stream<nwif_ports>            &portsIn,
                  stream<ap_uint<CMD_WIDTH> >   &logicCommandOut,
                  stream<ap_uint<STATE_WIDTH> > &logicStateIn,
                  stream<ap_uint<16> >          &portRequestOut,
                  stream<bool>                  &portReplyIn,
                  stream<bool>                  &commandReplyOut)
{
#pragma HLS DATAFLOW
#pragma HLS INTERFACE ap_ctrl_none port=return

#pragma HLS INTERFACE axis register both port=commandIn
#pragma HLS INTERFACE axis register both port=portsIn
#pragma HLS INTERFACE axis register both port=logicCommandOut
#pragma HLS INTERFACE axis register both port=logicStateIn
#pragma HLS INTERFACE axis register both port=portRequestOut
#pragma HLS INTERFACE axis register both port=portReplyIn
#pragma HLS INTERFACE axis register both port=commandReplyOut

#pragma HLS DATA_PACK variable=portsIn

    static enum TmState {S_START = 0, S_WAIT_TM_PORT_OPEN, S_WAIT_COMMAND, S_READ_PORTS, S_WAIT_PORT_OPEN, S_WAIT_TRANSITION} state;
    static ap_uint<32> init_wait_time = 100;

    switch (state) {
        case S_START:
            if (init_wait_time == 0) {
                if (!portRequestOut.full()) {
                    portRequestOut.write(5440);
                    state = S_WAIT_TM_PORT_OPEN;
                }
            } else {
                --init_wait_time;
            }
            break;
        case S_WAIT_TM_PORT_OPEN:
            if (!portReplyIn.empty()) {
                if (portReplyIn.read()) {
                    state = S_WAIT_COMMAND;
                }
            }
            break;
        case S_WAIT_COMMAND:
            if (!commandIn.empty() && !logicCommandOut.full()) {
                ap_uint<32> cmd = commandIn.read();
                if (cmd == CMD_SUBMIT) {
                    state = S_READ_PORTS;
                } else {
                    state = S_WAIT_TRANSITION;
                }
                logicCommandOut.write(cmd);
            }
            break;
        case S_READ_PORTS:
            if (!portsIn.empty() && !portRequestOut.full()) {
                nwif_ports ports = portsIn.read();
                portRequestOut.write(ports.selfPort);
                state = S_WAIT_PORT_OPEN;
            }
            break;
        case S_WAIT_PORT_OPEN:
            if (!portReplyIn.empty() && !commandReplyOut.full()) {
                bool new_port_opened = portReplyIn.read();
                state = S_WAIT_TRANSITION;
            }
            break;
        case S_WAIT_TRANSITION:
            if (!logicStateIn.empty()) {
                ap_uint<32> logic_state;
                logic_state = logicStateIn.read();
                if (logic_state == S_PREPARING) {
                    ;
                } else if (logic_state == S_CANCELLING) {
                    ;
                } else {
                    state = S_WAIT_COMMAND;
                    commandReplyOut.write(true);
                }
            }
            break;
    }
}
