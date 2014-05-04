#!/bin/bash
# args to videoProcess are: filename saveDir startFrame nfile ncall secPerCpu

python $HOME/code/github/mouseVideo-analysis/videoProcess.py $1 $2 $3 $4 $SGE_TASK_ID $5
