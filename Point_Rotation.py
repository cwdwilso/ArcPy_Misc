#-------------------------------------------------------------------------------
# Name: Point Rotation Script
# Purpose: Given point shapefile(s), this script rotates and calculates
#   new x and y coordinates of points given a point of rotation and a rotation
#   angle
#
# Authors: Cody Wilson, Harry Kim
#
# Created:     19/10/2013
# Copyright:   (c) Cody/Harry 2013
#-------------------------------------------------------------------------------

## Import arcpy, math, and numpy modules, and allow files to be overwritten.
import arcpy, math, numpy
from arcpy import env
arcpy.env.overwriteOutput = True

## Setting variables for the rotation tool
workspace = arcpy.GetParameterAsText(0)
arcpy.env.workspace = workspace
Rotation_Point = str(arcpy.GetParameterAsText(1))
input_rotation_point = arcpy.GetParameterAsText(2)
input_point_fc = arcpy.GetParameterAsText(3)
theta = float(arcpy.GetParameterAsText(4))
radian = theta*2*math.pi/360
output_FC_name = arcpy.GetParameterAsText(5)

## Defining The Spatial Reference for the new feature class
sr = arcpy.Describe(input_point_fc).spatialReference

## Output Feature class of rotated points
output_point_fc = arcpy.CreateFeatureclass_management(workspace, output_FC_name, "POINT", input_point_fc, "DISABLED", "DISABLED", sr)


## Array of fields to be added to the output feature class
narray = numpy.array([],
numpy.dtype([('_ID', numpy.int),
             ('ORIG_X', numpy.float),
             ('ORIG_Y', numpy.float),
             ('NEW_X', numpy.float),
             ('NEW_Y', numpy.float),
             ]))

## Add fields to feature class
arcpy.da.ExtendTable(output_point_fc,"OID@", narray, "_ID")

## Checks to see if the point of rotation is the first point in file.
if Rotation_Point == "true":
    with arcpy.da.SearchCursor(input_point_fc, ["OID@", "SHAPE@X", "SHAPE@Y"]) as cursor:
## Using the search cursor function, finds the x and y coordinates of the point that the deflection angle will be performed on
## Since this point is the first point in file, the coordinates of the first point are extracted
        for row in cursor:
            sort = row[0]
            if sort == 0:
                x_orig = row[1]
                y_orig = row[2]
## The x and y coordinates of the rest of the points are extracted
            if sort >= 1:
                x = row[1]
                y = row[2]
## Two dimension rotation matrix formula is used to calculate the new x and y coordinates
## The x and y values of a given point is subtracted by the x and y values of the point of rotation so that the rotation is performed using the origin
## Since the math module only used radian values, the radian variable was used to modify degrees input into radian values
                x2 = ((x-x_orig)*math.cos(-radian))-((y-y_orig)*math.sin(-radian))
                y2 = ((x-x_orig)*math.sin(-radian))+((y-y_orig)*math.cos(-radian))
## The final x and y coordinates are calculated by adding back the x and y values of the point of rotation
                x_final = x2 + x_orig
                y_final = y2 + y_orig
                transformed_point = arcpy.Point(x_final, y_final)
## Using the insert cursor function, create attribute table that includes the feature geometry (token), original x and y coordinates, and the new x and y coordinates
                with arcpy.da.InsertCursor(output_point_fc, ["SHAPE@", "ORIG_X", "ORIG_Y", "NEW_X", "NEW_Y"]) as cursor2:
                    cursor2.insertRow([transformed_point, x, y, x_final, y_final])

## If the point of rotation is not the first point in file, a rotation point feature class is used
else:
## Using search cursor function on the rotation point feature class, the x and y coordinates of point of rotation is extracted
    with arcpy.da.SearchCursor(input_rotation_point, ["OID@", "SHAPE@X", "SHAPE@Y"]) as cursor:
        for row in cursor:
            x_orig = row[1]
            y_orig = row[2]
## Using search cursor function, extract the x and y coordinates of the rest of the points and perform the rotation using the same formula seen from previous statement
    with arcpy.da.SearchCursor(input_point_fc, ["OID@", "SHAPE@X", "SHAPE@Y"]) as cursor2:
        for row in cursor2:
            x = row[1]
            y = row[2]
            x2 = ((x-x_orig)*math.cos(-radian))-((y-y_orig)*math.sin(-radian))
            y2 = ((x-x_orig)*math.sin(-radian))+((y-y_orig)*math.cos(-radian))
            x_final = x2 + x_orig
            y_final = y2 + y_orig
            transformed_point = arcpy.Point(x_final, y_final)
## Using the insert cursor function, create attribute table that includes the geometry (token), original x and y coordinates, and the new x and y coordinates
            with arcpy.da.InsertCursor(output_point_fc, ["SHAPE@", "ORIG_X", "ORIG_Y","NEW_X", "NEW_Y"]) as cursor2:
                cursor2.insertRow([transformed_point, x, y, x_final, y_final])








