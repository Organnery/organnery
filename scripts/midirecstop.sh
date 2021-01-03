#!/bin/bash

# get pid of current midi recorder
PID=$(pgrep -x arecordmidi)
if [ ! -z $PID ]; then
  echo found midi recorder $PID from runnning processes >> $HOME/organnery.log
# stop midi recorder
  echo stopping midi recorder  >> $HOME/organnery.log
  kill -INT $PID
else
  echo no midi recorder process found, no recorder to stop >> $HOME/organnery.log
fi
