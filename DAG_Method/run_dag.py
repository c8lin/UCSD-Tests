#!/usr/bin/env python
'''
Run as follows:
    ./run_dag.py NUM_JOBS MAX_JOBS

This will submit a DAG to HTCondor that can run at most MAX_JOBS concurrent
jobs, and NUM_JOBS jobs will be scheduled. If NUM_JOBS is greater than
MAX_JOBS, then MAX_JOBS jobs will be run and once any jobs are complete,
additional jobs will be introduced to bring it back up to MAX_JOBS, until a 
total of NUM_JOBS jobs have run.
'''

import sys
import os

n_jobs = int(sys.argv[1]) # Get NUM_JOBS
dag_file = "dag_submit.dag"
sub_file = "submit_single.file" # Name of condor submit file for each job

# Create DAG file to submit
file = open(dag_file, "w")
for n in range(n_jobs):
    file.write("JOB job" + str(n) + " " + sub_file + "\n")
    file.write("VARS job" + str(n) + " runnumber=\"" + str(n) + "\"\n")
file.close()

max_jobs = int(sys.argv[2]) # Get MAX_JOBS

# Submit the DAG to the system to run
os.system("condor_submit_dag -f -maxjobs " + str(max_jobs) \
    + " -maxidle " + str(max_jobs) + " " + dag_file) 
