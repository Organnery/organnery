from mididings import *

# enable/disable a stop
# group: 0=top row, 3=bottom row, ...
# stop:  0=first, 1=second, ...
# state: True=enable, False=disable
def aeolus_stop(group, stop, state):
	if state:
		return [ Ctrl(98, 0x60 | group), Ctrl(98, stop) ]
	else:
		return [ Ctrl(98, 0x50 | group), Ctrl(98, stop) ]


# transpose the cresendo value > preset value
def transpose_cresendo_value(ev):
	ev.program = ev.program - 89
	return ev


run(
	[
		# orginal examples
		#Filter(NOTEON) >> KeyFilter(30) >> System("./jamesbond.sh"),
		#Filter(NOTEON) >> KeyFilter(31) >> System("./children.sh"),
		#Filter(NOTEON) >> KeyFilter(32) >> System("./minimax.sh"),

		# Grand Orgue note on/off
		ChannelFilter(2) >> Filter(NOTEON, NOTEOFF) >> Channel(2),

		# Recit note on/off
		ChannelFilter(1) >> Filter(NOTEON, NOTEOFF) >> Channel(3),

		# Pedal note on/off
		ChannelFilter(4) >> Filter(NOTEON, NOTEOFF) >> Channel(1),

		# Tutti enable
		ChannelFilter(16) >> CtrlFilter(0x47) >> CtrlValueFilter(0x42) >> Channel(1) >> Ctrl(29, 10),

		# Tutti disable
		ChannelFilter(16) >> CtrlFilter(0x47) >> CtrlValueFilter(0x02) >> Channel(1) >> Ctrl(29, 11),

		# P.A.
		# todo: unknown

		# Cancel
		ChannelFilter(16) >> CtrlFilter(0x47) >> CtrlValueFilter(0x00) >> Channel(1) >> Ctrl(28, 10),

		# Presets
		ChannelFilter(16) >> ProgramFilter(1, 2, 3, 4, 5, 6, 7, 8, 9, 10) >> Channel(1) >> Ctrl(33, EVENT_PROGRAM),

		# I-P enable
		ChannelFilter(3) >> CtrlFilter(46) >> CtrlValueFilter(0x4d) >> Channel(1) >> aeolus_stop(3, 13, True),

		# I-P disable
		ChannelFilter(3) >> CtrlFilter(46) >> CtrlValueFilter(0x0d) >> Channel(1) >> aeolus_stop(3, 13, False),

		# II-P enable
		ChannelFilter(3) >> CtrlFilter(46) >> CtrlValueFilter(0x4e) >> Channel(1) >> aeolus_stop(3, 14, True),

		# II-P disable
		ChannelFilter(3) >> CtrlFilter(46) >> CtrlValueFilter(0x0e) >> Channel(1) >> aeolus_stop(3, 14, False),

		# II-I enable
		ChannelFilter(3) >> CtrlFilter(46) >> CtrlValueFilter(0x4e) >> Channel(1) >> aeolus_stop(2, 14, True),

		# II-I disable
		ChannelFilter(3) >> CtrlFilter(46) >> CtrlValueFilter(0x0e) >> Channel(1) >> aeolus_stop(2, 14, False),

		# EXP Pedal (swell for ManI and ManII)
		ChannelFilter(1) >> CtrlFilter(0x07) >> [ Channel(1), Channel(2) ],

		# Cresendo Pedal
		ChannelFilter(16) >> ProgramFilter(0x64, 0x65, 0x66, 0x67, 0x68, 0x69, 0x6a, 0x6b, 0x6c, 0x6d) >> Channel(1) >> Process(transpose_cresendo_value) >> Ctrl(33, EVENT_PROGRAM),

		# Grand orgue Volume
		ChannelFilter(2) >> CtrlFilter(0x07) >> Channel(2) >> Ctrl(16, EVENT_VALUE),

		# Pedal Volume
		ChannelFilter(4) >> CtrlFilter(0x07) >> Channel(1) >> Ctrl(16, EVENT_VALUE),
	]
)