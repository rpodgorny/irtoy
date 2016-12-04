#!/bin/sh
set -e -x

# from http://dangerousprototypes.com/docs/USB_IR_Toy_firmware_update
wget http://jesshaas.com/software/IRToy-fw_update.tar.gz
tar xf IRToy-fw_update.tar.gz
cd IRToy-fw_update
env LIBS=-lusb ./configure
make

# then (v22 is the official latest stable):
#sudo ./IRToy-fw_update/fw_update -e -w -v -m all -vid 0x04D8 -pid 0xFD0B -ix USBIRToy.v22.hex
