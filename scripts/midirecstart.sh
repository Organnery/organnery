#!/usr/bin/env bash

## load default configuration file & attempt to load user configuration file from USB
source /etc/organnery/organnery.conf
if [ -f $HOME/stops/organnery.conf ]; then
        echo "loading organnery.conf from home|usb" >> $HOME/organnery.log
	source $HOME/stops/organnery.conf
fi

# check for necessary options
if [ -z "${MIDI_REC_FOLDER}" ]; then
 echo MIDI_REC_FOLDER value is empty, please check organnery.conf >> $HOME/organnery.log
 exit 1
fi
if [ -z "${MIDI_REC_FORMAT}" ]; then
 echo MIDI_REC_FORMAT value is empty, please check organnery.conf >> $HOME/organnery.log
 exit 1
fi
if [ -z "${MIDI_REC_SOURCE}" ]; then
 echo MIDI_REC_SOURCE value is empty, please check organnery.conf >> $HOME/organnery.log
 exit 1
fi

#debug
 echo MIDI_REC_FOLDER $MIDI_REC_FOLDER
 echo MIDI_REC_SOURCE $MIDI_REC_SOURCE
 echo MIDI_REC_FORMAT $MIDI_REC_FORMAT

# check if record folder exists or create it
if [ ! -d $HOME/stops/$MIDI_REC_FOLDER  ]; then
  echo creating non existent midi recording folder $MIDI_REC_FOLDER >> $HOME/organnery.log
  mkdir $HOME/stops/$MIDI_REC_FOLDER
fi

# make sure no midi recording or playing is active
if pgrep -x aplaymidi &> /dev/null 2>&1; then
  echo **a midi file is currently playing, exiting >> $HOME/organnery.log
  exit 1
fi
if pgrep -x arecordmidi &> /dev/null 2>&1; then
  echo **a midi file is currently recording, exiting >> $HOME/organnery.log
  exit 1
fi

# generate filename
now=$(date +"%y%m%d_%H%M%S")
filename=organnery_rec_$now.mid

# start recorder
if [ "$MIDI_REC_FORMAT" = "0" ]; then
  # file 0 format (all midi channels on same track)
  echo starting recording midi file $filename with format 0 >> $HOME/organnery.log
  arecordmidi -p $MIDI_REC_SOURCE $HOME/stops/$MIDI_REC_FOLDER/$filename &
else
  # file 1 format (each midi channel on a track)
  echo starting recording midi file $filename with format 1 >> $HOME/organnery.log
  arecordmidi -s -p $MIDI_REC_SOURCE $HOME/stops/$MIDI_REC_FOLDER/$filename &
fi
