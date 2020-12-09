#!/usr/bin/python
import yaml
from FinanceChart import *
from pychartdir import *
from datetime import date, timedelta

setLicenseCode("DEVP-2LTF-FD2N-G76T-2691-3A31")

conf = yaml.safe_load(open('../config/settings.yaml'))

# *************** Settings for candlestick chart
IMAGE_WIDTH = conf['CHARTER_CANDLE_CHART']['IMAGE_WIDTH']
IMAGE_HEIGHT = conf['CHARTER_CANDLE_CHART']['IMAGE_HEIGHT']
TITLE_FONT_COLOR = conf['CHARTER_CANDLE_CHART']['TITLE_FONT_COLOR']
EXTRA_DAYS = conf['CHARTER_CANDLE_CHART']['EXTRA_DAYS']
AXIS_FONT_COLOR = conf['CHARTER_CANDLE_CHART']['AXIS_FONT_COLOR']
CHART_BACKGROUND_COLOR = conf['CHARTER_CANDLE_CHART']['CHART_BACKGROUND_COLOR']
OUTER_BACKGROUND_COLOR = conf['CHARTER_CANDLE_CHART']['OUTER_BACKGROUND_COLOR']
GRID_LINE_COLOR = conf['CHARTER_CANDLE_CHART']['GRID_LINE_COLOR']
WATERMARK_TEXT_COLOR = conf['CHARTER_CANDLE_CHART']['WATERMARK_TEXT_COLOR']
CANDLE_UP_COLOR = conf['CHARTER_CANDLE_CHART']['CANDLE_UP_COLOR']
CANDLE_DOWN_COLOR = conf['CHARTER_CANDLE_CHART']['CANDLE_DOWN_COLOR']
CANDLE_SHADOW_COLOR = conf['CHARTER_CANDLE_CHART']['CANDLE_SHADOW_COLOR']
COMPARISON_LINE_COLOR = conf['CHARTER_CANDLE_CHART']['COMPARISON_LINE_COLOR']

# *************** Settings for histogram chart
H_IMAGE_WIDTH = conf['CHARTER_HISTOGRAM']['IMAGE_WIDTH']
H_IMAGE_HEIGHT = conf['CHARTER_HISTOGRAM']['IMAGE_HEIGHT']
H_AXIS_FONT_COLOR = conf['CHARTER_HISTOGRAM']['AXIS_FONT_COLOR']
H_TITLE_FONT_COLOR = conf['CHARTER_HISTOGRAM']['TITLE_FONT_COLOR']
H_WATERMARK_TEXT_COLOR = conf['CHARTER_HISTOGRAM']['WATERMARK_TEXT_COLOR']
BAR_UP_COLOR = conf['CHARTER_HISTOGRAM']['BAR_UP_COLOR']
BAR_DOWN_COLOR = conf['CHARTER_HISTOGRAM']['BAR_DOWN_COLOR']
HIST_BACKGROUND_COLOR = conf['CHARTER_HISTOGRAM']['HIST_BACKGROUND_COLOR']


def create_chart(ticker, data, compare_ticker=None, compare_data=None):
    extra_days = EXTRA_DAYS

    time_stamps = []
    high_data = []
    low_data = []
    open_data = []
    close_data = []
    volume_data = []

    for quote in data:
        dt = date.fromisoformat(str(quote[0]))
        time_stamps.append(chartTime(dt.year, dt.month, dt.day))
        open_data.append(float(quote[1]))
        high_data.append(float(quote[2]))
        low_data.append(float(quote[3]))
        close_data.append(float(quote[4]))

    compare_close_data = []
    for cquote in compare_data:
        compare_close_data.append(float(cquote[4]))

    i = 0
    td = timedelta(1)
    while i < extra_days:
        dt = dt + td
        time_stamps.append(chartTime(dt.year, dt.month, dt.day))
        compare_close_data.append(NoValue)
        i += 1

    m = FinanceChart(IMAGE_WIDTH)

    m.setData(timeStamps=time_stamps, highData=high_data, lowData=low_data, openData=open_data, closeData=close_data,
              volData=volume_data, extraPoints=extra_days)

    title_str = "Portfolio vs " + compare_ticker
    m.addPlotAreaTitle(Center, "<*font=arial.ttf,size=12,color=0x5fffffff*>%s" % title_str)

    m.setLegendStyle("normal", 8, Transparent, 0xC4D6FF)
    m.setXAxisStyle("normal", 8, AXIS_FONT_COLOR, 0)
    m.setYAxisStyle("normal", 8, AXIS_FONT_COLOR, 0)

    # m.setMargins(leftMargin=20, topMargin=7, rightMargin=35, bottomMargin=25)
    m.setPlotAreaStyle(bgColor=CHART_BACKGROUND_COLOR,
                       majorHGridColor=GRID_LINE_COLOR,
                       majorVGridColor=GRID_LINE_COLOR,
                       minorHGridColor=GRID_LINE_COLOR,
                       minorVGridColor=GRID_LINE_COLOR)
    m.setPlotAreaBorder(Transparent, 0)
    m.addText(130, 130, "(c) @UpsilonBot", "arialbd.ttf", 32, WATERMARK_TEXT_COLOR)

    main_chart = m.addMainChart(IMAGE_HEIGHT)

    m.setPercentageAxis()
    # main_chart.setClipping(True)
    main_chart.setBackground(OUTER_BACKGROUND_COLOR)

    csl = m.addCandleStick(-1, -1)
    csl.getDataSet(0).setDataColor(CANDLE_UP_COLOR, CANDLE_SHADOW_COLOR)
    csl.getDataSet(1).setDataColor(CANDLE_DOWN_COLOR, CANDLE_SHADOW_COLOR)

    m.addComparison(compare_close_data, COMPARISON_LINE_COLOR, compare_ticker)

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
            colors.append(BAR_UP_COLOR)
        else:
            colors.append(BAR_DOWN_COLOR)
        i += 1
    excess_chart = XYChart(H_IMAGE_WIDTH, H_IMAGE_HEIGHT, HIST_BACKGROUND_COLOR)
    excess_chart.setYAxisOnRight(True)
    excess_chart.xAxis().setLabelStyle("normal", 8, H_AXIS_FONT_COLOR, 0)
    excess_chart.yAxis().setLabelStyle("normal", 8, H_AXIS_FONT_COLOR, 0)
    excess_chart.yAxis().setLabelFormat("{value}%")
    excess_chart.setPlotArea(0, 25, 605, 205, Transparent, -1, Transparent, 0xcccccc)
    title_str = "Monthly Portfolio Excess Returns over " + compare_ticker
    excess_chart.addTitle(title_str, "arial.ttf", 10, H_TITLE_FONT_COLOR)
    excess_chart.addText(100, 100, "(c) @UpsilonBot", "arialbd.ttf", 32, H_WATERMARK_TEXT_COLOR)
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

