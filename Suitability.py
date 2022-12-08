#############################################################################################################
# Program name: Suitability.py
# Suitability analysis model | Section 61 Group 05
# Anand Charvin Gopalakrishnan, Andy Mo, Meet Hitendra Naik, Ming Xuan Su

# The program works by taking in inputs from the user including X,Y cordinates 
# and values for parameters which will then be used to create a suitability analysis form in arcpy.
# Assumptions are that user don't input invalid data, also there is a random 
# x,y cordinate generator option implemented for just playing with the program.
# The limitations include tkinter implementaion for output, 
# It doesn't have a scroll bar element so more than 25 inputs won't be shown. 
# It is just a limit over there. Pandas implementation to display the same on the terminal resulted in too much issues with the manual input. 
# It will be resolved eventually down the line after the submission as part of maintenence and planned features.
# Symbology layer system in arc cannot impart proper colors to the buffer, that must be done manually in arcgis.

# - Inputs  - Manual Entry, CSV File, Database, Database Folder Path, Symbology Layer
# - Outputs - XY Point to Table in Arc, Buffers, Merged buffer

# General References include : 
# https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html
# https://docs.python.org/3/library/tkinter.html
# https://realpython.com/python-csv/
# https://pro.arcgis.com/en/pro-app/latest/tool-reference/data-management/xy-table-to-point.htm

# It is a collaborative project with each modules and some being made individually and collaboratevely. 
# the secions are marked on comments on top to differentiate that. 
# This is a product of team work and a few sleepless nights.
            
##############################################################################################################           
# Import the necessary modules
import arcpy    # Arcpy for ArcGIS related function
import csv      # csv module to read csv
import random   # random to generate random csv
from tkinter import * # tkinter for gui result display at the end.
from sys import argv
import os
import pandas as pd # Pandas for reading the csv file functions

#################################################################
# | Proximity weight calculation   - Anand Charvin & Andy Mo  | #
#################################################################
# Function to calculate the proximity weight
def calculate_proximity_weight(distance, threshold):
        # Check if the distance is zero
    if distance == 0:
        # If the distance is zero, return a value of zero
        return 0
    else:
        # Calculate the proximity
        distance = float(distance)
        proximity = 1 / distance
        
        # Return the proximity weight
        return min(proximity / threshold, 1)

###############################################################################################
# | Suitability value calculator   - Full collab - Code by Anand Charvin, Andy, Meet, Ming  | #
###############################################################################################

def calculate_suitability_value(location, power_plants_threshold, power_plants_max_threshold, heavy_industries_threshold, heavy_industries_max_threshold, high_risk_areas_threshold, high_risk_areas_max_threshold, rivers_streams_threshold, rivers_streams_max_threshold, heavy_traffic_threshold, heavy_traffic_max_threshold):
    x = location[0]
    y = location[1]
    power_plants_distance = location[2]
    heavy_industries_distance = location[3]
    high_risk_areas_distance = location[4]
    rivers_streams_distance = location[5]
    heavy_traffic_distance = location[6]

    # Calculate the suitability value of the location
    suitability_value = max_threshold
    suitability_value -= (1 - min(power_plants_distance, power_plants_threshold) / power_plants_max_threshold) * 40
    suitability_value -= (1 - min(heavy_industries_distance, heavy_industries_threshold) / heavy_industries_max_threshold) * 45
    suitability_value -= (1 - min(high_risk_areas_distance, high_risk_areas_threshold) / high_risk_areas_max_threshold) * 70
    suitability_value -= (1 - min(rivers_streams_distance, rivers_streams_threshold) / rivers_streams_max_threshold) * 25
    suitability_value -= (1 - min(heavy_traffic_distance, heavy_traffic_threshold) / heavy_traffic_max_threshold) * 25

    # Ensure that the suitability value is within the minimum and maximum threshold
    suitability_value = max(min_threshold, suitability_value)
    suitability_value = min(max_threshold, suitability_value)

    return suitability_value

# Function to calculate the suitability message for a location
def calculate_suitability_message(suitability):
    # Check the suitability score
    if suitability < 70:
        suitability_message = "Bad"
    elif suitability < 50:
        suitability_message = "Worse"
    elif suitability < 10:
        suitability_message = "Passable"
    else:
        suitability_message = "Suitable"
        
    # Return the suitability message
    return suitability_message

###########################################
# | Inputs and Processing    - Andy Mo & Meet | #
###########################################

