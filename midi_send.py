#!/usr/bin/env python3
"""Example script to transmit a sequence of MIDI messages over time.  Runs from
the command line, no GUI.  Uses the rtmidi package for output.
"""
################################################################
# Written in 2018-2021 by Garth Zeglin <garthz@cmu.edu>

# To the extent possible under law, the author has dedicated all copyright
# and related and neighboring rights to this software to the public domain
# worldwide. This software is distributed without any warranty.

# You should have received a copy of the CC0 Public Domain Dedication along with this software.
# If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.

################################################################
# Standard Python libraries.
import argparse, time, platform

# For documentation on python-rtmidi: https://pypi.org/project/python-rtmidi/
import rtmidi

################################################################
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""Demonstration of sending a timed sequence of MIDI messages.""")
    parser.add_argument( '-v', '--verbose', action='store_true', help='Enable more detailed output.' )
    parser.add_argument("--midi", type=str, default = "virtual MPD218", help = "Keyword identifying the MIDI output device (default: %(default)s).")
    args = parser.parse_args()

    # Initialize the MIDI output system and read the currently available ports.
    midi_out = rtmidi.MidiOut()
    for idx, name in enumerate(midi_out.get_ports()):
        if args.midi in name:
            print("Found preferred MIDI output device %d: %s" % (idx, name))
            midi_out.open_port(idx)
            break
        else:
            print("Ignoring unselected MIDI device: ", name)

    if not midi_out.is_port_open():
        if platform.system() == 'Windows':
            print("Virtual MIDI outputs are not currently supported on Windows, see python-rtmidi documentation.")
        else:
            print("Creating virtual MIDI output.")
            midi_out.open_virtual_port(args.midi)
    
    if not midi_out.is_port_open():
        print("No MIDI device opened, exiting.")
        exit(1)
        
    if args.verbose:
        print(f"Starting message sequence.")        

    chan = 9                          # MIDI channel 10 similar to the MPD218
    note_on  = [0x90 + chan, 36, 112] # note 36 is MPD218 pad 1 on bank A, with velocity 112
    note_off = [0x80 + chan, 36, 0]

    for i in range(10):
        midi_out.send_message(note_on)
        time.sleep(1.0)
        midi_out.send_message(note_off)
        time.sleep(0.25)
        
    if args.verbose:
        print(f"Sequence done.")

