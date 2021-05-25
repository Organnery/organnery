#!/bin/bash
if [[ `pgrep -f aplaymidi` ]]; then
    echo "Currently Playing"
    exit 1
else
    echo "NOT Playing"
    exit 0
fi
