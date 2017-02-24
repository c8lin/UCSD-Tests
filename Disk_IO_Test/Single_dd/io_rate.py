#!/usr/bin/env python

import os

n_GB = 15
n_iters = 3

print str(n_GB) + 'GB, ' + str(n_iters) + ' iterations.'
os.system('./disk-io.sh ' + str(n_GB) + ' ' +  str(n_iters))

write = open('writes.time', 'r')
read = open('reads.time', 'r')

wr_time = 0
rd_time = 0

for time in write:
    wr_time += float(time)

for time in read:
    rd_time += float(time)

write.close()
read.close()

wr_time /= n_iters
rd_time /= n_iters

wr_rate = ((n_GB*1024**3)/(1000**2))/wr_time
rd_rate = ((n_GB*1024**3)/(1000**2))/rd_time

print '=================================='
print 'Write speed (avg) is ' + ("%.4f" % wr_rate) + ' MB/s.'
print 'Read speed (avg) is ' + ("%.4f" % rd_rate) + ' MB/s.'
