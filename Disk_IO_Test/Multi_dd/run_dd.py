#!/usr/bin/env python

import os
import sys

'''
Author: Benjamin Steer
Date modified: 02/24/17

USAGE:
       ./run_dd.py N_TESTS

where N_TESTS is the number of dd read commands to run concurrently. The N_TESTS number of commands 
are distributed evenly across the disks of the particular node/cabinet. Output files are written to
the same folder as this script is located.

NOTE: Root access to the nodes/cabinets is required in order to create the temporary sample files to 
read from each disk.
'''

n_tests = int(sys.argv[1]) # Number of concurrent dd calls to run, taken from command line

size = 1     # File block size in 'unit' Bytes, maximum allowed by dd is 2.0GB
unit = 'G'
count = 1    # Number of file blocks to read per dd call

n_disks = 12 # Number of disks on the node/cabinet

try:
    os.remove('multi_dd.sh')
    os.remove('reads.time')
    os.remove('results.txt')
except OSError:
    pass

# Create list of disk names, where convention for nodes/cabinets at t2.ucsd.edu is disk1, disk2, etc.
ls_disknames = []
for i in range(n_disks):
    ls_disknames.append('data' + str(i+1))

os.system('echo Testing disk I/O on $(hostname).')
os.system('date')

# Create sample files to read from each disk, of the above-specified file size
for diskname in ls_disknames:
    os.system('mkdir /' + diskname + '/dd_test')
    os.system('dd bs=' + str(size) + unit + ' count=' + str(count) + ' if=/dev/zero of=/' + diskname \
              + '/dd_test/file.tmp iflag=fullblock status=none') 

multi_dd = open('multi_dd.sh', 'w') # Create the shell script 'multi_dd.sh' which runs the dd commands

per_disk = n_tests/n_disks     # Number of dd commands per disk
last_disk = n_tests % n_disks  # Remainder after distribution among disks

for diskname in ls_disknames:
    rem = 0 # If the number of tests doesn't divide evenly among disks, distribute remainder
    if last_disk > 0:
        rem = 1
        last_disk -= 1

    # Write the dd calls to the shell script 'multi_dd.sh', using the ampersand & to run the commands 
    # in the background. Each call is timed, and the times are stored in the file 'reads.time'. 
    for i in range(per_disk + rem):
        multi_dd.write('/usr/bin/time -f \'%e\' -o \'reads.time\' -a dd bs=' + str(size) + unit \
                       + ' count=' + str(count) + ' if=/' + diskname \
                       + '/dd_test/file.tmp of=/dev/null iflag=nocache,dsync' + ' status=none &\n')

multi_dd.write('echo\n')
multi_dd.write('wait\n')
multi_dd.write('echo Done.\necho\n')
multi_dd.close()

os.system('chmod a+x multi_dd.sh') # Give execution privileges to the shell script
os.system('./multi_dd.sh')         # Run the script
os.system('date')

# Remove sample files from each disk after completion       
for diskname in ls_disknames:
    os.system('rm -r /' + diskname + '/dd_test')

# Open the file 'reads.time' and add up all the completion times from each dd call
read = open('reads.time', 'r')
rd_time = 0
for time in read:
    rd_time += float(time)
read.close()

# Take average of completion times and use it to calculate average read rate per dd call
rd_time /= n_tests
rd_rate = ((count*size*1024**3)/(1000**2))/rd_time

# Save results of test to the file 'results.txt', along with the parameters used in the test
results = open('results.txt', 'w')
results.write('Ran ' + str(n_tests) + ' concurrent dd reads, each with ' + str(count) \
              + ' set(s) of ' + str(size) + unit + 'B blocks, with ' + str(n_disks) + ' disks.\n') 
results.write('Average read speed is ' + ("%.4f" % rd_rate) + ' MB/s.\n')
results.close()

os.system('cat results.txt')
