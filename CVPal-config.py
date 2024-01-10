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
import serial

# csv file names
cfg_csv  = "Config_Params.csv"
midi_csv = "MIDI.csv"

# USB Device Names
midi_usb = "CVPal"
dmm_port = "/dev/tty.usbserial-110"

# Read Config file into Dictionary
with open(cfg_csv, 'r') as cfg_file:
    cfg_dict = DictReader(cfg_file)
    cfg_list = list(cfg_dict)

print(cfg_list)

# Read MIDI file into Dictionary
with open(midi_csv, 'r') as f:
    midi_csv_list = [[val.strip() for val in r.split(",")] for r in f.readlines()]

(_, *header), *data = midi_csv_list
midi_dict = {}
for row in data:
    key, *values = row   
    midi_dict[key] = {key: value for key, value in zip(header, values)}

print(midi_dict)

# connect meter
dmm = serial.Serial(
    port=dmm_port,
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

# connect cvpal

# loop through notes

# play note
# check voltage
# too high? send F1
# too low?  send G1
# just right? next note

# if prev step was one way and this step is other, see which was closer and stick with that one

# all done? close connections
