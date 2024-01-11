#!/usr/bin/env python3

#https://pichenettes.github.io/mutable-instruments-diy-archive/cvpal/manual/

"""Calibration

Note: Yamaha and Roland have defined different schemes for numbering octaves – and since then nobody ever agreed on this! If, in the following procedures, everything appears to be off by one octave (the manual says something will happen with C4 but it happens with C3) or if measurements are off by +/-1V, don't panic – it is simply that your controller/DAW uses a different scheme for numbering octaves.

To ensure accurate note conversion, the CVpal needs to be manually calibrated. A digital multimeter with a precision of at least 3 digits is recommended for this task; but the calibration can also be done with an already calibrated synth or VCO module.

OUT 1 is calibrated by sending note messages to channel 15. OUT 2 is calibrated by sending note messages to channel 16.

Play a F#2 note (MIDI note 42). Check that the output voltage is 0.500V (or that the pitch of the emitted note on the synth/VCO is correct). If this is not the case, use F1 and G1 to make adjustments.
Play a C3 note (MIDI note 48). The target voltage is 1.000V. Use B1 or C#2 to make adjustments.
Play a F#3 note (MIDI note 54). The target voltage is 1.500V. Use F2 or G2 to make adjustments.
Play a C4 note (MIDI note 60). The target voltage is 2.000V. Use B3 or C#3 to make adjustments.
Play a F#4 note (MIDI note 66). The target voltage is 2.500V. Use F3 or G3 to make adjustments.
Play a C5 note (MIDI note 72). The target voltage is 3.000V. Use B3 or C#4 to make adjustments.
Play a F#5 note (MIDI note 78). The target voltage is 3.500V. Use F4 or G4 to make adjustments.
Play a C6 note (MIDI note 84). The target voltage is 4.000V. Use B4 or C#5 to make adjustments. The following chart summarizes this:

Technical note: to get maximum accuracy, it is recommended to temporarily connect a 100k resistor between the output being calibrated and ground. By doing so, the output protection resistor is taken into account. Not doing so might cause tuning errors of up to 10 cts at either ends of the scale.
"""
from csv import DictReader
import serial, time, platform

# For documentation on python-rtmidi: https://pypi.org/project/python-rtmidi/
import rtmidi

# csv file names
cfg_csv  = "Config_Params.csv"
midi_csv = "MIDI.csv"

# USB Device Names
midi_usb = "CVPal"
dmm_port = "/dev/tty.usbserial-110"

# MIDI Velocity values
vel_on = 100
vel_off = 0

# MIDI Channel number offset
midi_ch_offset = 0x90

# Read Config file into Dictionary
with open(cfg_csv, 'r') as cfg_file:
    cfg_dict = DictReader(cfg_file)
    cfg_list = list(cfg_dict)

# Read MIDI file into Dictionary
with open(midi_csv, 'r') as f:
    midi_csv_list = [[val.strip() for val in r.split(",")] for r in f.readlines()]

(_, *header), *data = midi_csv_list
midi_dict = {}
for row in data:
    key, *values = row   
    midi_dict[key] = {key: value for key, value in zip(header, values)}

# connect meter
try:
    dmm = serial.Serial(
        port=dmm_port,
        baudrate=115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS
    )
except:
    print("ERROR - failed to connect to DMM")
    exit(1)

# assuming DMM USB serial port was found, open it and get the DMM identity as confirmation
dmm.isOpen()

dmm_msg  = "*IDN?"
dmm_msg += '\n'
dmm.write(dmm_msg.encode())

dmm_resp = ''
# let's wait point one second before reading output (let's give device time to answer)
time.sleep(0.1)
while dmm.inWaiting() > 0:
    dmm_resp += dmm.read(1).decode()
            
if dmm_resp != '':
    print( "DMM Model " + dmm_resp )
else:
    print( "ERROR - DMM Failed to respond to request - exiting")
    exit(2)

# set measurement parameters
dmm_msg = "CONFigure:VOLTage:DC 50"
dmm_msg += '\n'
dmm.write(dmm_msg.encode())

# prepare volt read message
# set measurement parameters
dmm_msg = "MEAS1?"
dmm_msg += '\n'

# connect cvpal
# Initialize the MIDI output system and read the currently available ports.
midi_out = rtmidi.MidiOut()
for idx, name in enumerate(midi_out.get_ports()):
    if midi_usb in name:
        print("Found preferred MIDI output device %d: %s" % (idx, name))
        midi_out.open_port(idx)
        break
    else:
        print("Ignoring unselected MIDI device: ", name)

if not midi_out.is_port_open():
    print("ERROR - No MIDI device opened, exiting.")
    exit(1)

# loop through notes
for cfg_test in cfg_list:
    cv_channel     = cfg_test["CV Channel"]
    midi_channel   = cfg_test["MIDI Channel"]
    test_note      = cfg_test["Note"]
    tgt_volt       = float(cfg_test["CV Voltage"])
    decr_volt_note = cfg_test["Decr"]
    incr_volt_note = cfg_test["Incr"]

    test_note_midi = midi_dict[test_note]["MIDI note number"]
    decr_volt_midi = midi_dict[decr_volt_note]["MIDI note number"]
    incr_volt_midi = midi_dict[incr_volt_note]["MIDI note number"]
    
    print( "Test Note: " + test_note  + " (" + test_note_midi_val + ")")
    
    # set midi messages
    midi_channel += midi_ch_offset
    note_on  = [midi_channel, test_note_midi, vel_on] # note 36 is MPD218 pad 1 on bank A, with velocity 112
    note_off = [midi_channel, test_note_midi, vel_off]
    incr_on  = [midi_channel, incr_volt_midi, vel_on]
    decr_on  = [midi_channel, decr_volt_midi, vel_on]
    incr_off = [midi_channel, incr_volt_midi, vel_off]
    decr_off = [midi_channel, decr_volt_midi, vel_off]

    # play note
    midi_out.send_message(note_on)

    # loop through incr/decr until correct
    cv_volt = 99
    while cv_volt != tgt_volt:
        time.sleep(1.0) # settle time

        # check voltage
        volt_msg = ''
        while dmm.inWaiting() > 0:
            volt_msg += dmm.read(1).decode()

        print( "Voltage read" + volt_msg )

        #convert text to number
        cv_volt = float(volt_msg)

        # too high? send F1
        if cv_volt > tgt_volt:
            print( "Decr")
            # play note
            midi_out.send_message(decr_on)
            time.sleep(0.1)
            midi_out.send_message(decr_off)       

        # too low?  send G1
        if cv_volt < tgt_volt:
            print("Incr")
            # play note
            midi_out.send_message(decr_on)
            time.sleep(0.1)
            midi_out.send_message(decr_off)

    # just right? next note

    # if prev step was one way and this step is other, see which was closer and stick with that one
    # stop note
    print("Note Done")
    midi_out.send_message(note_off)


# all done? close connections
