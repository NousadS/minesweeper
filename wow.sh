#!/bin/bash

source ./venv/bin/activate

PROGRAM="python main.py"

$PROGRAM &
PROGRAM_PID=$!

while kill -0 $PROGRAM_PID 2>/dev/null; do
    MEM_USAGE=$(pmap $PROGRAM_PID | tail -n 1 | awk '/total/ {print $2}' | sed 's/K//')

    if [[ $MEM_USAGE -gt 10000000 ]]; then
        echo "10 GB Reach..."

        kill -9 $PROGRAM_PID
        break
    fi

    sleep 1
done
