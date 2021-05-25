from mididings import *

config(
	in_ports = [
		'from_hw',
		'from_aeolus',],
	out_ports = [
		'to_aeolus',
		'to_hw',],
)
# simple script to passthru midi from input to output
run(Pass())