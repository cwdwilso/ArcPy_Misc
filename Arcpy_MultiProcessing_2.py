#-------------------------------------------------------------------------------
# Name: Script_4.py
# Purpose: To explore the difference in geoprocessing times between serial and
# and parallel/concurrent processing.
# Author: Cody Wilson
#
# Created:     16/11/2013
# Copyright:   (c) Cody 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import multiprocessing as mp
import arcpy, os, time

print "Successfully imported modules..."
print "Defining script functions...."
print
print
## Warning to let users know that messages will not be ruturned to the IDLE
print "No messages from the children processes will not be returned to the IDLE"
print "Please use the Task manager to moniter the children processes"
print "The task should take ~300 seconds..."
################################################################################
## Buffer Function (containing geoprocessing logic)
def buffer(r):
    workspace = r"DIR:\strategy_2_b" ## make sure workspace points to the strategy_2_b folder
    arcpy.env.workspace = workspace
    j = r[1]
    s = r[0]
    ## Location of dataset
    godzilla = r"DIR:\strategy_2_b\TR_1760009_1.shp" #### set proper dir strategy_2_b folder
    ## Creates feature class for each range
    arcpy.CreateFeatureclass_management(r"DIR:\strategy_2_b", r"FID_to_{0}_1760009_1.shp".format(j) , "POLYGON") #### set proper dir strategy_2_b folder
    with arcpy.da.SearchCursor(godzilla, ["FID", "SHAPE@"]) as cursor: ## Search cursor to access feature FID and geometry
        for row in cursor:
            FID = row[0]
            GEOM = row[1]
            if FID >= s and FID <= j: ## if FID is within range
                b_fc = GEOM.buffer(10) ## Geometry is buffered by 10 meters
                c = arcpy.da.InsertCursor(r"FID_to_{0}_1760009_1.shp".format(j), ["SHAPE@"]) ## Insert cursor to place the resulting geometry
                c.insertRow([b_fc])
            else:
                pass

        del cursor
        del c
        del row
        ## Deleting cursor variables
##
################################################################################
################################################################################
## Main function to perform the concurrent processing
def main():
    ## Ranges determined by dividing the FID's into 8 ~equal groups
    ranges = [[0, 35000], [35001, 70000], [70001, 105000],[105001, 140000], [140001, 175000], [175001, 210000], [210001, 245000], [245001, 290000]]
    ## Create a pool class and run the jobs--the number of jobs is
    ## equal to the length of the range list
    pool = mp.Pool()
    pool.map_async(buffer, ranges)


    ## Synchronize the main process with the job processes to
    ## Ensure proper cleanup.
    pool.close()
    pool.join()
    ## End main
##
################################################################################
multiprocess_start = time.time()
if __name__ == '__main__':
    main()


print 'It took', time.time()-multiprocess_start, 'seconds to process data concurrently using all available cores'
