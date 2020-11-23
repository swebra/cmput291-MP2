#!/bin/bash

runPhase1 () {
    /usr/bin/time -f "Total exec time: %E\nUsr time: %U\nSys time: %S\nTotal CPU time/exec time: %P\nMax mem: %MKb" python phase1.py 27017
}

# Set any environment parameters here

runPhase1
