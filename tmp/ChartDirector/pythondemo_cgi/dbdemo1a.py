#!/usr/bin/python
from pychartdir import *
import cgi, sys

# Get HTTP query parameters
query = cgi.FieldStorage()

#
# Displays the monthly revenue for the selected year. The selected year should be passed in as a
# query parameter called "year"
#
try :
    selectedYear = int(query["year"].value)
except :
    selectedYear = 2005

#
# Query the database to get monthly reveunes for software, hardware and services for
# the year. In this demo, we will use random numbers instead of a real database.
#
rantable = RanTable(selectedYear, 3, 12)
rantable.setCol(0, 30 * (selectedYear - 1990),  80 * (selectedYear - 1990))
rantable.setCol(1, 30 * (selectedYear - 1990),  80 * (selectedYear - 1990))
rantable.setCol(2, 30 * (selectedYear - 1990),  80 * (selectedYear - 1990))

software = rantable.getCol(0)
hardware = rantable.getCol(1)
services = rantable.getCol(2)

#
# Now we have read data into arrays, we can draw the chart using ChartDirector
#

# Create a XYChart object of size 600 x 300 pixels, with a light grey (eeeeee) background, black
# border, 1 pixel 3D border effect and rounded corners.
c = XYChart(600, 300, 0xeeeeee, 0x000000, 1)
c.setRoundedFrame()

# Set the plotarea at (60, 60) and of size 520 x 200 pixels. Set background color to white (ffffff)
# and border and grid colors to grey (cccccc)
c.setPlotArea(60, 60, 520, 200, 0xffffff, -1, 0xcccccc, 0xccccccc)

# Add a title to the chart using 15pt Times Bold Italic font, with a light blue (ccccff) background
# and with glass lighting effects.
c.addTitle("Global Revenue for Year %s" % (selectedYear), "timesbi.ttf", 15).setBackground(0xccccff,
    0x000000, glassEffect())

# Add a legend box at (70, 32) (top of the plotarea) with 9pt Arial Bold font
c.addLegend(70, 32, 0, "arialbd.ttf", 9).setBackground(Transparent)

# Add a stacked bar chart layer using the supplied data
layer = c.addBarLayer2(Stack)
layer.addDataSet(software, 0xff0000, "Software")
layer.addDataSet(hardware, 0x00ff00, "Hardware")
layer.addDataSet(services, 0xffaa00, "Services")

# Use soft lighting effect with light direction from the left
layer.setBorderColor(Transparent, softLighting(Left))

# Set the x axis labels. In this example, the labels must be Jan - Dec.
labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sept", "Oct", "Nov", "Dec"]
c.xAxis().setLabels(labels)

# Draw the ticks between label positions (instead of at label positions)
c.xAxis().setTickOffset(0.5)

# Set the y axis title
c.yAxis().setTitle("USD (Millions)")

# Set axes width to 2 pixels
c.xAxis().setWidth(2)
c.yAxis().setWidth(2)

# Output the chart in PNG format
print("Content-type: image/png\n")
binaryPrint(c.makeChart2(PNG))

