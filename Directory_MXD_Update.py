#-------------------------------------------------------------------------------
# Name:        MXD Route/FC Updater For Directory
# Purpose:     To update a directory containing multiple MXD's with an Updataed
#               Feature Class
#
# Author:      Cody Wilson
#
# Created:     09/06/2014
# Copyright:   (c) Cody 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy, string, os, glob
import arcpy.mapping as MAP
from arcpy import env

#Script Parameters
ws_1 = r"C:\Users\Cody\Dropbox\DATA\temp" #<----------- Change Me
out_directory = r"C:\Users\Cody\Dropbox\DATA\temp\output" #<----------- Change Me
output_pdf_book = "Mapbook_Route_B.pdf"#<----------- Change Me
output_pdf_book_path = str(out_directory + "\\" + output_pdf_book)#<----------- Change Me
# Set New FC/Route name and worskspace/ designed to be in different FGDB than current Route
ws_2 = r"C:\Users\Cody\Dropbox\DATA\temp\foo2.gdb"#<----------- Change Me
inputlayer = "Hydro"#<----------- Change Me ** Route Update, or FC to be Updated

# Set workspace of arcpy and python
env.workspace = ws_1
os.chdir(ws_1)
print ws_1

# Checks if output directory (for pdf's) exsists, and if not creates it
if not os.path.exists(out_directory):
    os.makedirs(out_directory)

#List MXD's in Dir
MXDList = glob.glob('*.mxd')
print MXDList


################################################################################
## For each MXD update specific layer (Keeps same symbology)
## and exports pdf with same name as MXD,
for MXDPath in MXDList:
    # Setting Variables
    MXD = MAP.MapDocument(MXDPath)
    out_pdf = str(out_directory + "\\" + MXDPath)
    # Search through each dataframe in MXD
    for dataframe in arcpy.mapping.ListDataFrames(MXD):
        #
        lyrs = arcpy.mapping.ListLayers(dataframe)
        for lyr in lyrs:
            if lyr.datasetName == inputlayer:
                lyr.replaceDataSource(ws_2, "FILEGDB_WORKSPACE", inputlayer)
    MXD.save()
    MAP.ExportToPDF(MXD, out_pdf) # http://help.arcgis.com/en/arcgisdesktop/10.0/help/index.html#//00s300000027000000 for further parameters
#################################################################################
##Combine exported pdf's into mapbook
# look throgh output folder and create pdf mapbook
os.chdir(out_directory)
PDFList = glob.glob('*.pdf')
#Set file name and remove if it already exists
if os.path.exists(output_pdf_book_path):
    os.remove(output_pdf_book_path)

#Create the file and append pages
pdfDoc = arcpy.mapping.PDFDocumentCreate(output_pdf_book_path)
for pdf in PDFList:
    pdfDoc.appendPages(pdf)

#Commit changes and delete variable reference
pdfDoc.saveAndClose()
del pdfDoc