# Ask the user if they want to input the data manually or from a CSV file
input_mode = int(input("Enter 1 to input the data manually, or 2 to input the data from a CSV file: "))

# Pandas csv implementation - Anand Charvin
# Read the input data from a CSV file or from the user
if input_mode == 2:
        # Read the input data from a CSV file
        df = pd.read_csv('input.csv')
        # Access the values in the DataFrame as a 2D numpy array
        # Drop the first row
        df = df.drop(df.index[0])
        locations = df.values
else:
        # Read the input data from the user
        locations = []

        while True:
            # Ask the user if they want to generate random X and Y coordinates
            coordinates_mode = int(input("Enter 1 to generate random X and Y coordinates, or 2 to input the coordinates manually: "))
            
            
            # Generate random X and Y coordinates or read them from the user
            if coordinates_mode == 1:
                x = random.uniform(-180, 180)
                y = random.uniform(-90, 90)
            else:
                # Ask the user to input the values for the factors of a location
                x = float(input("Enter the X coordinate (longitude): "))
                y = float(input("Enter the Y coordinate (latitude): "))
                
        
        # Ask the user to input the values for the other factors of the location
            power_plants_distance = float(input("Enter the distance from nearby power plants (km): "))          
            heavy_industries_distance = float(input("Enter the distance from heavy industries (km): "))
            high_risk_areas_distance = float(input("Enter the distance from high risk areas (km): "))
            rivers_streams_distance = float(input("Enter the distance from rivers and streams (km): "))
            heavy_traffic_distance = float(input("Enter the distance from heavy traffic zones (km): "))
                
            # Add the location data to the list of locations
            location_data = [x, y, power_plants_distance, heavy_industries_distance, high_risk_areas_distance, rivers_streams_distance, heavy_traffic_distance]
            locations.append(location_data)

            # Ask the user if they want to continue inputting the data
            while True:
                print("Enter 1 to continue inputting the data, or 2 to finish: ")
                continue_input = input()
                if continue_input.isdigit():
                    continue_input = int(continue_input)
                    if continue_input == 1:
                        # Continue to the next iteration of the loop
                        break
                    elif continue_input == 2:
                        # Break out of the loop and continue to the next section of the code
                        break
                else:
                    print("Error: invalid input. Please enter 1 or 2.")
            if continue_input == 2:
                break

########################################################################
# | Threshold Definition   - Andy Mo & Anand Charvin Gopalakrishnan  | #
########################################################################
# Set the maximum and minimum threshold for each parameter
power_plants_threshold = 10
power_plants_max_threshold = 10
heavy_industries_threshold = 5
heavy_industries_max_threshold = 5
high_risk_areas_threshold = 2
high_risk_areas_max_threshold = 2
rivers_streams_threshold = 1
rivers_streams_max_threshold = 1
heavy_traffic_threshold = 0.5
heavy_traffic_max_threshold = 0.5

# Set the maximum and minimum threshold for selecting the locations
max_threshold = 100
min_threshold = 0

# Process the input data
selected_locations = []
for location in locations:
    x = location[0]
    y = location[1]
    # Calculate the suitability value of the location
    suitability_value = calculate_suitability_value(location, power_plants_threshold, power_plants_max_threshold, heavy_industries_threshold, heavy_industries_max_threshold, high_risk_areas_threshold, high_risk_areas_max_threshold, rivers_streams_threshold, rivers_streams_max_threshold, heavy_traffic_threshold, heavy_traffic_max_threshold)

    # Add the location and its suitability value to the list of selected locations
    selected_locations.append([x, y, round(suitability_value,2)])


