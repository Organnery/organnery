#!/bin/bash

# get the file to play from first argument
if [ -z $1 ]; then
  echo **you have to give the file to play in argumentm exiting >> $HOME/organnery.log
  exit 1
fi

filename=$1

# check if file exists or exit
if [ ! -e $filename ]; then
  echo **cannot find the file to play $filename, exiting >> $HOME/organnery.log
  exit 1
fi
echo **file $filename exists, going on >> $HOME/organnery.log

# make sure no midi recording or playing is active
if pgrep -x aplaymidi &> /dev/null 2>&1; then
  echo **a midi file is currently playing, exiting >> $HOME/organnery.log
  exit 1
fi
if pgrep -x arecordmidi &> /dev/null 2>&1; then
  echo **a midi file is currently recording, exiting >> $HOME/organnery.log
  exit 1
fi

# start player
echo starting playing midi file $filename >> $HOME/organnery.log
aplaymidi -p aeolus:0 $filename &
PLAYER_PID=$!

# look for player end
wait $PLAYER_PID
echo END playing midi file $filename >> $HOME/organnery.log

