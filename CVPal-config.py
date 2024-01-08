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
# read in midi notes

from csv import DictReader
# open file in read mode
with open("midi.csv", 'r') as f:
     
    dict_reader = DictReader(f)
     
    list_of_dict = list(dict_reader)
   
    print(list_of_dict)

# connect meter

# connect cvpal

# loop through notes

# play note
# check voltage
# too high? send F1
# too low?  send G1
# just right? next note

# if prev step was one way and this step is other, see which was closer and stick with that one

# all done? close connections
