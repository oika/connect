#include <hls_stream.h>
#include "ap_int.h"
#include "connect_platform.hpp"

void TaskManager(hls::stream<ap_uint<CMD_WIDTH> >   &commandIn,
                 hls::stream<nwif_ports>            &portsIn,
                 hls::stream<ap_uint<CMD_WIDTH> >   &logicCommandOut,
                 hls::stream<ap_uint<STATE_WIDTH> > &logicStateIn,
                 hls::stream<ap_uint<16> >          &portRequestOut,
                 hls::stream<bool>                  &portReplyIn,
                 hls::stream<bool>                  &commandReplyOut);
