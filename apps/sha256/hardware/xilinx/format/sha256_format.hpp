#include <stdio.h>
#include "connect_platform.hpp"
#include "ap_int.h"
#include "hls_stream.h"

using namespace hls;

void sha256_format(stream<axiWord>          &rxDataIn,
                   stream<ap_uint<1024> >   &rxEventOut,
                   stream<ap_uint<32> >     &txEventIn,
                   stream<axiWord>          &txDataOut);
