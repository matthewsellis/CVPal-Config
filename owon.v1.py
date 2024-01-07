#!/usr/bin/env python3

#        USB Serial:
#
#          Product ID: 0x7523
#          Vendor ID: 0x1a86
#          Version: 81.32
#          Speed: Up to 12 Mb/s
#          Location ID: 0x01100000 / 1
#          Current Available (mA): 500
#          Current Required (mA): 100
#          Extra Operating Current (mA): 0


from pyscpi import usbtmc

# use 'system_profiler SPUSBDataType' to list usb devices
# inst =  usbtmc.Instrument(<VendorID>, <ProductID>)
inst =  usbtmc.Instrument(0x1A86, 0x7523)
# "USB::0x1a86:0x7523::INSTR"

#inst =  usbtmc.Instrument("USB::0x1a86:0x7523::INSTR")

print(inst.query("*IDN?"))
