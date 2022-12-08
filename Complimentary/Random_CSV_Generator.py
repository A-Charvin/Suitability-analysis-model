# Program name: Random_CSV_Generator.py
# Input CSV FILE generator - Complimentary accessory for the Suitability calculator
# Made by Anand Charvin Gopalakrishnan
# Suitability analysis model | Section 61 Group 05
# Anand Charvin Gopalakrishnan, Andy Mo, Meet Hitendra Naik, Ming Xuan Su

# Import the necessary modules
import csv
import random

# Set the number of records to generate
num_locations = 20

# Open the output file for writing
with open("input.csv", "w", newline="") as output_file:
    # Create a CSV writer
    writer = csv.writer(output_file)
    
    # Write the header row
    writer.writerow(["X", "Y", "Power Plants Distance (km)", "Heavy Industries Distance (km)", "High Risk Areas Distance (km)", "Rivers and Streams Distance (km)", "Heavy Traffic Distance (km)"])
    
    # Generate the input data for the locations
    for i in range(num_locations):
        # Generate random X and Y coordinates
        x = random.uniform(-180, 180)
        y = random.uniform(-90, 90)
        
        # Generate random values for the distance from power plants, heavy industries, high risk areas, rivers and streams, and heavy traffic
        power_plants_distance = random.uniform(0, 100)
        heavy_industries_distance = random.uniform(0, 100)
        high_risk_areas_distance = random.uniform(0, 100)
        rivers_streams_distance = random.uniform(0, 100)
        heavy_traffic_distance = random.uniform(0, 100)
        
        # Write the location data to the CSV file
        writer.writerow([x, y, power_plants_distance, heavy_industries_distance, high_risk_areas_distance, rivers_streams_distance, heavy_traffic_distance])
