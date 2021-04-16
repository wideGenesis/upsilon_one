#!/usr/bin/python
import math

from FinanceChart import *
from pychartdir import *
from datetime import date, timedelta
from project_shared import *
from functools import reduce

setLicenseCode("DEVP-2LTF-FD2N-G76T-2691-3A31")


def create_chart(ticker, data, compare_ticker=None, compare_data=None, chart_type='Candlestic',
                 chart_path=CHARTER_IMAGES_PATH):
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
        open_data.append(float(quote[1])/100)
        high_data.append(float(quote[2])/100)
        low_data.append(float(quote[3])/100)
        close_data.append(float(quote[4])/100)

    compare_close_data = []
    for cquote in compare_data:
        compare_close_data.append(float(cquote[4])*100)

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

    title_ticker = ""
    for i, c in enumerate(ticker):
        title_ticker += c.upper() if i == 0 else c

    title_str = f'{title_ticker} portfolio vs {compare_ticker}'
    m.addPlotAreaTitle(Center, "<*font=arial.ttf,size=12,color=0x5fffffff*>%s" % title_str)

    # m.setLogScale(True)
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

    # m.setPercentageAxis()
    # main_chart.setClipping(True)
    main_chart.setBackground(OUTER_BACKGROUND_COLOR)

    if chart_type == 'Candlestic':
        csl = m.addCandleStick(-1, -1)
        csl.getDataSet(0).setDataColor(CANDLE_UP_COLOR, CANDLE_SHADOW_COLOR)
        csl.getDataSet(1).setDataColor(CANDLE_DOWN_COLOR, CANDLE_SHADOW_COLOR)
    elif chart_type == 'Bar':
        m.addHLOC(CANDLE_UP_COLOR, CANDLE_DOWN_COLOR)
    elif chart_type == 'Line':
        m.addCloseLine(CANDLE_UP_COLOR)

    m.addComparison(compare_close_data, COMPARISON_LINE_COLOR, compare_ticker)

    filename = f'{chart_path}/{ticker}_port_chart_over_{compare_ticker}.png'
    m.makeChart(filename)


def create_simple_chart(ticker, data, chart_type='Candlestic', chart_path=CHARTER_IMAGES_PATH):
    extra_days = EXTRA_DAYS

    time_stamps = []
    high_data = []
    low_data = []
    open_data = []
    close_data = []
    volume_data = []

    dt = date.today()
    for quote in data:
        dt = date.fromisoformat(str(quote[0]))
        time_stamps.append(chartTime(dt.year, dt.month, dt.day))
        open_data.append(float(quote[1]))
        high_data.append(float(quote[2]))
        low_data.append(float(quote[3]))
        close_data.append(float(quote[4]))

    i = 0
    td = timedelta(1)
    while i < extra_days:
        dt = dt + td
        time_stamps.append(chartTime(dt.year, dt.month, dt.day))
        i += 1

    m = FinanceChart(IMAGE_WIDTH)

    m.setData(timeStamps=time_stamps, highData=high_data, lowData=low_data, openData=open_data, closeData=close_data,
              volData=volume_data, extraPoints=extra_days)

    title_ticker = ""
    for i, c in enumerate(ticker):
        title_ticker += c.upper() if i == 0 else c

    title_str = f'{title_ticker}'
    m.addPlotAreaTitle(Center, "<*font=arial.ttf,size=12,color=0x5fffffff*>%s" % title_str)

    # m.setLogScale(True)
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

    if chart_type == 'Candlestic':
        csl = m.addCandleStick(-1, -1)
        csl.getDataSet(0).setDataColor(CANDLE_UP_COLOR, CANDLE_SHADOW_COLOR)
        csl.getDataSet(1).setDataColor(CANDLE_DOWN_COLOR, CANDLE_SHADOW_COLOR)
    elif chart_type == 'Bar':
        m.addHLOC(CANDLE_UP_COLOR, CANDLE_DOWN_COLOR)
    elif chart_type == 'Line':
        m.addCloseLine(CANDLE_UP_COLOR)

    filename = f'{chart_path}/{ticker}.png'
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


