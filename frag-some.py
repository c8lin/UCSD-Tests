#!/usr/bin/env python

# Conversion of frag-some.pl into Python script

import os
import sys

# Make command line calls to programs ls and ldd
print; sys.stdout.flush() 
os.system("ls -lah")

# Obtain command line arguments
sample = sys.argv[1]
offset, id, count, reqs = [int(i) for i in sys.argv[2:6]]

print "frag-some.pl --- " \
    + "   ".join((sample, str(offset), str(id), str(count), str(reqs))) + '\n'
sys.stdout.flush()

# Set up paths for file downloads and xrdfragcp executable 
PREF = "root://xrootd.t2.ucsd.edu:2050/"
BASE = "./"
XFCP = BASE + "xrdfragcp"
SMPL = BASE + sample

sample_file = None    # Open the sample file list
try:
    sample_file = open(SMPL, 'r')
except OSError:
    print "Can't open " + SMPL + " sample list."
    exit()

path_list = []    # Create list to store sample file paths

# Loop through and read every line in the sample file list
for line in sample_file:
    line.strip()
    path, size = line.split(" ")
    path_list.append(path)
    
sample_file.close()

n_paths = len(path_list) # Number of sample files read from sample file list

# Set total read size, number of read requests and time between reads
rd_size = reqs * 1024 * 1024 * 20     # 20MB ...
rd_reqs = reqs
rd_time = reqs * 10                   # per 10 seconds.

print "Read " + str(n_paths) + " lines from " + SMPL + ".\n"; sys.stdout.flush()
os.system("ls -lh")

beg = offset + id + count             # Set beginning index
for i in range (beg, beg + count):    # Download 'count' number of files
    fid = i % n_paths
    url = PREF + path_list[fid]
    cmd = XFCP + " --verbose --cmsclientsim "
    cmd += str(rd_size) + " " + str(rd_reqs) + " " + str(rd_time) + " "
    cmd += url

    print "\nGoing to run " + cmd + ".\n"; sys.stdout.flush()
    os.system(cmd)
    print "\nJob ended.\n"; sys.stdout.flush()
