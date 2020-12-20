#!/usr/bin/python
from pychartdir import *
import cgi, sys

# Get HTTP query parameters
query = cgi.FieldStorage()


#
# In this demo, the generated web page needs to load the "cdjcv.js" Javascript file and several GIF
# files. For ease of installation, we put these files in the same directory as this script. However,
# if this script is installed in a CGI only directory (such as cgi-bin), the web server would not
# allow the browser to access these non-CGI files.
#
# To get around this potential issue, a special load resource script is used to load these files.
# Instead of using:
#
#    <SCRIPT SRC="cdjcv.js">
#
# we now use:
#
#    <SCRIPT SRC="loadresource.py?file=cdjcv.js">
#
# Similar methods are used to load the GIF files.
#
# If this script is not in a CGI only directory, you may replace the following loadResource string
# with an empty string "" to improve performance.
#
loadResource = "loadresource.py?file="

# Data for the chart as 2 random data series
r = RanSeries(127)
data0 = r.getSeries(180, 10, -1.5, 1.5)
data1 = r.getSeries(180, 150, -15, 15)
timeStamps = r.getDateSeries(180, chartTime(2011, 1, 1), 86400)

# Create a XYChart object of size 670 x 400 pixels
c = XYChart(670, 400)

# Add a title to the chart using 18pt Times New Roman Bold Italic font
c.addTitle("Plasma Stabilizer Energy Usage", "timesbi.ttf", 18)

# Set the plotarea at (50, 55) with width 100 pixels less than chart width, and height 90 pixels
# less than chart height. Use a vertical gradient from light blue (f0f6ff) to sky blue (a0c0ff) as
# background. Set border to transparent and grid lines to white (ffffff).
c.setPlotArea(50, 55, c.getWidth() - 100, c.getHeight() - 90, c.linearGradientColor(0, 55, 0,
    c.getHeight() - 35, 0xf0f6ff, 0xa0c0ff), -1, Transparent, 0xffffff, 0xffffff)

# Add a legend box at (50, 25) using horizontal layout. Use 10pt Arial Bold as font. Set the
# background and border color to Transparent.
c.addLegend(50, 25, 0, "arialbd.ttf", 10).setBackground(Transparent)

# Set axis label style to 8pt Arial Bold
c.xAxis().setLabelStyle("arialbd.ttf", 8)
c.yAxis().setLabelStyle("arialbd.ttf", 8)
c.yAxis2().setLabelStyle("arialbd.ttf", 8)

# Set the axis stem to transparent
c.xAxis().setColors(Transparent)
c.yAxis().setColors(Transparent)
c.yAxis2().setColors(Transparent)

# Configure x-axis label format
c.xAxis().setMultiFormat(StartOfYearFilter(), "{value|mm/yyyy} ", StartOfMonthFilter(), "{value|mm}"
    )

# Add axis title using 10pt Arial Bold Italic font
c.yAxis().setTitle("Power Usage (Watt)", "arialbi.ttf", 10)
c.yAxis2().setTitle("Effective Load (kg)", "arialbi.ttf", 10)

# Add a line layer to the chart using a line width of 2 pixels.
layer = c.addLineLayer2()
layer.setLineWidth(2)

# Add 2 data series to the line layer
layer.setXData(timeStamps)
layer.addDataSet(data0, 0xcc0000, "Power Usage")
layer.addDataSet(data1, 0x008800, "Effective Load").setUseYAxis2()

# Create the WebChartViewer object
viewer = WebChartViewer(query, "chart1")

# Output the chart
chartQuery = c.makeTmpFile("/tmp/tmpcharts")

# Set the chart URL to the viewer
viewer.setImageUrl("getchart.py?img=/tmp/tmpcharts/" + chartQuery)

# Output Javascript chart model to the browser to support tracking cursor
viewer.setChartModel(c.getJsChartModel())

