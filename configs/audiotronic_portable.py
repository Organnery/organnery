# Filter for Audiotronic Custom portable console
# to aeolus default organ "Aeolus"

from mididings import *

# enable/disable a stop
# group: 0=top row, 3=bottom row, ...
# stop:  0=first, 1=second, ...
# state: True=enable, False=disable
def aeolus_stop(group, stop, state):
	if state:
		return [ Ctrl(EVENT_PORT, 1, 98, 0x60 | group), Ctrl(EVENT_PORT, 1, 98, stop) ]
	else:
		return [ Ctrl(EVENT_PORT, 1, 98, 0x50 | group), Ctrl(EVENT_PORT, 1, 98, stop) ]

# transpose the cresendo value > preset value
def transpose_cresendo_value(ev):
	if ev.value < 19:
		ev.value = 0
	elif ev.value < 37:
		ev.value = 1
	elif ev.value < 55:
		ev.value = 2
	elif ev.value < 73:
		ev.value = 3
	elif ev.value < 91:
		ev.value = 4
	elif ev.value < 109:
		ev.value = 5
	return ev

run(
	[
		#-------------------------------------------
		#		KEYBOARDS
		#-------------------------------------------

		# Grand Orgue note on/off
		ChannelFilter(1) >> Filter(NOTEON, NOTEOFF) >> Channel(1),

		# Recit note on/off
		ChannelFilter(2) >> Filter(NOTEON, NOTEOFF) >> Channel(2),

		# Pedal note on/off
		ChannelFilter(4) >> Filter(NOTEON, NOTEOFF) >> Channel(4),

		#-------------------------------------------
		#		SPECIAL FUNCTIONS
		#-------------------------------------------

		# Tutti enable/disable
		ChannelFilter(3) >> KeyFilter(0x35) >> Filter(NOTEON) >> Channel(1) >> Ctrl(29, 10),
		#ChannelFilter(3) >> KeyFilter(0x35) >> Channel(1) >> Ctrl(29, 11),

		# Cancel
		ChannelFilter(3) >> KeyFilter(0x34) >> Channel(1) >> Ctrl(28, 10),

		# Transpose -2/0/+3
		ChannelFilter(3) >> KeyFilter(0x2F) >> Channel(1) >> Ctrl(30, 62),
		ChannelFilter(3) >> KeyFilter(0x30) >> Channel(1) >> Ctrl(30, 63),
		ChannelFilter(3) >> KeyFilter(0x31) >> Channel(1) >> Ctrl(30, 64),
		ChannelFilter(3) >> KeyFilter(0x32) >> Channel(1) >> Ctrl(30, 65),
		ChannelFilter(3) >> KeyFilter(0x33) >> Channel(1) >> Ctrl(30, 66),
		ChannelFilter(3) >> KeyFilter(0x2B) >> Channel(1) >> Ctrl(30, 67),

		#-------------------------------------------
		#		PRESETS
		#-------------------------------------------

		# Bank Select
		ChannelFilter(3) >> KeyFilter(0x2A) >> Channel(1) >> Ctrl(32, 0),
		ChannelFilter(3) >> KeyFilter(0x29) >> Channel(1) >> Ctrl(32, 1),
		ChannelFilter(3) >> KeyFilter(0x28) >> Channel(1) >> Ctrl(32, 2),
		ChannelFilter(3) >> KeyFilter(0x27) >> Channel(1) >> Ctrl(32, 3),
		ChannelFilter(3) >> KeyFilter(0x26) >> Channel(1) >> Ctrl(32, 4),
		ChannelFilter(3) >> KeyFilter(0x25) >> Channel(1) >> Ctrl(32, 5),

		# Preset Select
		ChannelFilter(3) >> KeyFilter(0x3B) >> Channel(1) >> Ctrl(33, 0),
		ChannelFilter(3) >> KeyFilter(0x3A) >> Channel(1) >> Ctrl(33, 1),
		ChannelFilter(3) >> KeyFilter(0x39) >> Channel(1) >> Ctrl(33, 2),
		ChannelFilter(3) >> KeyFilter(0x38) >> Channel(1) >> Ctrl(33, 3),
		ChannelFilter(3) >> KeyFilter(0x37) >> Channel(1) >> Ctrl(33, 4),
		ChannelFilter(3) >> KeyFilter(0x36) >> Channel(1) >> Ctrl(33, 5),

		#-------------------------------------------
		#		COUPLERS
		#-------------------------------------------

		# I-P enable/disable
		#ChannelFilter(3) >> KeyFilter(0x2E) >> Filter(NOTEON)  >> Channel(1) >> aeolus_stop(3, 13, True),
		#ChannelFilter(3) >> KeyFilter(0x2E) >> Filter(NOTEOFF) >> Channel(1) >> aeolus_stop(3, 13, False),

		# II-P enable/disable
		#ChannelFilter(4) >> CtrlFilter(0x46) >> CtrlValueFilter(0x4e) >> aeolus_stop(3, 14, True),
		#ChannelFilter(4) >> CtrlFilter(0x46) >> CtrlValueFilter(0x0e) >> aeolus_stop(3, 14, False),

		# II-I enable/disable
		ChannelFilter(3) >> KeyFilter(0x2E) >> Filter(NOTEON)  >> Channel(1) >> aeolus_stop(2, 14, True),
		ChannelFilter(3) >> KeyFilter(0x2E) >> Filter(NOTEOFF) >> Channel(1) >> aeolus_stop(2, 14, False),

		# III-I enable/disable
		ChannelFilter(3) >> KeyFilter(0x2D) >> Filter(NOTEON)  >> Channel(1) >> aeolus_stop(2, 15, True),
		ChannelFilter(3) >> KeyFilter(0x2D) >> Filter(NOTEOFF) >> Channel(1) >> aeolus_stop(2, 15, False),

		# III-II enable/disable
		ChannelFilter(3) >> KeyFilter(0x2C) >> Filter(NOTEON)  >> Channel(1) >> aeolus_stop(1, 12, True),
		ChannelFilter(3) >> KeyFilter(0x2C) >> Filter(NOTEOFF) >> Channel(1) >> aeolus_stop(1, 12, False),

		#-------------------------------------------
		#		EXPRESSION PEDALS
		#-------------------------------------------

		# EXP Pedal (swell for ManI and ManII)
		# ChannelFilter(1) >> CtrlFilter(0x07) >> [ Channel(1), Channel(2) ], # maps to Ch1 & Ch2 swell sliders
		# ChannelFilter(16) >> CtrlFilter(0x07) >> Ctrl(16, EVENT_VALUE) >> [ Channel(1), Channel(2) ], # maps to Ch1 & Ch2 direct sliders
		# ChannelFilter(16) >> CtrlFilter(0x07) >> Channel(1) >> Ctrl(23, EVENT_VALUE), # maps to master volume slider

		# Cresendo Pedal
		#ChannelFilter(16) >> ProgramFilter(0x64, 0x65, 0x66, 0x67, 0x68, 0x69, 0x6a, 0x6b, 0x6c, 0x6d) >> Channel(1) >> Process(transpose_cresendo_value) >> Ctrl(33, EVENT_PROGRAM),

		# Grand orgue Volume
		#ChannelFilter(2) >> CtrlFilter(0x07) >> Channel(2) >> Ctrl(16, EVENT_VALUE),

		# -------		

		# Pedal Volume to Swell Man II
		ChannelFilter(4) >> CtrlFilter(0x07) >> Channel(2) >> Ctrl(7, EVENT_VALUE),

		# Pedal Volume to Swell Man II
		#ChannelFilter(4) >> CtrlFilter(0x07) >> Channel(3) >> Ctrl(7, EVENT_VALUE),

		# Pedal Volume as crescendo (6 presets in the bank)
		#ChannelFilter(4) >> CtrlFilter(0x07) >> Channel(1) >> Process(transpose_cresendo_value) >> Ctrl(33, EVENT_VALUE),

		#-------------------------------------------
		#		STOPS
		#-------------------------------------------

		ChannelFilter(5) >> [
		# STOPS GRAND ORGUE
			# 1 Montro 8 to Principal 8'
			KeyFilter(0x2D) >> Filter(NOTEON) >> aeolus_stop(2, 0, True),
			KeyFilter(0x2D) >> Filter(NOTEOFF) >> aeolus_stop(2, 0, False),

			# 2 Doublette 2 to Principal 4'
			KeyFilter(0x2C) >> Filter(NOTEON) >> aeolus_stop(2, 1, True),
			KeyFilter(0x2C) >> Filter(NOTEOFF) >> aeolus_stop(2, 1, False),

			# 3 Cymbale 3R to Octave 2'
			KeyFilter(0x2B) >> Filter(NOTEON) >> aeolus_stop(2, 2, True),
			KeyFilter(0x2B) >> Filter(NOTEOFF) >> aeolus_stop(2, 2, False),

			# 4 Unda Maris 8 to Octave 1'
			KeyFilter(0x2A) >> Filter(NOTEON) >> aeolus_stop(2, 3, True),
			KeyFilter(0x2A) >> Filter(NOTEOFF) >> aeolus_stop(2, 3, False),

			# 5 Bordon 16 to Quint 5'1/3
			KeyFilter(0x29) >> Filter(NOTEON) >> aeolus_stop(2, 4, True),
			KeyFilter(0x29) >> Filter(NOTEOFF) >> aeolus_stop(2, 4, False),

			# 6 Prestant 4 to Quint 2'2/3
			KeyFilter(0x28) >> Filter(NOTEON) >> aeolus_stop(2, 5, True),
			KeyFilter(0x28) >> Filter(NOTEOFF) >> aeolus_stop(2, 5, False),

			# 7 Plein-Jeux 2R to Flote 4'
			KeyFilter(0x27) >> Filter(NOTEON) >> aeolus_stop(2, 9, True),
			KeyFilter(0x27) >> Filter(NOTEOFF) >> aeolus_stop(2, 9, False),

			# 8 Sesqui-Altera 2R to Flote 2'
			KeyFilter(0x26) >> Filter(NOTEON) >> aeolus_stop(2, 10, True),
			KeyFilter(0x26) >> Filter(NOTEOFF) >> aeolus_stop(2, 10, False),

			# 7 Plein-Jeux 2R to Flote 4'
			KeyFilter(0x25) >> Filter(NOTEON) >> aeolus_stop(2, 11, True),
			KeyFilter(0x25) >> Filter(NOTEOFF) >> aeolus_stop(2, 11, False),

			# 8 Sesqui-Altera 2R to Flote 2'
			KeyFilter(0x24) >> Filter(NOTEON) >> aeolus_stop(2, 12, True),
			KeyFilter(0x24) >> Filter(NOTEOFF) >> aeolus_stop(2, 12, False),

		# STOPS RECIT

			# 14 Contre-basse 16 to Principal 16
			KeyFilter(0x3B) >> Filter(NOTEON) >> aeolus_stop(1, 1, True),
			KeyFilter(0x3B) >> Filter(NOTEOFF) >> aeolus_stop(1, 1, False),

			# 15 Basse 8 to Principal 8
			KeyFilter(0x33) >> Filter(NOTEON) >> aeolus_stop(1, 2, True),
			KeyFilter(0x33) >> Filter(NOTEOFF) >> aeolus_stop(1, 2, False),

			# 16 Octave 4 to Principal 4
			KeyFilter(0x32) >> Filter(NOTEON) >> aeolus_stop(1, 3, True),
			KeyFilter(0x32) >> Filter(NOTEOFF) >> aeolus_stop(1, 3, False),

			# 17 Forniture 4R to Octave 2
			KeyFilter(0x31) >> Filter(NOTEON) >> aeolus_stop(1, 4, True),
			KeyFilter(0x31) >> Filter(NOTEOFF) >> aeolus_stop(1, 4, False),

			# 18 Tirasse I-PED to P+I
			KeyFilter(0x30) >> Filter(NOTEON) >> aeolus_stop(1, 5, True),
			KeyFilter(0x30) >> Filter(NOTEOFF) >> aeolus_stop(1, 5, False),

			# 17 Forniture 4R to Octave 2
			KeyFilter(0x2F) >> Filter(NOTEON) >> aeolus_stop(1, 6, True),
			KeyFilter(0x2F) >> Filter(NOTEOFF) >> aeolus_stop(1, 6, False),

			# 18 Tirasse I-PED to P+I
			KeyFilter(0x2E) >> Filter(NOTEON) >> aeolus_stop(1, 7, True),
			KeyFilter(0x2E) >> Filter(NOTEOFF) >> aeolus_stop(1, 7, False),

		# STOPS PEDAL

			# 20 Soubasse 16 to Subbass 16
			KeyFilter(0x34) >> Filter(NOTEON) >> aeolus_stop(3, 0, True),
			KeyFilter(0x34) >> Filter(NOTEOFF) >> aeolus_stop(3, 0, False),

			# 21 Bordon 8 to Trombone 16
			KeyFilter(0x35) >> Filter(NOTEON) >> aeolus_stop(3, 1, True),
			KeyFilter(0x35) >> Filter(NOTEOFF) >> aeolus_stop(3, 1, False),

			# 22 Flute ouvert 4 to Octave 1
			KeyFilter(0x36) >> Filter(NOTEON) >> aeolus_stop(3, 2, True),
			KeyFilter(0x36) >> Filter(NOTEOFF) >> aeolus_stop(3, 2, False),

			# 23 Bombarde 16 to Bombarde 32
			KeyFilter(0x37) >> Filter(NOTEON) >> aeolus_stop(3, 3, True),
			KeyFilter(0x37) >> Filter(NOTEOFF) >> aeolus_stop(3, 3, False),

			# 24 Trompette 8 to Trumpet
			KeyFilter(0x38) >> Filter(NOTEON) >> aeolus_stop(3, 4, True),
			KeyFilter(0x38) >> Filter(NOTEOFF) >> aeolus_stop(3, 4, False),

			# 25 Clairon 4 to Mixtur
			KeyFilter(0x39) >> Filter(NOTEON) >> aeolus_stop(3, 5, True),
			KeyFilter(0x39) >> Filter(NOTEOFF) >> aeolus_stop(3, 5, False),

			# 26 Principal 4 to Rohrflote 8
			KeyFilter(0x3A) >> Filter(NOTEON) >> aeolus_stop(3, 6, True),
			KeyFilter(0x3A) >> Filter(NOTEOFF) >> aeolus_stop(3, 6, False),
		]
	]
)
