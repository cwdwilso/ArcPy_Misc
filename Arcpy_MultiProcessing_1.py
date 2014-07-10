#-------------------------------------------------------------------------------
# Name: Script_2.py
# Purpose: To explore the difference in geoprocessing times between serial and
# and parallel/concurrent processing.In this script conurrency strategy 1 is
# processed concurrently.
#
# Author: Cody Wilson
#
# Created:     16/11/2013
# Copyright:   (c) Cody 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import multiprocessing as mp
import arcpy, os, time, sys

multiprocess_start = time.time()
workspace = r"DIR:\strategy_1_b" ## make sure workspace points to the strategy_1_b folder
arcpy.env.workspace = workspace

print "Successfully imported modules..."
print "Defining script functions...."
print
print
## Warning to let users know that messages will not be ruturned to the IDLE
print "No messages from the children processes will not be returned to the IDLE"
print "Please use the Task manager to moniter the children processes"
print "The task should take ~118 seconds..."

################################################################################
## Geoprocessing function
def geoprocess_func(f):
    split = os.path.split(f)
    fc_name = str(split[1])
    output_features = os.path.join(split[0], "buffer_dissolve_" + fc_name)
    arcpy.Buffer_analysis (f, output_features, "10 Meters", "", "", "ALL")
##
################################################################################
################################################################################
## Main function to perform the concurrent processing
def main():
    fcs = arcpy.ListFeatureClasses()
    fc_list = [os.path.join(workspace, fc) for fc in fcs]
    ## Create a pool class and run the jobs--the number of jobs is
    ## equal to the length number of features in fc_list
    pool = mp.Pool(4)
    pool.map_async(func = geoprocess_func, iterable = fc_list)
    ## Synchronize the main process with the job processes to
    ## Ensure proper cleanup.
    pool.close()
    pool.join()
    ## End main
##
################################################################################
if __name__ == '__main__':
    main()


print 'It took', time.time()-multiprocess_start, 'seconds to process data concurrently using all available cores'



