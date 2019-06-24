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
	ev.program = ev.program - 89
	return ev


run(
	[
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
		ChannelFilter(4) >> CtrlFilter(46) >> CtrlValueFilter(0x4d) >> aeolus_stop(3, 13, True),

		# I-P disable
		ChannelFilter(4) >> CtrlFilter(46) >> CtrlValueFilter(0x0d) >> aeolus_stop(3, 13, False),

		# II-P enable
		ChannelFilter(4) >> CtrlFilter(46) >> CtrlValueFilter(0x4e) >> aeolus_stop(3, 14, True),

		# II-P disable
		ChannelFilter(4) >> CtrlFilter(46) >> CtrlValueFilter(0x0e) >> aeolus_stop(3, 14, False),

		# II-I enable
		ChannelFilter(4) >> CtrlFilter(46) >> CtrlValueFilter(0x4e) >> aeolus_stop(2, 14, True),

		# II-I disable
		ChannelFilter(4) >> CtrlFilter(46) >> CtrlValueFilter(0x0e) >> aeolus_stop(2, 14, False),

		# EXP Pedal (swell for ManI and ManII)
		# todo: channel not specified in spreadsheet
		ChannelFilter(16) >> CtrlFilter(0x07) >> [ Channel(1), Channel(2) ], # maps to Ch1 & Ch2 swell sliders
		# ChannelFilter(16) >> CtrlFilter(0x07) >> Ctrl(16, EVENT_VALUE) >> [ Channel(1), Channel(2) ], # maps to Ch1 & Ch2 direct sliders
		# ChannelFilter(16) >> CtrlFilter(0x07) >> Channel(1) >> Ctrl(23, EVENT_VALUE), # maps to master volume slider

		# Cresendo Pedal
		ChannelFilter(16) >> ProgramFilter(0x64, 0x65, 0x66, 0x67, 0x68, 0x69, 0x6a, 0x6b, 0x6c, 0x6d) >> Channel(1) >> Process(transpose_cresendo_value) >> Ctrl(33, EVENT_PROGRAM),

		# Grand orgue Volume
		ChannelFilter(2) >> CtrlFilter(0x07) >> Channel(2) >> Ctrl(16, EVENT_VALUE),

		# Pedal Volume
		ChannelFilter(4) >> CtrlFilter(0x07) >> Channel(1) >> Ctrl(16, EVENT_VALUE),

		# STOPS
		CtrlFilter(0x46) >> [

			# STOPS GRAND ORGUE
			ChannelFilter(2) >> [
				# 1 Montro 8 to Principal 8' & Tibia 8'
				CtrlValueFilter(0x43) >> [
					aeolus_stop(2, 0, True),
					aeolus_stop(2, 6, True),
				],
				CtrlValueFilter(0x03) >> [
					aeolus_stop(2, 0, False),
					aeolus_stop(2, 6, False),
				],

				# 2 Doublette 2 to Principal 4' & Celesta 8'
				CtrlValueFilter(0x45) >> [
					aeolus_stop(2, 1, True),
					aeolus_stop(2, 7, True),
				],
				CtrlValueFilter(0x05) >> [
					aeolus_stop(2, 1, False),
					aeolus_stop(2, 7, False),
				],

				# 3 Cymbale 3R to Octave 2'
				CtrlValueFilter(0x48) >> aeolus_stop(2, 2, True),
				CtrlValueFilter(0x08) >> aeolus_stop(2, 2, False),

				# 4 Unda Maris 8 to Octave 1'
				CtrlValueFilter(0x4b) >> aeolus_stop(2, 3, True),
				CtrlValueFilter(0x0b) >> aeolus_stop(2, 3, False),

				# 5 Bordon 16 to Quint 5'1/3
				CtrlValueFilter(0x42) >> aeolus_stop(2, 4, True),
				CtrlValueFilter(0x02) >> aeolus_stop(2, 4, False),

				# 6 Prestant 4 to Quint 2'2/3
				CtrlValueFilter(0x44) >> aeolus_stop(2, 5, True),
				CtrlValueFilter(0x04) >> aeolus_stop(2, 5, False),

				# 7 Plein-Jeux 2R to Flote 4'
				CtrlValueFilter(0x49) >> aeolus_stop(2, 9, True),
				CtrlValueFilter(0x09) >> aeolus_stop(2, 9, False),

				# 8 Sesqui-Altera 2R to Flote 2'
				CtrlValueFilter(0x4a) >> aeolus_stop(2, 10, True),
				CtrlValueFilter(0x0a) >> aeolus_stop(2, 10, False),

				# 9 ACC. II-I to I+II & I+III
				CtrlValueFilter(0x50) >> [
					aeolus_stop(2, 15, True),
					aeolus_stop(2, 16, True),
				],
				CtrlValueFilter(0x10) >> [
					aeolus_stop(2, 15, False),
					aeolus_stop(2, 16, False),
				],

				# 10 Flute 8 to Flote 8'
				CtrlValueFilter(0x40) >> aeolus_stop(2, 8, True),
				CtrlValueFilter(0x00) >> aeolus_stop(2, 8, False),

				# 11 Flute a fuseau to Cymbel VI
				CtrlValueFilter(0x41) >> aeolus_stop(2, 11, True),
				CtrlValueFilter(0x01) >> aeolus_stop(2, 11, False),

				# 12 Trompette 8 to Trumpet
				CtrlValueFilter(0x4d) >> aeolus_stop(2, 13, True),
				CtrlValueFilter(0x0d) >> aeolus_stop(2, 13, False),

				# 13 Cromorne 8 to Mixtur
				CtrlValueFilter(0x4e) >> aeolus_stop(2, 12, True),
				CtrlValueFilter(0x0e) >> aeolus_stop(2, 12, False),
			],

			# STOPS PEDAL
			ChannelFilter(4) >> [
				# 14 Contre-basse 16 to Principal 16
				CtrlValueFilter(0x41) >> aeolus_stop(3, 1, True),
				CtrlValueFilter(0x01) >> aeolus_stop(3, 1, False),

				# 15 Basse 8 to Principal 8
				CtrlValueFilter(0x43) >> aeolus_stop(3, 2, True),
				CtrlValueFilter(0x03) >> aeolus_stop(3, 2, False),

				# 16 Octave 4 to Principal 4
				CtrlValueFilter(0x45) >> aeolus_stop(3, 3, True),
				CtrlValueFilter(0x05) >> aeolus_stop(3, 3, False),

				# 17 Forniture 4R to Octave 2
				CtrlValueFilter(0x48) >> aeolus_stop(3, 4, True),
				CtrlValueFilter(0x08) >> aeolus_stop(3, 4, False),

				# 18 Tirasse I-PED to P+I
				CtrlValueFilter(0x4d) >> aeolus_stop(3, 13, True),
				CtrlValueFilter(0x0d) >> aeolus_stop(3, 13, False),

				# 19 Tirasse II-PED to P+II & P+III & Quint 5 1/3
				CtrlValueFilter(0x4e) >> [
					aeolus_stop(3, 14, True),
					aeolus_stop(3, 15, True),
					aeolus_stop(2, 4, True),
				],
				CtrlValueFilter(0x0e) >> [
					aeolus_stop(3, 14, False),
					aeolus_stop(3, 15, False),
					aeolus_stop(2, 4, False),
				],

				# 20 Soubasse 16 to Subbass 16 & Quint 2 2/3
				CtrlValueFilter(0x42) >> [
					aeolus_stop(3, 0, True),
					aeolus_stop(3, 7, True),
				],
				CtrlValueFilter(0x02) >> [
					aeolus_stop(3, 0, False),
					aeolus_stop(3, 7, False),
				],

				# 21 Bordon 8 to Trombone 16 & Fagott 16
				CtrlValueFilter(0x44) >> [
					aeolus_stop(3, 10, True),
					aeolus_stop(3, 9, True),
				],
				CtrlValueFilter(0x04) >> [
					aeolus_stop(3, 10, False),
					aeolus_stop(3, 9, False),
				],

				# 22 Flute ouvert 4 to Octave 1
				CtrlValueFilter(0x46) >> aeolus_stop(3, 5, True),
				CtrlValueFilter(0x06) >> aeolus_stop(3, 5, False),

				# 23 Bombarde 16 to Bombarde 32
				CtrlValueFilter(0x4a) >> aeolus_stop(3, 11, True),
				CtrlValueFilter(0x0a) >> aeolus_stop(3, 11, False),

				# 24 Trompette 8 to Trumpet
				CtrlValueFilter(0x4b) >> aeolus_stop(3, 12, True),
				CtrlValueFilter(0x0b) >> aeolus_stop(3, 12, False),

				# 25 Clairon 4 to Mixtur
				CtrlValueFilter(0x4c) >> aeolus_stop(3, 8, True),
				CtrlValueFilter(0x0c) >> aeolus_stop(3, 8, False),

			],

			# STOPS Recit
			ChannelFilter(1) >> [
				# 26 Principal 4 to Rohrflote 8
				CtrlValueFilter(0x45) >> aeolus_stop(1, 0, True),
				CtrlValueFilter(0x05) >> aeolus_stop(1, 0, False),

				# 27 Quinte 1-1/3 to Harmonic Flute 8'
				CtrlValueFilter(0x47) >> aeolus_stop(1, 1, True),
				CtrlValueFilter(0x07) >> aeolus_stop(1, 1, False),

				# 28 Cymbale 3R to Flauto dolce 4'
				CtrlValueFilter(0x4c) >> aeolus_stop(1, 2, True),
				CtrlValueFilter(0x0c) >> aeolus_stop(1, 2, False),

				# 30 Bordon 8 to Nasard 2'2/3
				CtrlValueFilter(0x41) >> aeolus_stop(1, 3, True),
				CtrlValueFilter(0x01) >> aeolus_stop(1, 3, False),

				# 31 Cor de nuit 4 to Ottavina 2'
				CtrlValueFilter(0x42) >> aeolus_stop(1, 4, True),
				CtrlValueFilter(0x02) >> aeolus_stop(1, 4, False),

				# 32 Nasard 2-2/3 to Tertia 1'3/5 & Sesqui-altera
				CtrlValueFilter(0x48) >> [
					aeolus_stop(1, 5, True),
					aeolus_stop(1, 6, True),
				],
				CtrlValueFilter(0x08) >> [
					aeolus_stop(1, 5, False),
					aeolus_stop(1, 6, False),
				],

				# 33 Flute 2 to Septime & Super octave 2'
				CtrlValueFilter(0x44) >> [
					aeolus_stop(1, 7, True),
					aeolus_stop(0, 7, True),
				],
				CtrlValueFilter(0x04) >> [
					aeolus_stop(1, 7, False),
					aeolus_stop(0, 7, False),
				],

				# 34 Tierce 1-3/5 to Principal 8' & Sifflet 1'
				CtrlValueFilter(0x49) >> [
					aeolus_stop(3, 2, True),
					aeolus_stop(0, 8, True),
				],
				CtrlValueFilter(0x09) >> [
					aeolus_stop(3, 2, False),
					aeolus_stop(0, 8, False),
				],

				# 35 Gambe 8 to Gemshorn 8' & Krumhorn & Cymbel VI
				CtrlValueFilter(0x4a) >> [
					aeolus_stop(0, 1, True),
					aeolus_stop(1, 9, True),
					aeolus_stop(2, 11, True),
				],
				CtrlValueFilter(0x0a) >> [
					aeolus_stop(0, 1, False),
					aeolus_stop(1, 9, False),
					aeolus_stop(2, 11, False),
				],

				# 36 Voix celeste 8 to Quinta-dena 8' & Melodia & Oboe
				CtrlValueFilter(0x4b) >> [
					aeolus_stop(0, 2, True),
					aeolus_stop(1, 10, True),
					aeolus_stop(0, 10, True),
				],
				CtrlValueFilter(0x0b) >> [
					aeolus_stop(0, 2, False),
					aeolus_stop(1, 10, False),
					aeolus_stop(0, 10, False),
				],

				# 37 Regale 16 to Suabile 8'
				CtrlValueFilter(0x4e) >> aeolus_stop(0, 3, True),
				CtrlValueFilter(0x0e) >> aeolus_stop(0, 3, False),

				# 38 Hautbois 8 to Rohrflote 4
				CtrlValueFilter(0x51) >> aeolus_stop(0, 4, True),
				CtrlValueFilter(0x11) >> aeolus_stop(0, 4, False),

			]
		],

		ChannelFilter(1) >> CtrlFilter(0x5c) >> [
			# 29 Tremolo to II & III
			CtrlValueFilter(0x7f) >> aeolus_stop(1, 12, True),
			CtrlValueFilter(0x00) >> aeolus_stop(1, 12, False),
		],
	]
)