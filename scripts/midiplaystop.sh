#!/bin/bash

# get pid of current midi player
PID=$(pgrep -x aplaymidi)
if [ ! -z $PID ]; then
  echo found midi player $PID from runnning processes >> $HOME/organnery.log
# stop midi player
  echo stopping midi player  >> $HOME/organnery.log
  kill $PID
else
  echo no midi player process found, no player to stop >> $HOME/organnery.log
fi

