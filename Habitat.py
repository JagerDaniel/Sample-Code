#This script will buffer roads to find areas suitable for bird watching, then remove private land from
#suitable watching areas for species.

#import acrpy for tools and os for new file paths
import arcpy
import os


#setup variables
inputFolder = arcpy.GetParameterAsText(0)
inputRoads = arcpy.GetParameterAsText(1)
inputPrivateLand = arcpy.GetParameterAsText(2)
bufferdist = arcpy.GetParameterAsText(3)
birdviews = arcpy.GetParameterAsText(4)
inputExtent = arcpy.GetParameterAsText(5)

#setup env params, overwrite and extent
arcpy.env.overwriteOutput = True
arcpy.env.extent = inputExtent



#buffer road and create new file named and define path for erase tool
buffName = inputRoads.replace(".shp", "_buffered.shp")
arcpy.Buffer_analysis(inputRoads, buffName, bufferdist)
buffPath = os.path.join(buffName)
#erase unwanted area from clipped feature and create new file and define path for clip tool
eraseName = buffPath.replace("_buffered.shp", "_erased.shp")
arcpy.Erase_analysis(buffPath, inputPrivateLand, eraseName)
clipPath = os.path.join(eraseName)

#for each habitat file the tool will clip the suitable area and create new file
arcpy.env.workspace = inputFolder
fcList = arcpy.ListFeatureClasses()
for fc in fcList:
    outputName = os.path.join(birdviews, fc + "_view")
    arcpy.Clip_analysis(fc, clipPath, outputName)

#add finish message
arcpy.AddMessage("Tool is successful.")
print arcpy.GetMessage(0)


