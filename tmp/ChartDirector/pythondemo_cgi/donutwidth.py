#!/usr/bin/python
from pychartdir import *
import cgi, sys

# Get HTTP query parameters
query = cgi.FieldStorage()

# This script can draw different charts depending on the chartIndex
chartIndex = int(query["img"].value)

# Determine the donut inner radius (as percentage of outer radius) based on input parameter
donutRadius = chartIndex * 25

# The data for the pie chart
data = [10, 10, 10, 10, 10]

# The labels for the pie chart
labels = ["Marble", "Wood", "Granite", "Plastic", "Metal"]

# Create a PieChart object of size 150 x 120 pixels, with a grey (EEEEEE) background, black border
# and 1 pixel 3D border effect
c = PieChart(150, 120, 0xeeeeee, 0x000000, 1)

# Set donut center at (75, 65) and the outer radius to 50 pixels. Inner radius is computed according
# donutWidth
c.setDonutSize(75, 60, 50, int(50 * donutRadius / 100))

# Add a title to show the donut width
c.addTitle("Inner Radius = %s %%" % (donutRadius), "arial.ttf", 10).setBackground(0xcccccc, 0)

# Draw the pie in 3D
c.set3D(12)

# Set the pie data and the pie labels
c.setData(data, labels)

# Disable the sector labels by setting the color to Transparent
c.setLabelStyle("", 8, Transparent)

# Output the chart
print("Content-type: image/png\n")
binaryPrint(c.makeChart2(PNG))

