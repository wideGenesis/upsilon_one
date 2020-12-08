#!/usr/bin/python
from FinanceChart import *
from pychartdir import *
from datetime import date, timedelta

setLicenseCode("DEVP-2LTF-FD2N-G76T-2691-3A31")


def create_chart(ticker, data, compare_ticker=None, compare_data=None):
    extraDays = 5

    timeStamps = []
    highData = []
    lowData = []
    openData = []
    closeData = []
    volData = []

    for quote in data:
        dt = date.fromisoformat(str(quote[0]))
        timeStamps.append(chartTime(dt.year, dt.month, dt.day))
        openData.append(float(quote[1]))
        highData.append(float(quote[2]))
        lowData.append(float(quote[3]))
        closeData.append(float(quote[4]))

    compare_close_data = []
    compare_dt = None
    for cquote in compare_data:
        compare_dt = date.fromisoformat(str(cquote[0]))
        compare_close_data.append(float(cquote[4]))

    i = 0
    td = timedelta(1)
    while i < extraDays:
        dt = dt + td
        timeStamps.append(chartTime(dt.year, dt.month, dt.day))
        compare_close_data.append(NoValue)
        i += 1

    m = FinanceChart(640)

    m.setData(timeStamps=timeStamps, highData=highData, lowData=lowData, openData=openData, closeData=closeData,
              volData=volData, extraPoints=extraDays)

    title_str = "Portfolio vs " + compare_ticker
    m.addPlotAreaTitle(Center, "<*font=arial.ttf,size=12,color=0x5fffffff*>%s" % title_str)

    m.setLegendStyle("normal", 8, Transparent, 0xC4D6FF)
    m.setXAxisStyle("normal", 8, 0x5fFFFFFF, 0)
    m.setYAxisStyle("normal", 8, 0x5fFFFFFF, 0)

    m.setMargins(leftMargin=20, topMargin=7, rightMargin=35, bottomMargin=25)
    m.setPlotAreaStyle(bgColor=0x000000, majorHGridColor=0xcdd9d9d9, majorVGridColor=0xcdd9d9d9,
                       minorHGridColor=0xcdd9d9d9, minorVGridColor=0xcdd9d9d9)
    m.setPlotAreaBorder(Transparent, 0)
    m.addText(130, 130, "(c) @UpsilonBot", "arialbd.ttf", 32, 0xf1d9d9d9)

    main_chart = m.addMainChart(320)

    m.setPercentageAxis()
    # main_chart.setClipping(True)
    main_chart.setBackground(0x000000)

    csl = m.addCandleStick(-1, -1)
    csl.getDataSet(0).setDataColor(0x38761D, 0x9eB5B5B8)
    csl.getDataSet(1).setDataColor(0xff0000, 0x9eB5B5B8)

    m.addComparison(compare_close_data, 0xff7f27, compare_ticker)

    filename = "port_chart_over_" + compare_ticker + ".png"
    m.makeChart(filename)


def create_excess_histogram(ticker, data, compare_ticker, compare_data):
    labels = []
    bars1 = []
    bars2 = []
    dt = None
    pdt = None
    month_open = None
    month_close = None
    for quote in data:
        dt = date.fromisoformat(str(quote[0]))
        if pdt is None:
            pdt = dt
            month_open = float(quote[1])
            month_close = float(quote[4])
        else:
            if dt.month == pdt.month:
                month_close = float(quote[4])
                pdt = dt
            else:
                labels.append(pdt.strftime("%b %y"))
                sign = 0
                if (month_close - month_open) > 0.0:
                    sign = 1
                elif (month_close - month_open) < 0.0:
                    sign = -1
                if sign == 0:
                    bars1.append(0.0)
                else:
                    bars1.append(
                        round((int(abs(month_close - month_open) * 100) * 100) / int(month_open * 100), 2) * sign)
                month_open = float(quote[1])
                month_close = float(quote[4])
                pdt = dt

    print("Labels:" + str(labels))
    print("Bars1:" + str(bars1))

    compare_close_data = []
    compare_open_data = []
    compare_month_open = None
    compare_month_close = None
    compare_dt = None
    compare_pdt = None
    for cquote in compare_data:
        compare_dt = date.fromisoformat(str(cquote[0]))
        compare_open_data.append(float(cquote[1]))
        compare_close_data.append(float(cquote[4]))
        if compare_pdt is None:
            compare_pdt = compare_dt
            compare_month_open = float(cquote[1])
            compare_month_close = float(cquote[4])
        else:
            if compare_dt.month == compare_pdt.month:
                compare_month_close = float(cquote[4])
                compare_pdt = compare_dt
            else:
                sign = 0
                if (compare_month_close - compare_month_open) > 0.0:
                    sign = 1
                elif (compare_month_close - compare_month_open) < 0.0:
                    sign = -1
                if sign == 0:
                    bars2.append(0.0)
                else:
                    bars2.append(round((int(abs(compare_month_close - compare_month_open) * 100) * 100) / int(
                        compare_month_open * 100), 2) * sign)
                compare_month_open = float(cquote[1])
                compare_month_close = float(cquote[4])
                compare_pdt = compare_dt

    bars = []
    colors = []
    i = 0
    for bar in bars1:
        value = bar - bars2[i]
        bars.append(bar - bars2[i])
        if value >= 0:
            colors.append(0x38761D)
        else:
            colors.append(0xff0000)
        i += 1
    excess_chart = XYChart(640, 250, 0x000000)
    excess_chart.setYAxisOnRight(True)
    excess_chart.xAxis().setLabelStyle("normal", 8, 0x5fFFFFFF, 0)
    excess_chart.yAxis().setLabelStyle("normal", 8, 0x5fFFFFFF, 0)
    excess_chart.yAxis().setLabelFormat("{value}%")
    excess_chart.setRoundedFrame(0x000000, 20)
    excess_chart.setPlotArea(0, 25, 605, 205, Transparent, -1, Transparent, 0xcccccc)
    title_str = "Monthly Portfolio Excess Returns over " + compare_ticker
    excess_chart.addTitle(title_str, "arial.ttf", 10, 0x5fFFFFFF)
    excess_chart.addText(100, 100, "(c) @UpsilonBot", "arialbd.ttf", 32, 0xcdd9d9d9)
    bl = excess_chart.addBarLayer3(bars, colors)
    bl.setBorderColor(Transparent)
    bl.setBarShape(CircleShape)
    excess_chart.xAxis().setLabels(labels)

    filename = "port_excess_over_" + compare_ticker + ".png"
    excess_chart.makeChart(filename)


def color_2_int(red, green, blue, alpha):
    return ((255 - alpha) << 24) + (red << 16) + (green << 8) + blue


def color_2_chart_string(int_color):
    res = hex(int_color)
    return res

# QColor ATGOwnChartDialog::getInverseColor(QColor inColor) {
#     return ((255-inColor.alpha()) << 24)+((255-inColor.red()) << 16)+((255-inColor.green()) << 8) + (255-inColor.blue());
# }
