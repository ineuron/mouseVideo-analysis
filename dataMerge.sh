#!/bin/bash

DIR=$1
njobs=$2

touch $DIR/file.txt
echo $(ls $DIR/file*.txt | wc -l)
echo 'Waiting for all cpus to finish'
while (( $(ls $DIR/file*.txt | wc -l) < $njobs ))
do
  sleep 1
  echo $(ls $DIR/file*.txt | wc -l)
done
echo 'All jobs done'

cat $DIR/file*.txt > $DIR/trackingData.txt
rm -f $DIR/file*.txt

avimerge -o $DIR/trackingMovie.avi -i $DIR/file*.avi
rm -f $DIR/file*.avi

python /lmb/home/tbranco/code/dataProcess.py $1

#for f in $DIR/file*.avi
#do
#  /usr/bin/ffmpeg -i $f $DIR/$(basename $f .avi).mpg
#done