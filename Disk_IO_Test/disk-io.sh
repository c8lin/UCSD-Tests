#!/bin/bash

size=1G
count=$1
n_iters=$2

rm -f writes.time
rm -f reads.time

echo "Testing disk I/O on $(hostname)."
for ((i=1; i<=$n_iters; i++)); do
    /usr/bin/time -f '%e' -o 'writes.time' -a dd bs=$size count=$count if=/dev/zero of=file.tmp oflag=nocache,dsync
    /usr/bin/time -f '%e' -o 'reads.time' -a dd bs=$size count=$count if=file.tmp of=/dev/null iflag=nocache,dsync
done

rm file.tmp