#######################################################################################################
# Output Printing  # | Output printing using Python Tkinter Module   - Anand Charvin Gopalakrishnan | #
#######################################################################################################
window = Tk()
# Define the print_output function
def print_output(locations, power_plants_threshold, power_plants_max_threshold, heavy_industries_threshold, heavy_industries_max_threshold, high_risk_areas_threshold, high_risk_areas_max_threshold, rivers_streams_threshold, rivers_streams_max_threshold, heavy_traffic_threshold, heavy_traffic_max_threshold):
    # Create a Tkinter window

    window.title("Suitability Calculations")
    window.geometry("1024x400")

    # Create a frame to hold the table
    frame = Frame(window)
    frame.pack()

    # Create the table headers
    for col in ["Longitude", "Latitude", "Power Plants", "Heavy Industry", "High Risk", "Water Bodies", "Heavy Traffic", "Suitability","Suitability Message"]:
        Label(frame, text=col, font="Courier 11", relief=SUNKEN, width=15, wraplength=100, justify=CENTER).grid(row=0, column=["Longitude", "Latitude", "Power Plants", "Heavy Industry", "High Risk", "Water Bodies", "Heavy Traffic", "Suitability", "Suitability Message"].index(col))

            # Create the table rows
    for row in range(len(locations)):
        location = locations[row]
        suitability_value = calculate_suitability_value(location, power_plants_threshold, power_plants_max_threshold, heavy_industries_threshold, heavy_industries_max_threshold, high_risk_areas_threshold, high_risk_areas_max_threshold, rivers_streams_threshold, rivers_streams_max_threshold, heavy_traffic_threshold, heavy_traffic_max_threshold)
        suitability_message = calculate_suitability_message(suitability_value)
        Label(frame, text=location[0], font="Courier 11", relief=SUNKEN, width=15,wraplength=100).grid(row=row+1, column=0)
        Label(frame, text=location[1], font="Courier 11", relief=SUNKEN, width=15,wraplength=100, justify=CENTER).grid(row=row+1, column=1)
        Label(frame, text=location[2], font="Courier 11", relief=SUNKEN, width=15,wraplength=100, justify=CENTER).grid(row=row+1, column=2)
        Label(frame, text=location[3], font="Courier 11", relief=SUNKEN, width=15,wraplength=100, justify=CENTER).grid(row=row+1, column=3)
        Label(frame, text=location[4], font="Courier 11", relief=SUNKEN, width=15,wraplength=100, justify=CENTER).grid(row=row+1, column=4)
        Label(frame, text=location[5], font="Courier 11", relief=SUNKEN, width=15,wraplength=100, justify=CENTER).grid(row=row+1, column=5)
        Label(frame, text=location[6], font="Courier 11", relief=SUNKEN, width=15,wraplength=100, justify=CENTER).grid(row=row+1, column=6)
        Label(frame, text=suitability_value, font="Courier 11", relief=SUNKEN, width=15,wraplength=100, justify=CENTER).grid(row=row+1, column=7)
        Label(frame, text=suitability_message, font="Courier 11", relief=SUNKEN, width=15,wraplength=100, justify=CENTER).grid(row=row+1, column=8)


# Call the print_output function
print_output(locations, power_plants_threshold, power_plants_max_threshold, heavy_industries_threshold, heavy_industries_max_threshold, high_risk_areas_threshold, high_risk_areas_max_threshold, rivers_streams_threshold, rivers_streams_max_threshold, heavy_traffic_threshold, heavy_traffic_max_threshold)

# Export the results to a CSV file
######################################################
# | Out put as CSV Export   - Meet Hitendra Naik |   #
######################################################

with open("locations.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Longitude", "Latitude", "Power Plants", "Heavy Industries", "High Risk Areas", "Rivers/Streams", "Heavy Traffic", "Suitability"])
    for location in locations:
        suitability_value = calculate_suitability_value(location, power_plants_threshold, power_plants_max_threshold, heavy_industries_threshold, heavy_industries_max_threshold, high_risk_areas_threshold, high_risk_areas_max_threshold, rivers_streams_threshold, rivers_streams_max_threshold, heavy_traffic_threshold, heavy_traffic_max_threshold)
        writer.writerow([location[0], location[1], location[2], location[3], location[4], location[5], location[6], round(suitability_value,2)])


# Start the main event loop
window.mainloop()

######################################################
# ARC PY Section # | ARC PY Section  - Mingxuan Su   #
######################################################