print("Content-type: text/html\n")
print("""
<!DOCTYPE html>
<html>
<head>
    <title>Track Line with Axis Labels</title>
    <script type="text/javascript" src="%(loadResource)scdjcv.js"></script>
</head>
<body style="margin:5px 0px 0px 5px">
<script type="text/javascript">

//
// Use the window load event to set up the MouseMovePlotArea event handler
//
JsChartViewer.addEventListener(window, 'load', function() {
    var viewer = JsChartViewer.get('%(id)s');

    // Draw track cursor when mouse is moving over plotarea. Hide it when mouse leaves plot area.
    viewer.attachHandler(["MouseMovePlotArea", "TouchStartPlotArea", "TouchMovePlotArea", "ChartMove"],
    function(e) {
        this.preventDefault(e);   // Prevent the browser from using touch events for other actions
        trackLineAxis(viewer, viewer.getPlotAreaMouseX());
        viewer.setAutoHide("all", ["MouseOutPlotArea", "TouchEndPlotArea"]);
    });
});

//
// Draw track line with axis labels
//
function trackLineAxis(viewer, mouseX)
{
    // Remove all previously drawn tracking object
    viewer.hideObj("all");

    // The chart and its plot area
    var c = viewer.getChart();
    var plotArea = c.getPlotArea();

    // Get the data x-value that is nearest to the mouse, and find its pixel coordinate.
    var xValue = c.getNearestXValue(mouseX);
    var xCoor = c.getXCoor(xValue);

    // The vertical track line is drawn up to the highest data point (the point with smallest
    // y-coordinate). We need to iterate all datasets in all layers to determine where it is.
    var minY = plotArea.getBottomY();

    // Iterate through all layers to find the highest data point
    for (var i = 0; i < c.getLayerCount(); ++i)
    {
        var layer = c.getLayerByZ(i);

        // The data array index of the x-value
        var xIndex = layer.getXIndexOf(xValue);

        // Iterate through all the data sets in the layer
        for (var j = 0; j < layer.getDataSetCount(); ++j)
        {
            var dataSet = layer.getDataSetByZ(j);
            var yCoor = c.getYCoor(dataSet.getPosition(xIndex), dataSet.getUseYAxis());
            if ((yCoor != null) && (dataSet.getDataColor() != null))
                minY = Math.min(minY, yCoor);
        }
    }

    // Draw a vertical track line at the x-position up to the highest data point.
    viewer.drawVLine("trackLine", xCoor, Math.max(minY, plotArea.getTopY()),
        plotArea.getBottomY() + 3, "black 1px dotted");

    // Draw a label on the x-axis to show the track line position
    viewer.showTextBox("xAxisLabel", xCoor, plotArea.getBottomY() + 3, JsChartViewer.Top,
        c.xAxis().getFormattedLabel(xValue, "mmm dd, yyyy"),
        "font:bold 11px Arial;color:#FFFFFF;background-color:#000000;padding:2px 3px");

    // Iterate through all layers to draw the axis labels for the data points
    for (var i = 0; i < c.getLayerCount(); ++i)
    {
      var layer = c.getLayerByZ(i);

        // The data array index of the x-value
        var xIndex = layer.getXIndexOf(xValue);

        // Iterate through all the data sets in the layer
        for (var j = 0; j < layer.getDataSetCount(); ++j)
        {
            var dataSet = layer.getDataSetByZ(j);

            // The positional value, axis binding, pixel coordinate and color of the data point.
            var dataPoint = dataSet.getPosition(xIndex);
            var yAxis = dataSet.getUseYAxis();
            var yCoor = c.getYCoor(dataPoint, yAxis);
            var color = dataSet.getDataColor();

            // Draw the axis label only for visible data points of named data sets
            if ((yCoor != null) && (yCoor >= plotArea.getTopY()) && (yCoor <= plotArea.getBottomY()) &&
                (color != null))
            {
                // The axis label consists of 3 parts - a track dot for the data point, an axis label,
                // and a line joining the track dot to the axis label.

                // Draw the line first. The end point of the line at the axis label side depends on
                // whether the label is at the left or right side of the axis (that is, on whether
                // the axis is on the left or right side of the plot area).
                var xPos = yAxis.getX() + ((yAxis.getAlignment() == JsChartViewer.Left) ? -4 : 4);
                viewer.drawHLine("joinLine" + i + "_" + j, yCoor, xPos, xCoor, color + " 1px dotted");

                // Draw the axis label. If the axis is on the left side of the plot area, the labels
                // should right aligned to the axis, and vice versa.
                viewer.showTextBox("yAxisLabel" + i + "_" + j, xPos, yCoor,
                    (yAxis.getAlignment() == JsChartViewer.Left) ? JsChartViewer.Right : JsChartViewer.Left,
                    dataPoint.toPrecision(4), "padding:2px 3px;font:bold 11px Arial;background-color:" +
                    color + ";color:#FFFFFF;-webkit-text-size-adjust:100%%;");

                // Draw the track dot
                viewer.showTextBox("dataPoint" + i + "_" + j, xCoor, yCoor, JsChartViewer.Center,
                    viewer.htmlRect(7, 7, color));
            }
        }
    }
}

</script>
<div style="font-size:18pt; font-family:verdana; font-weight:bold">
    Track Line with Axis Labels
</div>
<hr style="border:solid 1px #000080" />
<div style="font-size:10pt; font-family:verdana; margin-bottom:1.5em">
    <a href="viewsource.py?file=%(SCRIPT_NAME)s">View Source Code</a>
</div>
<!-- ****** Here is the chart image ****** -->
%(chartImg)s
</body>
</html>
""" % {
    "loadResource" : loadResource,
    "id" : viewer.getId(),
    "SCRIPT_NAME" : os.environ["SCRIPT_NAME"],
    "chartImg" : viewer.renderHTML()
    })