def create_revenue_histogram(ticker, data, img_path):
    millnames = ['', ' Thousand', ' M', ' B', ' T']
    labels = data.keys()
    bars = []
    colors = []
    millidx = 0
    millidxs = []
    for k in data:
        n = float(data[k])
        millidx = max(0, min(len(millnames) - 1,
                             int(math.floor(0 if n == 0 else math.log10(abs(n)) / 3))))
        millidxs.append(millidx)
    millidx = max(millidxs)
    for k in data:
        n = float(data[k])
        val = round(n / 10**(3 * millidx), 2)
        bars.append(val)
        if date.fromisoformat(k) > datetime.datetime.now().date():
            colors.append(0x06468f)
        else:
            colors.append(BAR_UP_COLOR)
    excess_chart = XYChart(H_IMAGE_WIDTH, H_IMAGE_HEIGHT, HIST_BACKGROUND_COLOR)
    excess_chart.setYAxisOnRight(True)
    excess_chart.xAxis().setLabelStyle("normal", 8, H_AXIS_FONT_COLOR, 0)
    excess_chart.yAxis().setLabelStyle("normal", 8, H_AXIS_FONT_COLOR, 0)
    if millidx == 0:
        excess_chart.yAxis().setLabelFormat("{value}")
    elif millidx == 1:
        excess_chart.yAxis().setLabelFormat("{value}Th")
    elif millidx == 2:
        excess_chart.yAxis().setLabelFormat("{value}M")
    elif millidx == 3:
        excess_chart.yAxis().setLabelFormat("{value}B")
    elif millidx == 4:
        excess_chart.yAxis().setLabelFormat("{value}T")
    excess_chart.setPlotArea(0, 25, 605, 205, Transparent, -1, Transparent, 0xcccccc)
    title_str = f'{ticker} Revenue'
    excess_chart.addTitle(title_str, "arialbd.ttf", 12, H_TITLE_FONT_COLOR)
    excess_chart.addText(100, 100, "    @UpsilonBot", "arialbd.ttf", 32, H_WATERMARK_TEXT_COLOR)
    bl = excess_chart.addBarLayer3(bars, colors)
    bl.setBorderColor(Transparent)
    bl.setBarShape(CircleShape)
    excess_chart.xAxis().setLabels(labels)

    filename = f'{img_path}revenue_{ticker}.png'
    excess_chart.makeChart(filename)


def create_custom_histogram(data, header, img_path, filename):
    labels = data.keys()
    bars = data.values()
    colors = []
    for bar in bars:
        if bar >= 0:
            colors.append(BAR_UP_COLOR)
        else:
            colors.append(BAR_DOWN_COLOR)
    excess_chart = XYChart(H_IMAGE_WIDTH, H_IMAGE_HEIGHT, HIST_BACKGROUND_COLOR)
    excess_chart.setYAxisOnRight(True)
    excess_chart.xAxis().setLabelStyle("normal", 8, H_AXIS_FONT_COLOR, 0)
    excess_chart.yAxis().setLabelStyle("normal", 8, H_AXIS_FONT_COLOR, 0)
    excess_chart.yAxis().setLabelFormat("{value}")
    excess_chart.setPlotArea(0, 25, 605, 205, Transparent, -1, Transparent, 0xcccccc)
    title_str = header
    excess_chart.addTitle(title_str, "arialbd.ttf", 12, H_TITLE_FONT_COLOR)
    excess_chart.addText(100, 100, "    @UpsilonBot", "arialbd.ttf", 32, H_WATERMARK_TEXT_COLOR)
    bl = excess_chart.addBarLayer3(bars, colors)
    bl.setBorderColor(Transparent)
    bl.setBarShape(CircleShape)
    excess_chart.xAxis().setLabels(labels)

    filename = f'{img_path}{filename}.png'
    excess_chart.makeChart(filename)


