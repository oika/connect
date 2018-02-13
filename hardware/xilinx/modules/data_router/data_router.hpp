#include <hls_stream.h>
#include "ap_int.h"
#include "connect_platform.hpp"

void data_router(hls::stream<axiWord>               &rxDataIn,
                 hls::stream<metadata>              &rxMetadataIn,
                 hls::stream<axiWord>               &rxDataOut,
                 hls::stream<axiWord>               &txDataIn,
                 hls::stream<axiWord>               &txDataOut,
                 hls::stream<metadata>              &txMetadataOut,
                 hls::stream<ap_uint<16> >          &txLengthOut,
                 hls::stream<ap_uint<CMD_WIDTH> >   &commandOut,
                 hls::stream<nwif_ports>            &portsOut,
                 hls::stream<bool>                  &commandReplyIn);
