#!/bin/bash
if [[ `pgrep -f arecordmidi` ]]; then
    echo "Currently Recording"
    exit 1
else
    echo "NOT Recording"
    exit 0
fi