def Model():  

    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = True

    # Call the ask_folder function and save the returned value
    workingdir = str(input("Please enter the folder location of the workspace here:\n"))
    
    Suitability_gdb = os.path.join(workingdir, "suitability.gdb")
    FullPath = Suitability_gdb

    locations_csv = os.path.join(os.getcwd(), "locations.csv")
    Symbology_lyrx = os.path.join(os.getcwd(), "Symbology.lyrx")

    # Process: XY Table To Point (XY Table To Point) (management)
    locations_XYTableToPoint =  FullPath + "\locations_XYTableToPoint"
    arcpy.management.XYTableToPoint(in_table=locations_csv, out_feature_class=locations_XYTableToPoint, x_field="Longitude", y_field="Latitude", z_field="", coordinate_system="GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119521E-09;0.001;0.001;IsHighPrecision")

    # Process: Buffer (Buffer) (analysis)
    locations_XYTableToPo_Buffer = FullPath + "\locations_XYTableToPo_Buffer"
    arcpy.analysis.Buffer(in_features=locations_XYTableToPoint, out_feature_class=locations_XYTableToPo_Buffer, buffer_distance_or_field="Power_Plants", line_side="FULL", line_end_type="ROUND", dissolve_option="NONE", dissolve_field=[], method="PLANAR")

    # Process: Buffer (2) (Buffer) (analysis)
    locations_XYTableToPo_Buffer1 = FullPath + "\locations_XYTableToPo_Buffer1"
    arcpy.analysis.Buffer(in_features=locations_XYTableToPo_Buffer, out_feature_class=locations_XYTableToPo_Buffer1, buffer_distance_or_field="Heavy_Industries", line_side="FULL", line_end_type="ROUND", dissolve_option="NONE", dissolve_field=[], method="PLANAR")

    # Process: Buffer (3) (Buffer) (analysis)
    locations_XYTableToPo_Buffer2 = FullPath + "\locations_XYTableToPo_Buffer2"
    arcpy.analysis.Buffer(in_features=locations_XYTableToPo_Buffer1, out_feature_class=locations_XYTableToPo_Buffer2, buffer_distance_or_field="High_Risk_Areas", line_side="FULL", line_end_type="ROUND", dissolve_option="NONE", dissolve_field=[], method="PLANAR")

    # Process: Buffer (5) (Buffer) (analysis)
    locations_XYTableToPo_Buffer3 = FullPath + "\locations_XYTableToPo_Buffer3"
    arcpy.analysis.Buffer(in_features=locations_XYTableToPo_Buffer2, out_feature_class=locations_XYTableToPo_Buffer3, buffer_distance_or_field="Rivers_Streams", line_side="FULL", line_end_type="ROUND", dissolve_option="NONE", dissolve_field=[], method="PLANAR")

    # Process: Buffer (4) (Buffer) (analysis)
    locations_XYTableToPo_Buffer4 = FullPath + "\locations_XYTableToPo_Buffer4"
    arcpy.analysis.Buffer(in_features=locations_XYTableToPo_Buffer3, out_feature_class=locations_XYTableToPo_Buffer4, buffer_distance_or_field="Heavy_Traffic", line_side="FULL", line_end_type="ROUND", dissolve_option="NONE", dissolve_field=[], method="PLANAR")

    # Process: Merge (Merge) (management)
    Buffer_Merge = FullPath + "\Buffer_Merge"
    arcpy.management.Merge(inputs=[locations_XYTableToPo_Buffer4, locations_XYTableToPo_Buffer3, locations_XYTableToPo_Buffer2, locations_XYTableToPo_Buffer1, locations_XYTableToPo_Buffer], output=Buffer_Merge, field_mappings="Longitude \"Longitude\" true true false 8 Double 0 0,First,#,ModelBuilder\\locations_XYTableToPo_Buffer4:locations_XYTableToPo_Buffer4,Longitude,-1,-1,ModelBuilder\\locations_XYTableToPo_Buffer3:locations_XYTableToPo_Buffer3,Longitude,-1,-1,ModelBuilder\\locations_XYTableToPo_Buffer2:locations_XYTableToPo_Buffer2,Longitude,-1,-1,ModelBuilder\\locations_XYTableToPo_Buffer1:locations_XYTableToPo_Buffer1,Longitude,-1,-1,ModelBuilder\\locations_XYTableToPo_Buffer:locations_XYTableToPo_Buffer,Longitude,-1,-1;Latitude \"Latitude\" true true false 8 Double 0 0,First,#,ModelBuilder\\locations_XYTableToPo_Buffer4:locations_XYTableToPo_Buffer4,Latitude,-1,-1,ModelBuilder\\locations_XYTableToPo_Buffer3:locations_XYTableToPo_Buffer3,Latitude,-1,-1,ModelBuilder\\locations_XYTableToPo_Buffer2:locations_XYTableToPo_Buffer2,Latitude,-1,-1,ModelBuilder\\locations_XYTableToPo_Buffer1:locations_XYTableToPo_Buffer1,Latitude,-1,-1,ModelBuilder\\locations_XYTableToPo_Buffer:locations_XYTableToPo_Buffer,Latitude,-1,-1;Power_Plants \"Power Plants\" true true false 8 Double 0 0,First,#,ModelBuilder\\locations_XYTableToPo_Buffer4:locations_XYTableToPo_Buffer4,Power_Plants,-1,-1,ModelBuilder\\locations_XYTableToPo_Buffer3:locations_XYTableToPo_Buffer3,Power_Plants,-1,-1,ModelBuilder\\locations_XYTableToPo_Buffer2:locations_XYTableToPo_Buffer2,Power_Plants,-1,-1,ModelBuilder\\locations_XYTableToPo_Buffer1:locations_XYTableToPo_Buffer1,Power_Plants,-1,-1,ModelBuilder\\locations_XYTableToPo_Buffer:locations_XYTableToPo_Buffer,Power_Plants,-1,-1;Heavy_Industries \"Heavy Industries\" true true false 8 Double 0 0,First,#,ModelBuilder\\locations_XYTableToPo_Buffer4:locations_XYTableToPo_Buffer4,Heavy_Industries,-1,-1,ModelBuilder\\locations_XYTableToPo_Buffer3:locations_XYTableToPo_Buffer3,Heavy_Industries,-1,-1,ModelBuilder\\locations_XYTableToPo_Buffer2:locations_XYTableToPo_Buffer2,Heavy_Industries,-1,-1,ModelBuilder\\locations_XYTableToPo_Buffer1:locations_XYTableToPo_Buffer1,Heavy_Industries,-1,-1,ModelBuilder\\locations_XYTableToPo_Buffer:locations_XYTableToPo_Buffer,Heavy_Industries,-1,-1;High_Risk_Areas \"High Risk Areas\" true true false 8 Double 0 0,First,#,ModelBuilder\\locations_XYTableToPo_Buffer4:locations_XYTableToPo_Buffer4,High_Risk_Areas,-1,-1,ModelBuilder\\locations_XYTableToPo_Buffer3:locations_XYTableToPo_Buffer3,High_Risk_Areas,-1,-1,ModelBuilder\\locations_XYTableToPo_Buffer2:locations_XYTableToPo_Buffer2,High_Risk_Areas,-1,-1,ModelBuilder\\locations_XYTableToPo_Buffer1:locations_XYTableToPo_Buffer1,High_Risk_Areas,-1,-1,ModelBuilder\\locations_XYTableToPo_Buffer:locations_XYTableToPo_Buffer,High_Risk_Areas,-1,-1;Rivers_Streams \"Rivers/Streams\" true true false 8 Double 0 0,First,#,ModelBuilder\\locations_XYTableToPo_Buffer4:locations_XYTableToPo_Buffer4,Rivers_Streams,-1,-1,ModelBuilder\\locations_XYTableToPo_Buffer3:locations_XYTableToPo_Buffer3,Rivers_Streams,-1,-1,ModelBuilder\\locations_XYTableToPo_Buffer2:locations_XYTableToPo_Buffer2,Rivers_Streams,-1,-1,ModelBuilder\\locations_XYTableToPo_Buffer1:locations_XYTableToPo_Buffer1,Rivers_Streams,-1,-1,ModelBuilder\\locations_XYTableToPo_Buffer:locations_XYTableToPo_Buffer,Rivers_Streams,-1,-1;Heavy_Traffic \"Heavy Traffic\" true true false 8 Double 0 0,First,#,ModelBuilder\\locations_XYTableToPo_Buffer4:locations_XYTableToPo_Buffer4,Heavy_Traffic,-1,-1,ModelBuilder\\locations_XYTableToPo_Buffer3:locations_XYTableToPo_Buffer3,Heavy_Traffic,-1,-1,ModelBuilder\\locations_XYTableToPo_Buffer2:locations_XYTableToPo_Buffer2,Heavy_Traffic,-1,-1,ModelBuilder\\locations_XYTableToPo_Buffer1:locations_XYTableToPo_Buffer1,Heavy_Traffic,-1,-1,ModelBuilder\\locations_XYTableToPo_Buffer:locations_XYTableToPo_Buffer,Heavy_Traffic,-1,-1;Suitability \"Suitability\" true true false 4 Long 0 0,First,#,ModelBuilder\\locations_XYTableToPo_Buffer4:locations_XYTableToPo_Buffer4,Suitability,-1,-1,ModelBuilder\\locations_XYTableToPo_Buffer3:locations_XYTableToPo_Buffer3,Suitability,-1,-1,ModelBuilder\\locations_XYTableToPo_Buffer2:locations_XYTableToPo_Buffer2,Suitability,-1,-1,ModelBuilder\\locations_XYTableToPo_Buffer1:locations_XYTableToPo_Buffer1,Suitability,-1,-1,ModelBuilder\\locations_XYTableToPo_Buffer:locations_XYTableToPo_Buffer,Suitability,-1,-1;BUFF_DIST \"BUFF_DIST\" true true false 8 Double 0 0,First,#,ModelBuilder\\locations_XYTableToPo_Buffer4:locations_XYTableToPo_Buffer4,BUFF_DIST,-1,-1,ModelBuilder\\locations_XYTableToPo_Buffer3:locations_XYTableToPo_Buffer3,BUFF_DIST,-1,-1,ModelBuilder\\locations_XYTableToPo_Buffer2:locations_XYTableToPo_Buffer2,BUFF_DIST,-1,-1,ModelBuilder\\locations_XYTableToPo_Buffer1:locations_XYTableToPo_Buffer1,BUFF_DIST,-1,-1,ModelBuilder\\locations_XYTableToPo_Buffer:locations_XYTableToPo_Buffer,BUFF_DIST,-1,-1;ORIG_FID \"ORIG_FID\" true true false 4 Long 0 0,First,#,ModelBuilder\\locations_XYTableToPo_Buffer4:locations_XYTableToPo_Buffer4,ORIG_FID,-1,-1,ModelBuilder\\locations_XYTableToPo_Buffer3:locations_XYTableToPo_Buffer3,ORIG_FID,-1,-1,ModelBuilder\\locations_XYTableToPo_Buffer2:locations_XYTableToPo_Buffer2,ORIG_FID,-1,-1,ModelBuilder\\locations_XYTableToPo_Buffer1:locations_XYTableToPo_Buffer1,ORIG_FID,-1,-1,ModelBuilder\\locations_XYTableToPo_Buffer:locations_XYTableToPo_Buffer,ORIG_FID,-1,-1;Shape_Length \"Shape_Length\" false true true 8 Double 0 0,First,#,ModelBuilder\\locations_XYTableToPo_Buffer4:locations_XYTableToPo_Buffer4,Shape_Length,-1,-1,ModelBuilder\\locations_XYTableToPo_Buffer3:locations_XYTableToPo_Buffer3,Shape_Length,-1,-1,ModelBuilder\\locations_XYTableToPo_Buffer2:locations_XYTableToPo_Buffer2,Shape_Length,-1,-1,ModelBuilder\\locations_XYTableToPo_Buffer1:locations_XYTableToPo_Buffer1,Shape_Length,-1,-1,ModelBuilder\\locations_XYTableToPo_Buffer:locations_XYTableToPo_Buffer,Shape_Length,-1,-1;Shape_Area \"Shape_Area\" false true true 8 Double 0 0,First,#,ModelBuilder\\locations_XYTableToPo_Buffer4:locations_XYTableToPo_Buffer4,Shape_Area,-1,-1,ModelBuilder\\locations_XYTableToPo_Buffer3:locations_XYTableToPo_Buffer3,Shape_Area,-1,-1,ModelBuilder\\locations_XYTableToPo_Buffer2:locations_XYTableToPo_Buffer2,Shape_Area,-1,-1,ModelBuilder\\locations_XYTableToPo_Buffer1:locations_XYTableToPo_Buffer1,Shape_Area,-1,-1,ModelBuilder\\locations_XYTableToPo_Buffer:locations_XYTableToPo_Buffer,Shape_Area,-1,-1", add_source="NO_SOURCE_INFO")

    # Process: Apply Symbology From Layer (Apply Symbology From Layer) (management)
    Buffer_Merge_Layer3 = arcpy.management.ApplySymbologyFromLayer(in_layer=Buffer_Merge, in_symbology_layer=Symbology_lyrx, symbology_fields=[["VALUE_FIELD", "BUFF_DIST", "BUFF_DIST"]], update_symbology="UPDATE")[0]

    # Process: Match Layer Symbology To A Style (Match Layer Symbology To A Style) (management)
    Output_Layer = arcpy.management.MatchLayerSymbologyToAStyle(in_layer=Buffer_Merge_Layer3, match_values="$feature.BUFF_DIST", in_style="ColorBrewer Schemes (RGB)")[0]

    return Output_Layer

if __name__ == '__main__':
    # Global Environment settings
    with arcpy.EnvManager(scratchWorkspace=r"FullPath", workspace=r"FullPath"):
        Model(*argv[1:])