def create_portfolio_donut(portfolio_data=None, title="", filename="pie"):
    data = [round((i * 100), 2) for i in portfolio_data.values()]
    # debug(data)
    labels = portfolio_data.keys()
    # debug(labels)

    pie_chart = PieChart(P_IMAGE_WIDTH, P_IMAGE_HEIGHT, P_BACKGROUND_COLOR)

    title = pie_chart.addTitle(title, "timesbi.ttf", 18, P_TITLE_FONT_COLOR)
    title.setMargin2(0, 0, 8, 8)
    pie_chart.addLine(10, title.getHeight() - 2, pie_chart.getWidth() - 11, title.getHeight(), P_TITLE_FONT_COLOR, 2)
    pie_chart.setDonutSize(160, 200, 110, 0)
    pie_chart.setStartAngle(85)
    # pie_chart.setTransparentColor(20)
    pie_chart.setData(data, labels)
    # pie_chart.setSectorStyle(RingShading)
    pie_chart.setColors(transparentPalette)
    pie_chart.setBackground(P_OUTER_BACKGROUND_COLOR)
    pie_chart.setLabelLayout(SideLayout, 16)
    pie_chart.setLabelFormat("<*font=arialbd.ttf,size=13,color=%s*>{={sector}+1}" % 0xffffff)
    pie_chart.setLabelStyle("arialbd.ttf", 10).setBackground(Transparent, P_AXIS_FONT_COLOR)
    pie_chart.setLineColor(Transparent, P_AXIS_FONT_COLOR)
    legend_box = pie_chart.addLegend(330, 185, 1, "arialbi.ttf", 10)
    legend_box.setAlignment(Left)
    legend_box.setBackground(Transparent, P_AXIS_FONT_COLOR)
    legend_box.setFontColor(P_AXIS_FONT_COLOR)
    legend_box.setRoundedCorners()
    legend_box.setMargin(16)
    legend_box.setKeySpacing(0, 5)
    legend_box.setText(
        "<*block,valign=top*>{={sector}+1}.<*advanceTo=22*><*block,width=120*>{label}<*/*>"
        "<*block,width=40,halign=right*>{percent}<*/*>%")

    pie_chart.makeChart(f'{CHARTER_IMAGES_PATH}{filename}.png')


def manual_create_portfolio_donut(portfolio_data=None, title="", filename="pie"):
    data = [round((i * 100), 2) for i in portfolio_data.values()]
    # debug(data)
    labels = portfolio_data.keys()
    # debug(labels)

    pie_chart = PieChart(P_IMAGE_WIDTH, P_IMAGE_HEIGHT, P_BACKGROUND_COLOR)

    title = pie_chart.addTitle(title, "timesbi.ttf", 18, P_TITLE_FONT_COLOR)
    title.setMargin2(0, 0, 8, 8)
    pie_chart.addLine(10, title.getHeight() - 2, pie_chart.getWidth() - 11, title.getHeight(), P_TITLE_FONT_COLOR, 2)
    pie_chart.setDonutSize(160, 200, 110, 0)
    pie_chart.setStartAngle(85)
    # pie_chart.setTransparentColor(20)
    pie_chart.setData(data, labels)
    # pie_chart.setSectorStyle(RingShading)
    pie_chart.setColors(transparentPalette)
    pie_chart.setBackground(P_OUTER_BACKGROUND_COLOR)
    pie_chart.setLabelLayout(SideLayout, 16)
    pie_chart.setLabelFormat("<*font=arialbd.ttf,size=13,color=%s*>{={sector}+1}" % 0xffffff)
    pie_chart.setLabelStyle("arialbd.ttf", 10).setBackground(Transparent, P_AXIS_FONT_COLOR)
    pie_chart.setLineColor(Transparent, P_AXIS_FONT_COLOR)
    legend_box = pie_chart.addLegend(330, 185, 1, "arialbi.ttf", 10)
    legend_box.setAlignment(Left)
    legend_box.setBackground(Transparent, P_AXIS_FONT_COLOR)
    legend_box.setFontColor(P_AXIS_FONT_COLOR)
    legend_box.setRoundedCorners()
    legend_box.setMargin(16)
    legend_box.setKeySpacing(0, 5)
    legend_box.setText(
        "<*block,valign=top*>{={sector}+1}.<*advanceTo=22*><*block,width=120*>{label}<*/*>"
        "<*block,width=40,halign=right*>{percent}<*/*>%")

    pie_chart.makeChart(f'{CHARTER_IMAGES_PATH}{filename}.png')


def color_2_int(red, green, blue, alpha):
    return ((255 - alpha) << 24) + (red << 16) + (green << 8) + blue


def color_2_chart_string(int_color):
    res = hex(int_color)
    return res
