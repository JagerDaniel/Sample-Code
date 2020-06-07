#This script is to be used within a ArcMap Tool to find Parcels of residents affected by the new Tax

#Import Arcpy Module
import arcpy

#Setup Variables that will be replaced with get Parameter
parcels = arcpy.GetParameterAsText(0)
zones = arcpy.GetParameterAsText(1)
output = arcpy.GetParameterAsText(2)


#Set the fields that will be used in tuple first tuple is 0
fields = ("TOTAPR", "STATE")

#Make the feature layer your selecting from
valueQuery = '"TOTAPR" > 300000'
arcpy.MakeFeatureLayer_management(parcels, "Parcels300k", valueQuery)

#Make the feature layer to select R2
zoneQuery = '"ZONE" = ' + "'R2'"
arcpy.MakeFeatureLayer_management(zones, "R2Layer", zoneQuery)

#Select by location using the feature layers
arcpy.SelectLayerByLocation_management("Parcels300k", "INTERSECT", "R2Layer", "-2 Feet")
#create count variables
state = 0
outOfStateOwn = 0
#open search cursor, use two count variables to calculate number owners outside of Washington
with arcpy.da.SearchCursor("Parcels300k", fields)as cursor:
    for row in cursor:
        if row[1] != "WA":
            outOfStateOwn += 1
        state += 1
#create a new shapefile with the select by location layer
arcpy.CopyFeatures_management("Parcels300k", output)

#calc percent and print informative message
percOutState = (float(outOfStateOwn) / float(state))* 100
arcpy.AddMessage(str(percOutState) + " percent of property owners affected by the change, have addresses listed outside of Washington State.")
print arcpy.GetMessage(0)




#clean up feature layers
arcpy.Delete_management("Parcels300k")
arcpy.Delete_management("R2Layer")