#import modules and set workspace enviornments
import arcpy
import csv
import os
arcpy.env.overwriteOutput = 1

###
###               SCRIPT SETUP, CHANGE VARIABLES
###
#Setup Pathfiles, Field and SR, this is where the user can moodify variables

csvPath = "D:\\411\\taxi\\taxi.csv" #insert your path to your csv file
outputFolder = "D:\\411\\taxi\\" #insert the path to your output location, add \\ to the end
outputName = "taxi.shp" #the name of your desired output
fullPath = os.path.join(outputFolder, outputName)
fields = ("SHAPE@", "CAR",) #changing the second variable will create a new field name for tracks
# create list of index
keyIndex = 1 #index for your polyline key
lonIndex = 2 #index of your x variable
latIndex = 3 #index of your y variable
sr = arcpy.SpatialReference("WGS 1984") #add desired projection

###
###                     SCRIPT RUNS FROM HERE
###

#create shape file to write new polylines
arcpy.CreateFeatureclass_management(outputFolder, outputName, "POLYLINE", "", "", "", sr)

#add fields to shape file, added some flexability so user can change variables in setup.
arcpy.AddField_management(fullPath, fields[1], "TEXT")


#create function to add car keys to dictionary and populate arrays
def checkKey(car, X, Y, dictionary):
    if car not in dictionary:
        #create array
        array = arcpy.Array()
        #create point
        newPoint = arcpy.Point(X, Y)
        #add point to arry
        array.add(newPoint)
        #add array to to dictionary using car id as key
        dictionary[car] = array
    else:
        point = dictionary[car]
        newPoint = arcpy.Point(X, Y)
        point.append(newPoint)

#Create CSV Reader to look through taxi CSV
with open(csvPath, "r") as infile:
    csvReader = csv.reader(infile)
    header = csvReader.next()

#Set up function to create the dictionary, to be populated with arrays
    carDictonary = {}
    for row in csvReader:
    #create variables we want in dictionary
        car = row[keyIndex]
        X = row[lonIndex]
        Y = row[latIndex]
    #create function check
        checkKey(car, X, Y, carDictonary)

#USE insert cursor to add polylines to shapefile.
with arcpy.da.InsertCursor(fullPath, fields) as cursor:
    for car in carDictonary:
        polyline = arcpy.Polyline(carDictonary[car], sr)
        newRow = (polyline, car)
        cursor.insertRow(newRow)
arcpy.AddMessage("Create polyline shapefile is complete!")
arcpy.GetMessage(0)