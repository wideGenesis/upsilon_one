import re

pattern = re.compile(r'^(\/start\b|'
                     r'\/publish_to\b|'
                     r'\/to\b|'
                     r'\/about\b|'
                     r'\/goals\b|'
                     r'\/skills\b|'
                     r'\/future\b|'
                     r'\/support\b|'
                     r'\/adv\b|'
                     r'\/bug\b|'
                     r'portfolio\b|portfolios\b|'
                     r'Info\b|info\b|Information\b|information\b|🛎 Information\b|'
                     r'Main menu\b|menu\b|main menu\b|📁 Main menu\b|'
                     r'Profile\b|profile\b|👤 Profile\b|'
                     r'\/help\b|instructions\b|help\b|'
                     r'news \b|\/q \b|[@#$]|'
                     r'!\b|'
                     r'\/instruction00\b|'
                     r'\/instruction01\b|'
                     r'\/instruction02\b|'
                     r'\/instruction03\b|'
                     r'\/instruction04\b|'
                     r'\/instruction05\b|'
                     r'\/instruction06\b|'
                     r'\/instruction07\b|'
                     r'\/instruction08\b|'
                     r'\/instruction09\b|'
                     r'\/instruction10\b|'
                     r'\/instruction11\b|'
                     r'\/instruction12\b|'
                     r'\/instruction13\b|'
                     r'\/instruction14\b|'
                     r'\/instruction15\b|'
                     r'\/instruction16\b|'
                     r'\/instruction17\b|'
                     r'\/instruction18\b|'
                     r'\/instruction19\b|'
                     r'\/instruction20\b|'
                     r'\/instruction21\b|'
                     r'\/instruction22\b|'
                     r'\/instruction23\b|'
                     r'\/instruction24\b|'
                     r'\/instruction25\b|'
                     r'\/instruction26\b|'
                     r'\/instruction27\b|'
                     r'\/instruction28\b|'
                     r'\/instruction31\b|'
                     r'\/instruction32\b|'
                     r'\/instruction33\b|'
                     r'\/instruction34\b|'
                     r'\/instruction35\b|'
                     r'\/instruction36\b|'
                     r'\/mindepo\b|'
                     r'\/managers_form\b )', re.IGNORECASE)
# r'\/chart_parking\b|'
# r'\/chart_allweather\b|'
# r'\/chart_balanced\b|'
# r'\/chart_aggressive\b|'
# r'\/chart_leveraged\b|'
# r'\/chart_elastic\b|'
# r'\/chart_yolo\b|'



hello_1 = '__I am Upsilon__ – your personal financial manager!'

hello_2 = 'You have savings or profits from business, but do not know where to invest profitably?\n' \
          ' I know not only where, but also how to do it as efficiently as possible. ' \
          'to create passive income!'

hello_3 = 'I will help with financial management to make your investing process easier, ' \
          'doesn\'t matter what your goals are:\n\n' \
          '\U0001F3AF calm and passive income\n' \
          '\U0001F3AF retirement\n' \
          '\U0001F3AF savings for a big purchase\n' \
          '\U0001F3AF future prosperity\n' \
          '\U0001F3AF education of children\n\n' \
          'Together we will achieve your financial goals and you will avoid most of the mistakes, ' \
          'faced by investors.'

hello_4 = '\U00002705 Upsilon helps ordinary people to make savings and to achieve financial freedom. ' \
          'You don\'t need to study investing deeply ' \
          '(unless you want to), I will take on all of the routine work.\n' \
          '\U00002705 Unlike many financial institutions, I help to shape ' \
          'healthy financial habits such as saving and investing. ' \
          'Automate your investments to reach your financial goals'


hello_7 = '__My advantages:__\n\n' \
          '\U0001F3AF I select and manage your diversified portfolio accodring to your goals.\n' \
          '\U0001F3AF rebalance * when necessary to support diversification and risk ' \
          'of the portfolio.\n' \
          '\U0001F3AF I will inform you about the portfolio changes to be made. You don\'t need to care about ' \
          'choosing funds and shares, I will remind you what and how to do.\n'

hello_7a = '\U0001F3AF when rebalancing, I make a choice in favor of large companies with a profit and ' \
          'development potential. Among ETF funds, the choice always rests with the largest funds on the planet.\n' \
          '\U0001F3AF I will not recommend bubbles, zombie corporations. As for ' \
          'country diversification, your portfolio will include the largest funds of developed countries. ' \
          'For risky investors, exchange-traded bitcoin funds are provided.\n' \
          '*Rebalancing is carried out monthly on the first working day.\n' \
          '\U0001F3AF I have paid features, but all new users can demo it for 3 days ' \
           'all functionality is free, but requests for paid functions can be made no more than once within 5 minutes.'


hello_8 = 'Let\'s find a solution in accordance with your plans and goals!\n\n'

goals = '__First Goal__ — find affordable investment solutions for ordinary people!\n' \
        'Financial institutions are not interested in unconditional customer benefit, ' \
        'and focused on increasing commissions. But __investment is the only way to develop__ ' \
        'and improving welfare. There is no development without investments in the future! ' \
        'That\'s why I work for ordinary people, ' \
        'who need professional investment support.\n\n' \
        '__Second Goal__ — information filtering.\n' \
        'I filter out conflicting opinions and use market research and statistical analysis. I found ' \
        'many conditional patterns in market and financial data and I can share them in the form of analysis. ' \
        'You can find my developments in \"Market Analysis\"'

skills = '__My Skills:__ \n \n' \
         '\U00002705 communicate and answer investment and online trading questions\n' \
         '\U00002705 track stock market indicators, analyse stocks on the NYSE and NASDAQ exchanges\n' \
         '\U00002705 track volatility and risks \n' \
         '\U00002705 collect information about the stocks price movement \n' \
         '\U00002705 monitor the dynamics of exchange-traded funds (ETF) on the main US market indices \n' \
         '\U00002705 remind of the need for actions on the market, signal \n' \
         '\U00002705 analyze financial data and even make google requests \n \n' \
         '\U00002705 __My main skill__ — ability to manage investment portfolios in the stock market. ' \
         'I can compose and monitor diversified investment portfolios. ' \
         'Anticipating concerns about my level of competence, I will tell you how ' \
         'investment portfolios and strategies are generated. The principles and methods of building portfolios are based on the latest' \
         ' stock market research. Information required to define the structure ' \
         'of the portfolio is checked for purity, then filtered and used for the stock and fund selection procedure. ' \
         'After the list of shares is formed, weighing is performed. Weight is distributed ' \
         'to minimize risk and increase profitability. A mandatory step in modeling a strategy is ' \
         'checking the stability of the algorithm using the forward testing method. This is a necessary step for ' \
         'prevent deterioration of strategy results in the future. '


mindepo = '__Minimal deposit__ - $5000 \n' \
          '__Required! __ The broker allows the use of odd lots. ' \
          'Odd lots are not divisible by 100 shares.'


brokers = '[Upsilon - brokers comparison](https://t.me/upsilonbot)\n\n' \
          '[Interactive Brokers](https://ibkr.com)\n' \
          '__Basic comission per trade (stocks, ETF)__ - от $0,005\n' \
          '__Inactivity fee__ - $10/месяц\n' \
          '__Trading platforms__ - Desktop, Web, Mobile\n' \
          '__Regulators and licenses__ - FINRA, SIPC, NFA (США)\n' \
          '__Features:__\n' \
          '\U000026A0 blocking of accounts is possible in case of suspicion of the rules violation\n' \
          '\U000026A0 possible restrictions on ETF trading for EU residents\n' \
          '\U000026A0 possible long opening of accounts\n' \
          '\U00002705 for accounts over $ 100,000, interest is accrued on the funds balance, ' \
          'no inactivity fee\n\n' \
         '[Score Priority](https://scorepriority.com)\n' \
          '__Basic commission per trade (stocks, ETFs)__ - $0\n' \
          '__Inactivity fee__ - $0\n' \
          '__Trading platforms__ - Desktop, Mobile\n' \
          '__Regulators and licenses__ - FINRA, SIPC, NFA (США)\n' \
          '__Features:__\n' \
          '\U00002705 opening accounts for residents of the Republic of Belarus\n\n' \
          '[Exante](https://exante.eu)\n' \
          '__Basic commission per trade (stocks, ETFs)__ - от $0.02\n' \
          '__Inactivity fee__ - € 50 for half a year of inactivity\n' \
          '__Trading platforms__ - Desktop, Web, Mobile\n' \
          '__Regulators and licenses__ - FCA (UK), MFSA (Malta), CySEC (Cyprus), SFC (Hong Kong) \n\n' \
          '[TradeStation](https://tradestation.com)\n' \
          '__Basic commission per trade (stocks, ETF)__ - $0\n' \
          '__Inactivity fee__ - $50 for a year of inactivity\n' \
          '__Trading platforms__ - Desktop, Web, Mobile\n' \
          '__Regulators and licenses__ - FINRA, SIPC, NFA (USA)\n\n'


# managers_form = 'If you are interested in cooperation and placement of services or portfolios on the platform,' \
#                 'send a questionnaire by completely copying the template,' \
#                 'and then add your answer to each question. After filling out, just send a message. \n \n '\
#                 'Manager registration form # \n' \
#                 '1. License - \n '\
#                 '2. Company name - \n '\
#                 '3. Contact - \n '\
#                 '4. Experience - \n '\
#                 '5. Do you provide a choice of portfolios - the tariff scale or the portfolio is selected '\
#                 'individually? - \n '\
#                 '6. Serving Broker - \n '\
#                 '7. Are you ready to provide daily returns on the portfolios you want '\
#                 'place on the site? - \n \n '\
#                 '__Example of filling. Send without changing the title .__ \n \n '\
#                 'Manager registration form \n' \
#                 '1. License - CySEC \n '\
#                 '2. Company name - ABC Inc \n '\
#                 '3. Contact @ abc-inc, + xx (yyy) 1231212 \n '\
#                 '4. Experience - 10 years \n '\
#                 '5. Do you provide a choice of portfolios - tariff scale or '\
#                 'is the portfolio selected individually? - tariff scale \n '\
#                 '6. Serving Broker - goldmansachs.com \n '\
#                 '7. Are you ready to provide daily returns on the portfolios you want '\
#                 'to place on the platform? - Yes \n \n '

instructions_main = '__Instructions__ \n \n' \
                    'Goals - /goals \n' \
                    'My skills are /skills \n' \
                    'Dialog core - /instruction00 \n' \
                    'stock growth and falls statistics - /instruction01 \n' \
                    'US market trend graph - /instruction02 \n' \
                    'Momentum in stocks - /instruction03 \n' \
                    'Heatmaps - /instruction04 \n' \
                    'Yield curve and dividends - /instruction05 \n' \
                    'Volatility curve - /instruction06 \n' \
                    'Cryptocurrency trend chart - /instruction07 \n' \
                    'Trend chart for the RF market - /instruction08 \n' \
                    'Interest rate - /instruction10 \n' \
                    'Inflation rate - /instruction11 \n' \
                    'Composite Purchasing Managers Index - /instruction12 \n' \
                    'Unemployment rate - /instruction13 \n \n' \
                    'Parking briefcase - /instruction14 \n \n' \
                    'Weatherproof briefcase - /instruction15 \n \n' \
                    'Balanced portfolio - /instruction16 \n \n' \
                    'Aggressive portfolio - /instruction17 \n \n' \
                    'shoulder portfolio - /instruction18 \n \n' \
                    'Elastic portfolio - /instruction23 \n \n' \
                    'Yolo portfolio - /instruction23 \n \n' \
                    'All Seasons S - /instruction31 \n \n' \
                    'All Seasons M - /instruction32 \n \n' \
                    'All Seasons L - /instruction33 \n \n' \
                    'Minimum deposit - /mindepo \n \n' \
                    'Latest news about the company you are interested in - /instruction20 \n \n' \
                    'Key statistics about the company you are interested in - /instruction21 \n' \
                    '/instruction22 \n \n'

instruction00 = '__Dialogue core__ \n' \
                'I understand commands and questions. I am still learning to communicate, '\
                'so some of our dialogs may get stuck or I will respond inappropriately. '\
                'I will not answer some questions right away, but after looking for information and thinking it over. '\
                'I have limited resources, so please be patient.'

instruction01 = '__ Stock growth and fall statistics .__ \n' \
                'The ratio of rising to falling stocks on major exchanges' \
                'The US determines the short-term momentum of the market, and hence the momentum of most investment portfolios. '\
                'If the statistic value is more than 55%, then there is enough buers on the market' \
                'to continue growth. If the value is less than 55%, then there is a high probability of price decline '\
                'both today and in the following days. '\
                'This is a short term indicator. If volumes show similar '\
                'momentum, then there is momentum in the market. If the volume indicators do not confirm the ratio '\
                'rise to fall, then there is no impulse.'

instruction02 = '__US Market Overview__ \n\n' \
                '\U0001F537 __Market Condition__ - trend detector, detects the presence of a bullish trend or correction. \n '\
                '\U0001F537 __Hedge demand__ - detector of demand for hedging or defensive assets. '\
                'The stronger the demand for defensive assets, the stronger the fear in the market and the more likely it is' \
                'what will be the correction. \n '\
                '\U0001F537 __Sentiment__ - sentiment detector. '\
                'Extreme greed | Greed | Fear | Extreme fear \n '\
                'As long as the Greed level remains and above, the market is normal and is within the' \
                'expected trend. \n\n '\
                'Block __Hedge Analysis__ \n\n' \
                '\U0001F537 __Current hedge__ - detector of the best defensive asset for the current market. \n \n' \
                'Block __Factor Analysis__ \n \n' \
                'The detector determines which factors bring more' \
                'profitability in the current situation. \n' \
                'Factors to compare: Momentum, Value, Large, Small, Developed, Emerging, Old Economy, New Economy \n' \
                '\U0001F537 Volatility - defines the state of futures on the VIX. Contango - no risk, Backwardation - '\
                'there is a risk, there is a decrease in the market \n \n' \
                '__Color of the main chart candles .__ \n \n' \
                'History of trend detector signals. The trend is determined heuristically. '\
                'As long as the color of the candles remains green, the market is within the expected trend,' \
                'those. the trend remains bullish. \n \n '\
                '__How to use the market analyzer? __ \n' \
                'If you use portfolio correction techniques, read carefully' \
                'next statement. \n' \
                '\U0001F537 Changing the mode from Trend to Correction is the time to sell part of the portfolio and' \
                'purchase protective' \
                'asset, which is defined in the line Current hedge. \n' \
                '\U0001F537 Changing the mode from Correction to Trend is the time for reverse rebalancing,' \
                'that is, for sale' \
                'the protective part of the portfolio and buying the risky part, for example stocks or SPY. \n' \
                'Changing the mode from Correction to Trend is the best time for additional investment,' \
                'that is, the best time for the so-called "refills". \n \n '\
                '\U0001F537 The defensive asset detector can be used for more than just protecting the portfolio during' \
                'corrections, but also for the "portfolio-bar". That is, instead of holding bonds, '\
                'which can fall in price, you can use a detector to determine the best option' \
                'protective asset. For example, your portfolio usually includes ratio of 60% stocks and 40% bonds, '\
                'but the detector shows that the best defensive asset right now is the cache. If you replace your 40% '\
                'bonds to cash, then the portfolio yield will improve. \n \n' \
                '\U0001F537 Factor analysis is used to determine the more profitable factor. \n' \
                'If you invest using factors, the detector will tell you which factors are more profitable right now.'


instruction35 = '__Signals__ \n \n' \
                '\U0001F537 __Long__ - the signal indicates the resumption of the trend. This is the optimal point '\
                'for the initial entry into the market, adding funds or rebalancing in more risky assets. \n '\
                '\U0001F537 __Risk-off__ - signal indicates deflationary pressure. In such conditions, the growth of '\
                'The market is not justified by anything, since the presence of inflation is the main criterion for the growth of markets. '\
                'This is the point to rebalance into defensive assets. Defensive assets suitable for the current market, '\
                'you can find in the infobox. '

instruction03 = '__ Promotional Moment__ \n \n' \
                'Momentum readings over 55% indicate a trend in the US market. '\
                'With such values, you can buy, buy, buy rollbacks. \n \n '\
                'Values ​​less than 55% are typical for corrections. If you manage portfolios yourself, '\
                'then you should either reduce the share of shares in the portfolio or rebalance into defensive assets. '\
                'If you are a trader, it\'s time to short sell.'

instruction04 = '__Heat cards__ \n \n' \
                'There are 5 heatmap options available: \n' \
                '\U0001F537 changes in the US stock market during the last trading day \n' \
                '\U0001F537 major stock market movements by region during the last trading day \n' \
                '\U0001F537 changes in the RF market during the last trading day \n \n' \
                '\U0001F537 crypto market changes during the last trading day \n \n' \
                '__1-day map__ can be used to search for up / down leaders and evaluate sectors and runaway' \
                'look at the market.'

instruction05 = '__Dividends__ \n \n' \
                'The average SP500 dividend yield can be compared to the yield on a 10-year bond,' \
                'to determine how much rational to invest in bonds or stocks. '\
                'If the dividend yield becomes __ less__ than the bond yield, and' \
                'the yield on bonds is higher than the inflation rate, then the market will experience it after a while' \
                'correction. Investors prefer to invest in bonds' \
                'due to the higher yield, even though the maturity is long. '\
                'The opposite situation is also possible - when the dividend yield rises sharply and' \
                'is outstripping inflation and bond yields. This means the start of recovery '\
                'the market is after the correction and is a strong signal for growth.'

instruction06 = '__Volatility Analysis__ \n \n' \
                'The volatility curve tracks market expectations for future volatility' \
                'by comparing the time frames of the SPX implied volatility. '\
                'When more distant futures, that is, futures with long expiration dates are priced' \
                'the market is more expensive,' \
                'than the nearest futures, then this situation is called __Contango__. '\
                'Contango is a normal situation for' \
                'market, it means that the current risks are less than the risks in the future. '\
                'The price of volatility futures takes into account the time factor, the further the expiration is' \
                'futures volatility, the more expensive the futures price. '\
                'The opposite situation is - __backwardation__. Backwardation - the market evaluates the coming futures for '\
                'volatility is more expensive than long-range volatility. That is, the risks are now more expensive than in the future. '\
                'When backwardation is observed, it is one of the main signals of a stock market correction. '\
                'As a rule, during sharp downturns, volatility rises sharply and the time structure' \
                'VIX futures are changed to backwardation. Completion of the backwardation stage means the beginning of the '\
                'recovery in the market, that is, the risks of time become more expensive than the current risks, which means' \
                'the market started an upward trend. \n \n '\
                'It is very easy to use this risk detector. \n' \
                'If there is a trend in the market, then you will see a signal - __Contango .__ \n' \
                'If there is a correction in the market, then you will see a signal - __Backwordation .__'

instruction07 = '__Graph of the general trend in the cryptocurrency market__ \n \n' \
                'Main graph. \n '\
                '\U0001F537 __Market Condition__ - trend detector, detects the presence of a bullish trend or correction. \n '\
                '\U0001F537 __Sentiment__ - sentiment detector. '\
                'Extreme greed | Greed | Fear | Extreme fear \n '\
                'As long as the Greed level remains and above, the market is normal and is within the' \
                'expected trend. \n \n '\
                'Block __Factor Analysis__ \n \n' \
                'The detector determines which cryptocurrencies bring the most' \
                'profitability in the current situation. \n' \
                'Factors to compare: BTC, ETH, Alts \n' \
                '__Color of candles on the main chart .__ \n \n' \
                'History of trend detector signals. The trend is determined heuristically. '\
                'As long as the color of the candles remains green, the market is within the expected trend,' \
                'those. the trend remains bullish. \n \n '\
                '__How to use the market analyzer? __ \n' \
                'If you use portfolio correction techniques, read carefully' \
                'next statement. \n' \
                '\U0001F537 Changing the mode from Trend to Correction is the time to sell part of the portfolio \n' \
                '\U0001F537 Changing the mode from Correction to Trend is the time for reverse rebalancing,' \
                'that is, to sell altcoins or exit the cache \n' \
                'Changing the mode from Correction to Trend is the best time for additional investment,' \
                'that is, the best time for the so-called "refills". \n \n '

instruction08 = '__Graph of the general trend in the Russian market__ \n \n' \
                'Main schedule. \n '\
                'A trend detector is superimposed on the Moscow Exchange index, which is determined by a heuristic method. '\
                'As long as the color of the candles remains green, the market is within the expected trend,' \
                'those. the trend remains bullish. \n \n '\
                'subwindow. \n '\
                'A portfolio of index stocks. Exclusively reference indicator. '\
                'Its goal is to show that a "better" portfolio is possible and can be invested with a high' \
                'profitability even on the Russian stock market. \n \n '\
                'In the near future, portfolio options for the Russian market will become available.'

instruction09 = '__TF Sentiment__ \n \n' \
                'Cash flows to funds representing asset classes allow us to assess the dynamics of preferences' \
                'investors. Are you investing in risky, defensive or risk-free instruments now? '\
                'More money in venture funds means a trend in the US stock market. \n '\
                'Inflows into bond funds and outflows from risky equity funds means a correction in the stock' \
                'the US market. \n \n '\
                'Cash flows allow you to reveal the big picture and determine which asset class goes to' \
                'financial flows. '

instruction10 = '__Interest rate__ \n \n' \
                '\U0001F537 Easing of monetary policy. \n '\
                'Lower interest rates, additional incentives to make money cheaper, or' \
                'easier access to money or quantitative easing programs stimulate long-term' \
                'growth of markets. As a rule, it takes time for the market to react to incentives - from a few '\
                'weeks to several months. Usually, such measures are applied in crisis' \
                'situations and falls in inflation. \n \n '\
                '\U0001F537 Monetary tightening. \n '\
                'Raising interest rates, canceling incentive programs, quantitative easing,' \
                'sale of assets from the Fed\'s balance sheet. '\
                'The tightening of monetary policy does not have a clear impact on the market. '\
                'After the tightening of the policy, the stock market behaves differently, depending on' \
                'from the context of the economic situation, other informational factors.'

instruction11 = '__Inflation rate__ \n \n' \
                'For the economy to function normally, the annual inflation rate must be within the range of 2% -4%. '\
                'Inflation values ​​above this threshold in developed economies stimulate central banks' \
                'to raise interest rates to prevent hyperinflation. '\
                'A normal rate of inflation stimulates the growth of stock markets. '\
                'stock market growth is stronger in a region with a higher inflation rate,'\
                'if inflation does not exceed the 4% limit.'

instruction12 = '__Composite Purchasing Manager Index__ \n \n' \
                'Business activity indices are used to assess the state of the economy. '\
                'Business activity indices are of particular importance in macroeconomics, as well as for participants' \
                'stock markets. The index reflects the mood of industrial companies and characterizes the state of '\
                'business climate. \n \n '\
                '\U0001F537 A reading above 50 indicates a recovery in business activity,' \
                'below 50 indicates deterioration' \
                'economic situation. Values ​​above 50 indicate that the majority of respondents' \
                'positively characterizes the business conditions at the time of the survey, while the data' \
                'Below 50 indicates worsening business conditions. \n \n '\
                'Thus, PMI is a leading indicator of production and inflation. \n \n '\
                'The indicator is used to control the share of bonds in the portfolio, since it is' \
                'has a strong correlation with changes in bond prices and not with the stock market. \n '\
                '\U0001F537 Decrease in PMI stimulates growth in bond prices,' \
                'allowing investors to have a more diversified portfolio with less' \
                'risk in such periods, values ​​above 50 indicate stable functioning of the economy,' \
                'readings below 50 indicate a possible recession in the future or the current crisis.'

instruction13 = '__Unemployment rate__ \n \n' \
                'The rising unemployment rate is a clear sign of problems in the economy. \n '\
                '\U0001F537 Increase in unemployment indicates impending recession and recession on' \
                'the market, especially if the jump in unemployment is large. \n '\
                '\U0001F537 The stabilization of the labor market marks the beginning of a recovery in the stock market and the economy.'

instruction14 = '\U0001F4BC __Parking Briefcase__ \n \n' \
                'This portfolio serves as a replacement for long-term bonds and has the best ratio' \
                'risk-to-return than buying US bonds. The portfolio has stable growth and '\
                'yields on par with long-term US bonds, but without the inherent volatility of bonds. \n \n '\
                '__Advantages: __ \n' \
                '\U0001F537 low volatility compared to bonds, stable capital growth. \n \n '\
                '__ Who is the parking portfolio for? __ \n' \
                '\U0001F537 you are afraid of risks and you need low but stable profitability \n' \
                '\U0001F537 you are new to the stock market \n \n' \
                '__When to buy a parking portfolio? __ \n' \
                '\U0001F537 at any given time \n' \
                '\U0001F537 on the first trading day of the month, the user should' \
                'call up the required portfolio through the menu and buy the shares indicated in the diagram. '\
                'More info - / instruction27 \n' \
                '\U0001F537 when you need to park money \n' \
                '\U0001F537 during recession, corrections \n' \
                '\U0001F537 instead of bonds, as a way to enter a more risky "working" portfolio. '\
                'For example, you buy a third of your work portfolio and invest the rest in' \
                'parking portfolio, and then when adjusting the work portfolio, you translate' \
                'money from parking to work briefcase. This will allow the money to work and reduce the '\
                'risks of drawdown of the working portfolio.'

instruction15 = '\U0001F4BC __All Weather Portfolio__ \n \n' \
                'The portfolio works in any market and economic environment. '\
                'The risks are evenly distributed among the assets. Such a portfolio is resistant to any '\
                'market turmoil, has relatively low risk and higher returns' \
                'for a portfolio of this type. Portfolio focused on capital preservation - aggressive '\
                'You should not expect growth from him. The all-weather portfolio consists of the assets of all '\
                'classes and, depending on the market situation, allocates capital in such a way,' \
                'to achieve the lowest possible risk in all conditions. \n \n '\
                '__Advantages: __ \n' \
                '\U0001F537 low volatility compared to SPY \n' \
                '\U0001F537 lower maximum drawdown compared to SPY \n' \
                '\U0001F537 higher long-term profitability compared to SPY \n' \
                '\U0001F537 stable capital growth \n \n' \
                '__Who is an all-weather portfolio suitable for? __ \n' \
                '\U0001F537 you are afraid of risks and do not want to take risks, but at the same time you want to receive profitability' \
                'above the inflation rate and above the level of interest rates on deposits \n' \
                '\U0001F537 retirement portfolio \n \n' \
                '__When to buy an all-weather portfolio? __ \n' \
                '\U0001F537 on the first trading day of the month, the user should' \
                'call up the required portfolio through the menu and buy the shares indicated in the diagram. '\
                'More info - / instruction27 \n' \
                '\U0001F537 at any given time'

instruction16 = '\U0001F4BC __Balanced Portfolio__ \n \n' \
                'Portfolio with a conservative weighting approach focused on the performance of the QQQ fund. '\
                'There are no new companies in the portfolio, but most of the portfolio is split between' \
                'technology companies, due to which high profitability is achieved. '\
                'Conservative capital allocation keeps risks relatively low. \n \n '\
                '__Advantages: __ \n' \
                '\U0001F537 low volatility compared to QQQ \n' \
                '\U0001F537 lower maximum drawdown compared to QQQ, \n' \
                'profitability comparable to QQQ \n' \
                '\U0001F537 stable capital growth \n \n' \
                '__ Who is a balanced portfolio for? __ \n' \
                '\U0001F537 you want a portfolio with relatively low and stable risks over time,' \
                'but with high profitability \n' \
                '\U0001F537 you want to get the QQQ level of profitability with less risks and drawdowns \n \n' \
                '__When to buy a balanced portfolio? __ \n' \
                '\U0001F537 on the first trading day of the month, the user should' \
                'call up the required portfolio through the menu and buy the shares indicated in the diagram. '\
                'More info - / instruction27 \n' \
                '\U0001F537 at any time, but on the first trading day of the month,' \
                'except for periods of explosive capital gains. '\
                'In that case, we should wait for the portfolio to return to average growth rates.'

instruction17 = '\U0001F4BC __Aggressive Portfolio__ \n \n' \
                'The purpose of the portfolio is to generate more returns than the QQQ fund. '\
                'There are new companies in the portfolio, most of the portfolio is distributed between' \
                'by technological, biotechnological and fintech companies, due to which it is achieved '\
                'high profitability. Conservative capital allocation allows to keep risks on '\
                'relatively low level. \n \n '\
                '__Advantages: __ \n' \
                '\U0001F537 low volatility compared to QQQ, lower maximum drawdown' \
                'versus QQQ \n' \
                '\U0001F537 higher long-term profitability compared to QQQ \n' \
                '\U0001F537 stable capital growth \n \n' \
                '__ Who is an aggressive portfolio for? __ \n' \
                '\U0001F537 if you are focused on high returns and ready for medium risks. \n \n '\
                '__When to buy an aggressive portfolio? __ \n' \
                '\U0001F537 on the first trading day of the month, the user should' \
                'call up the required portfolio through the menu and buy the shares indicated in the diagram. '\
                'More info - / instruction27 \n' \
                '\U0001F537 at any time, but on the first trading day of the month,' \
                'except for periods of explosive capital gains. '\
                'In that case, we should wait for the portfolio to return to average growth rates.'

instruction18 = '\U0001F4BC __Shoulder Briefcase__ \n \n' \
                'The goal of the portfolio is to bring the highest possible return with the drawdown level of the QQQ fund. '\
                'There are new companies in the portfolio, most of the portfolio is distributed between' \
                'by technological, biotechnological and fintech companies, due to which a high' \
                'profitability. The portfolio uses shoulder funds to increase returns. '\
                'shoulder funds are always limited in weight and are recruited into the portfolio only when' \
                'growth or expectation of market growth. At the slightest threat of correction, shoulder funds are sold or '\
                'a risk balancing mechanism is activated to prevent a decrease in portfolio capitalization. \n \n '\
                '__Advantages: __ \n' \
                '\U0001F537 portfolio volatility repeats the QQQ volatility level \n' \
                '\U0001F537 portfolio drawdown repeats the QQQ drawdown level \n' \
                '\U0001F537 higher yield compared to QQQ \n' \
                '\U0001F537 stable capital growth \n \n' \
                '__Who is a shoulder bag suitable for? __ \n' \
                '\U0001F537 if you are focused on high returns and ready for high risks \n' \
                '\U0001F537 you understand the nature of high risk \n' \
                '\U0001F537 you are a former or current trader \n' \
                '\U0001F537 you are a cryptocurrency investor \n \n' \
                '__When to buy a shoulder bag? __ \n' \
                '\U0001F537 on the first trading day of the month, the user should' \
                'call up the required portfolio through the menu and buy the shares indicated in the diagram. '\
                'More info - / instruction27 \n' \
                '\U0001F537 at any time, but on the first trading day of the month,' \
                'except for periods of explosive capital gains. '\
                'In that case, we should wait for the portfolio to return to average growth rates.'

instruction19 = '__How to interpret Monte Carlo simulation results? __ \n \n' \
                'The Monte Carlo method is understood as a numerical method for solving mathematical problems using' \
                'simulation of random variables. \n' \
                'simulation of portfolio returns using the Monte Carlo method' \
                'is as follows: changes in portfolio returns are described by mathematical' \
                'a model using a random variable generator, the model is calculated many times' \
                '(10000-100000 iterations), based on the data obtained, the probabilistic characteristics are calculated' \
                'portfolio with given characteristics. Monte Carlo methods are used to solve problems in '\
                'various fields of physics, mathematics and economics. \n \n '\
                '__Rules of interpretation: __ \n' \
                '\U0001F537 should be guided by the 50th percentile - the average result obtained in' \
                '100,000 10-year simulations. '\
                'This means that this is the most likely meaning of the results to be expected' \
                'from investments in a portfolio of this type \n' \
                '\U0001F537 10th percentile - 10% of portfolios of 100,000 simulations performed worse or equal to' \
                'these values ​​for 10 years \n' \
                '\U0001F537 25th percentile - 25% of portfolios of 100,000 simulations performed worse or equal to' \
                'these values ​​for 10 years \n' \
                '\U0001F537 75th percentile - 75% of portfolios of 100,000 simulations performed worse or equal to' \
                'these values ​​for 10 years \n' \
                '\U0001F537 90th percentile - 90% of portfolios of 100,000 simulations performed worse or equal to' \
                'these values ​​for 10 years. '\
                'It\'s almost impossible to get a result better than the 90th percentile. \n \n '\
                '__Frequency Graph - Abbreviated (10000) simulation of the final balance .__ \n' \
                'The frequency value is the X-axis. The final balance value achieved in 10 years is the Y-axis. \n' \
                'The values ​​of the diagram determine the number of portfolios that have reached a certain' \
                'balance values ​​for 10 years. '

instruction20 = 'To view the latest news from global media for the company of interest,' \
                'type in message line \n' \
                '__news and company ticker__. \n \n '\
                'For example: \n' \
                '__news AAPL__ \n' \
                '__news nvda__ \n \n'

instruction21 = 'To view financial analysis for a company of interest,' \
                'type in message line \n' \
                'any of the special characters __ # @ ticker__ or __ $ @ ticker__ or __ @ ticker__ without spaces \n \n' \
                'For example: \n' \
                '__ # AAPL__ \n' \
                '__ $ NVDA__ \n' \
                '__ @ AMZN__ \n \n' \
                'When using financial analysis, 1 request is written off🔋'

instruction22 = 'Comparison of key company statistics with benchmark,' \
                'allows you to quickly assess the stability and potential of a stock. \n \n '\
                '__CAGR% __ is the compound annual growth rate. '\
                'Expressed as a percentage and shows how many percent grows on average over the year' \
                'stock returns.' \
                'It is useful to compare the CAGR of companies with each other or an index. '\
                'A larger CAGR is a more profitable company. \n \n '\
                '__Sharpe__ - an indicator of the performance of an investment portfolio or asset,' \
                'which is calculated as the ratio of the average return to the average portfolio risk. '\
                'sharpe ratio is used to determine how good a return is' \
                'the asset compensates for the risk taken by the investor. When comparing two assets with the same '\
                'profitability, investing in an asset with a higher Sharp will be less risky. \n \n '\
                '__Volatility (ann.)% __ - average annual volatility, is a measure of risk' \
                'financial asset. '\
                'The lower this indicator, the less risky the asset or portfolio is. \n \n '\
                '__Kelly Criterion% ​​__ - determines the optimal bet size. Used to compare stocks' \
                'between themselves. The higher the Kelly criterion for a particular stock, the more profitable this' \
                'investment versus a share with a lower criterion value. \n \n '\
                '__Daily Value-at-Risk__ is the value at risk. It is a measure of the risk of losing an investment. '\
                'The parameter estimates how much the asset can lose (with a given probability, usually 95%)' \
                'under normal market conditions per day. For example, DVAR = 2% - this means that '\
                'maximum possible loss after eliminating all worst outcomes with' \
                '95% probability will not exceed 2%. This is a measure of risk that excludes "black swans" from calculations, '\
                'that is, this is the maximum risk under normal market conditions. \n \n '\
                '__Alpha__ - the coefficient is used to determine the return on an asset or portfolio' \
                'higher than the theoretical, expected return. Used as a measure of control '\
                'portfolio. Alpha is positive - the asset or portfolio brings more profitability, '\
                'than expected. For actively managed portfolios, the presence of a positive Alpha '\
                'means management is effective. \n \n '\
                'Used to compare portfolios or stocks - the higher the Alpha, the more profitable the investment.' \
                '__Beta__ is a measure of market risk reflecting the variability of the return on an asset or portfolio by' \
                'in relation to the return on another portfolio, which is the index. '\
                'For example, Beta = 2 - when the price of the index changes by a certain amount, given' \
                'the investment will change twice as much. Beta = 1 - means that the returns' \
                'investment changes by the same amount as the market. \n '

instruction23 = '\U0001F4BC __Elastic Strategy__ \n \n' \
                'The purpose of the portfolio is to generate more returns than the QQQ fund. '\
                'There are new companies in the portfolio, most of the portfolio is distributed between' \
                'by technological, biotechnological and fintech companies, due to which it is achieved '\
                'high profitability. Conservative capital allocation allows to keep risks on '\
                'relatively low level. \n \n '\
                '__Advantages: __ \n' \
                '\U0001F537 lower maximum drawdown' \
                'versus QQQ \n' \
                '\U0001F537 higher long-term profitability compared to QQQ \n' \
                '\U0001F537 stable capital growth \n \n' \
                '__ Who is Elastic Strategy for? __ \n' \
                '\U0001F537 if you are limited to buying stocks exclusively, without the option to buy ETFs. \n '\
                '\U0001F537 if you are focused on high returns and ready for medium risks. \n \n '\
                '__When to buy Elastic portfolio? __ \n' \
                '\U0001F537 on the first trading day of the month, the user should' \
                'call up the required portfolio through the menu and buy the shares indicated in the diagram. '\
                'More info - / instruction27 \n' \
                '\U0001F537 at any time, but on the first trading day of the month, except for periods' \
                'explosive capital growth. '\
                'In that case, we should wait for the portfolio to return to average growth rates.'

instruction24 = '\U0001F4BC __Yolo Strategy__ \n \n' \
                'The purpose of the portfolio is to bring in higher returns than an SPY fund. The portfolio consists of stocks only, '\
                'traded on spbexchange. Available for clients of Sberbank, Tinkoff, Alfa-Bank, VTB. '\
                'There are new companies in the portfolio, most of the portfolio is distributed between' \
                'by technological, biotechnological and fintech companies, due to which it is achieved '\
                'high profitability. Conservative capital allocation allows to keep risks on '\
                'relatively low level. \n \n '\
                '__Advantages: __ \n' \
                '\U0001F537 lower maximum drawdown compared to SPY \n' \
                '\U0001F537 higher long-term profitability compared to SPY \n' \
                '\U0001F537 stable capital growth \n \n' \
                '__ Who is the Yolo Strategy for? __ \n' \
                '\U0001F537 if you are an investor from the Russian Federation, but want to invest in the most successful companies from the USA. \n '\
                '\U0001F537 if you are limited to buying stocks exclusively, without the option to buy ETFs. \n '\
                '\U0001F537 if you are focused on high returns and ready for medium risks. \n \n '\
                '__When to buy Yolo portfolio? __ \n' \
                '\U0001F537 on the first trading day of the month, the user should' \
                'call up the required portfolio through the menu and buy the shares indicated in the diagram. '\
                'More info - / instruction27 \n' \
                '\U0001F537 at any time, but on the first trading day of the month,' \
                'except for periods of explosive capital gains. '\
                'In that case, we should wait for the portfolio to return to average growth rates.'

instruction25 = '__Reset Risk Profile __ \n \n' \
                'If you inattentively went through the risk profiling and want to clarify it, then you can do' \
                'reset the profile. If you do not like the return on the selected portfolios, it is too low, '\
                'then your expectations from the market are unrealistic given the risk that you are psychologically' \
                'you can admit. In this case, it is not recommended to reset the risk profile \U000026D4__! __ \U000026D4 \n \n '\
                'If you buy a portfolio with a higher profitability, and therefore with a greater risk, to which it is moral' \
                'not ready and you will face a drawdown, then you just sell such a portfolio and fix the drawdown' \
                'at a loss. You can\'t just promise yourself to take more risk than you can actually handle. '\
                'Therefore, it is critical to be honest with yourself!'

instruction26 = '__About Trust__. \n \n '\
                '__Risk Profile__. \n '\
                'In accordance with regional laws, management companies are obliged to carry out the procedure' \
                'risk profiling, that is, to determine the level of risk tolerance. After defining your '\
                'risk tolerance and category assignment can choose investment products and get' \
                'investment information associated with selected products. Before going through risk profiling '\
                'Providing investment information is prohibited. This approach is practiced because investment '\
                'are associated with risks and the client of the company must have an idea of ​​their tolerance for' \
                'risk and their goals. \n \n '\
                'Access to statistics of investment products of management companies. '\
                'Management companies work through brokers with different infrastructures,' \
                'usually it is a general corporate account segregated into customer sub-accounts. '\
                'The main brokers with whom management companies in the CIS countries cooperate' \
                'Is IBKR, Exante, Tradestation. '\
                'These brokers do not provide the ability to automatically separate trades and positions' \
                'clients of the management company. That is, statistics and status of client portfolios are available in '\
                'the form of reports. This makes it difficult to provide information '\
                'for new clients. The client can see his own positions directly in his office, '\
                'on your account and can generate reports. '\
                'A company can similarly create reports on its account, but such statistics' \
                'can be mixed and irrelevant because different clients have different portfolios with different' \
                'drawdowns and yields. Therefore, management companies often do not provide '\
                'statistics and all information on investment products are limited to presentations. '\
                'This situation exists due to regulatory restrictions, so the company has no right' \
                'provide and generate reports and statistics on customer accounts for marketing purposes,' \
                'and the provision of general statistics on the corporate account contains depersonalized positions' \
                'all clients and portfolios at once. That is, the new client will not be able to get an idea of ​​'\
                'the portfolio he needs. \n' \
                'In turn, large management companies tend to create ETFs or mutual funds. '\
                'In this case, strategy or portfolio statistics are transparently available to everyone. \n \n' \
                'The best solution to increase transparency and trust is third-party maintenance' \
                'portfolio statistics and providing clients of the management company with online access to '\
                'reference portfolio. For example, a client chooses a portfolio from those available in the bot. These portfolios' \
                'are monitored independently of the management company, and the company implements an identical strategy. '\
                'In this case, such third-party statistics can serve in monitoring and in' \
                'for marketing purposes. Any interested client can not just trust the words of the manager '\
                'companies, and browse portfolios and strategies in the bot and choose the appropriate solution. '\
                'After that, the client agrees with the company on all the details, signs contracts and the company' \
                'manages the client\'s assets according to the generally accepted scheme of managed accounts. \n \n '\
                '__Managed account__ is the account where the company can manage assets' \
                'client, but does not have access to the withdrawal and deposit of funds, that is, only market transactions. \n \n '\
                'That is why Upsilon is inviting asset managers to list their portfolios. '\
                'This increases the transparency of portfolios as all information is available online: history,' \
                'backtests, current allocation and changes in the capital of the strategy. The client transparently has access' \
                'to all this data, and can check the strategy of the management company for compliance' \
                'the declared profitability and risk. And also, having access to the weights, recreate the '\
                'the portfolio on your own and check against what is on the managed account.'

instruction27 = '__How and when to buy a portfolio? __ \n \n' \
                'All Upsilon portfolios are fully algorithmic and automatic. \n '\
                '\U00002757 Any of the portfolios is rebalanced every 1st day of the month at 12:00 UTC. \n '\
                'The rebalancing procedure takes place in several stages: \n' \
                'one. A sample is formed based on an algorithm that takes into account '\
                'the company\'s popularity in the media and social networks, liquidity, profitability and sales growth. \n '\
                '2. The sample is sieved using another algorithm, the task of which is to select the most '\
                'promising stocks. \n '\
                '3. The new portfolio composition is compared with the previous one and weights are formed for each stock. '\
                'The algorithm for the formation of weights takes into account the state of the market as a whole and' \
                'selects the most suitable weighing mode. \n '\
                'The whole procedure is fully automatic and takes place after the end of the auction on the last day of the month. '\
                'On the first trading day of the month, the user must call the desired portfolio through the menu and buy stocks,' \
                'indicated in the diagram. \n \n '\
                '\U00002757 __User can buy stocks with a delay of a couple of days, but this will affect' \
                'investment result. Therefore, it is preferable to buy the portfolio on the first trading day of the month. '\
                'The portfolio rebalancing procedure must be carried out monthly to achieve' \
                'matching results .__'

instruction28 = '__ Rating Model Methodology__ \n \n' \
                'The new assessment model consists of two parts: financial and statistical ratings. \nFinancial assessment' \
                'is produced using financial data from the official SEC database and takes into account the' \
                'exclusively financial performance of companies. \nStatistical evaluation is performed using' \
                'price data from Refinitiv. Historical risk premiums are determined for a specific stock and '\
                'are compared with current financial estimates. '\
                'A composite rating is displayed based on the comparison. \n' \
                'A key feature of the Upsilon ranking is that earnings data is processed' \
                'in such a way as to avoid misstatements due to accounting tricks. Information can and will be '\
                'differ from any data you can find in common stock screeners. '\
                'The differences in the data are solely due to the fact that Upsilon processes data about the financial' \
                'state so as to restore the real position of the company. \nUpsilon fundamentally does not carry out' \
                'evaluating companies based on smart beta factors, momentum, patterns and sentiment. If you ' \
                'I wonder why factors don\'t matter, but why data recovery is important,' \
                'then more detailed articles are available under the links \n' \
                '[Financial Analysis Problems] (https://telegra.ph/Problemy-finansovogo-analiza-04-04) \n \n' \
                '[Relationship between corporate lifecycle and smart beta factors] (https://telegra.ph/Vzaimosvyaz-mezhdu-zhiznennyj-ciklom-korporacij-i-smart-beta-faktorami-04-05) \n \n'


instruction34 = '__How to use stock ratings? __ \n \n' \
                'The rating is built taking into account the fact that the user does not know how or does not know how to manage the risk. '\
                'Upsilon portfolios use different risk management algorithms, so no need to be surprised' \
                'the emergence of high-risk companies in portfolios. Upsilon knows exactly what he is doing. \n \n '\
                'The company\'s valuation changes during reporting periods and during periods of change' \
                'modes of volatility. Therefore, any estimates should be considered exclusively within the monthly '\
                'interval. That is, the company can be as attractive as you want in the current month, '\
                'but that may change in the future. Therefore, after the company reports, the rating should be clarified. \n '\
                '⚠️ Some companies submit reports to the SEC with a long delay, therefore the financial rating' \
                'after reports may contain inaccuracies.' \
                'In any case, a portfolio based on ratings should be' \
                'rebalance at least once a quarter, so' \
                'How financial information significantly affects the growth prospects of stocks. Should not feed '\
                'hopes that by choosing a company this month, you can forget about your investment for a year. \n \n '\
                '\U00002757 when you are rating companies using any model or rating provider,' \
                'then the portfolio cannot be long-term without changing its composition. Any ratings and ratings may '\
                'change often enough. Therefore, at least once a month, every 1st day of the month, watch out for that, '\
                'so that the rating for the selected shares remains positive. \n \n' \
                '__Technical rating interpretation: __ \n' \
                '⭐️⭐️⭐️ - high probability that the stock will be more profitable than the index️ \n' \
                '⭐️⭐️- moderate probability that the stock will outperform the index️ \n' \
                '⭐️- the profitability of the stock will be commensurate with the index \n️' \
                '-The probability that the stock will make losses or, at best, will bring less,' \
                'than the index of profitability \n' \
                '__Interpretation of financial rating: __ \n' \
                '🟢 - prosperous companies with high growth potential \n' \
                '🟡 - stable companies with moderate growth potential \n' \
                '🔴 - speculative or highly volatile companies,' \
                'whose growth potential depends on randomness \n \n️️' \

instruction29 = 'Do you have a collaboration or promotional offer? We will consider them with interest. '\
                'Just write us a message! Sample message: / adv TEXT of a sentence. '

instruction30 = 'Have you noticed a bug or have you got a request for Upsilon? Just write me a message! '\
                'sample message: / bug TEXT of the message.'

ranking_v3 = {
    'rank_type':
        {
            # 'Bagger': '__Type: __ 🛫 Startup - a company at the initial stage of its life cycle \n',
            # 'Growth': '__Type: __ ✈ Growth - a company in the stage of stable growth \n',
            # 'Value': '__Type: __ 🛬 Value - the company has passed the peak of its life cycle \n',
            # 'NonType': '__Type: __ 🛸 the company is not classified \n',
            # 'NoData': '__Type: __ 🔎 no data to analyze \n'
            'Bagger': '\n',
            'Growth': '\n',
            'Value': '\n',
            'NonType': '\n',
            'NoData': '\n'
        },
    'nopat':
        {
            2: '__Current financial position of the company: __ \n'
               '\U0001F537 is profitable and profit has increased in the last quarter \n',
            1: '__Current financial position of the company: __ \n'
               '\U0001F536 is profitable, but profit declined in the last quarter \n',
            0: '__Current financial position of the company: __ \n'
               '\U0001F536 suffered a loss in the last quarter, but previously saw profit \n',
            -1: '__Current financial position of the company: __ \n'
                '\U0001F53B is unprofitable and losses have increased \n',
            None: '\n'
        },
    'profitability':
        {
            1: '\U0001F537 uses its assets effectively, including credit funds'
               'to create profit \n',
            0: '\U00002666 is unprofitable or ineffectively using its assets and loan funds \n',
            None: '\n'
        },
    'delta_profitability':
        {
            1: '\U0001F537 operating income increases, business profitability increases \n',
            0: '\U00002666 operating income falls or losses increase,'
               'business profitability is declining \n',
            None: '\n'
        },
    'roic':
        {
            1: '\U0001F537 the funds invested in the company\'s activities have brought profit \n',
            0: '\U00002666 funds invested in the company\'s activities do not bring profit. '
               'The capital costs and / or investments of the company are not profitable. If it\'s a mature company, '
               'then this is a sign that the company is dying out, that is, it has moved from the Value to the Decline phase. \n',
            None: '\n'
        },
    'delta_shareholders_equity':
        {
            1: '\U0001F537 equity capital increased. If the company is profitable, then '
               'this is a positive development. If the company is unprofitable, then an additional issue of shares was implemented \n ',
            0: '\U00002666 Equity has decreased. May have been produced '
               'dividend payments in excess of the company\'s current profit \n',
            None: '\n'
        },
    'margin':
        {
            1: '\U0001F537 margin increased. Last quarter sales brought more profit \n ',
            0: '\U00002666 business marginality declined in the last quarter. Last quarter sales'
               'brought less profit \n',
            None: '\n'
        },
    'net_liquidity':
        {
            1: '\U0001F537 has sufficient liquidity and is able to pay in full'
               'short-term liabilities \n',
            0: '\U00002666 is experiencing liquidity problems. Difficulties may be observed with '
               'payments on short-term liabilities \n',
            None: '\n'
        },
    'improving_net_liquidity':
        {
            1: '\U0001F537 liquidity increased, cash increased \n',
            0: '\U00002666 liquidity decreased, cash flow decreased \n',
            None: '\n'
        },
    'decrease_in_receivables':
        {
            1: '\U0001F537 Decrease in receivables. The company controls deliveries and imposes'
               'own terms for mutual settlements. Potential insolvency risks are low \n ',
            0: '\U00002666 Growth in accounts receivable. This phenomenon can increase the risks of insolvency. '
               'The company lends to its customers, which results in a freeze of part of the working capital \n',
            None: '\n'
        },
    'leverage1':
        {
            1: '\U0001F537 leverage is within normal limits \n',
            0: '\U00002666 is funded by a debt or debt issue. '
               'Large leverage can lead to volatile profits due to interest payments. '
               'If the company is young and increasing sales, then the debt situation is normal. If a '
               'the company is not in the stage of development and sales growth, then the company is potentially problematic \n',
            None: '\n'
        },
    'leverage0':
        {
            1: '\U0001F537 leverage has decreased \n',
            0: '\U00002666 leverage increased \n',
            None: '\n'
        },
    'interest_coverage':
        {
            1: '\U0001F537 has sufficient profit to service obligations,'
               'scheduled for the current fiscal year \n',
            0: '\U00002666 has no profit in the last quarter or the current profit is not enough to service'
               'commitments planned for this fiscal year. Too high debt load in '
               'compared with current income, there may be problems with payments on current obligations \n',
            None: '\n'
        },
    'revenue_estimate_ttm1':
        {
            1: '__Expectations and projections: __ \n'
               '\U0001F537 __increase__ of the sales growth rate during the current quarter \n',
            0: '__Expectations and predictions: __ \n'
               '\U00002666 __decreasing__ of the sales growth rate in the current quarter \n',
            None: '\n'
        },
    'revenue_estimate_ttm2':
        {
            1: '\U0001F537 __increase__ of the sales growth rate in the next quarter \n',
            0: '\U00002666 __decreasing__ sales growth rate in the next quarter \n',
            None: '\n'
        },
    'eps_estimate_ttm1':
        {
            1: '\U0001F537 __increase__ of the net profit growth rate during the current quarter \n',
            0: '\U00002666 __decrease__ of the growth rate of net profit in the current quarter \n',
            None: '\n'
        },
    'eps_estimate_ttm2':
        {
            1: '\U0001F537 __increase__ of the growth rate of net profit in the next quarter \n',
            0: '\U00002666 __decrease__ in the growth rate of net profit in the next quarter \n',
            None: '\n'
        },

    'cash_dividends_paid':
        {
            1: '__ Attitude towards shareholders: __ \n'
               '\U0001F4B5 pays dividends. This is an indirect sign of a mature and stable company \n ',
            0: '__ Attitude towards shareholders: __ \n'
               '\U0000267B the company does not pay dividends \n',
            None: '\n'
        },
    'D_issued':
        {
            1: '\U0001F537 is repurchasing shares positively \n',
            0: '\U0001F536 implements an additional issue of shares, that is, it is funded through sales of its own'
               'shares. If the company is developing, then this situation is acceptable. If '
               'the company has systematic problems, sales decline, then this situation is negative \n',
            None: '\n'
        },
    'rank':
        {
            0: '\U000026D4 no data to evaluate or extremely poor business conduct. '
               'You cannot invest in this company! \n',
            1: '\U0001F534 extremely poor business conduct. '
               'You cannot invest in this company! \n',
            2: '\U0001F534 extremely poor business conduct. '
               'You cannot invest in this company! \n',
            3: '\U0001F534 extremely poor business conduct. '
               'You cannot invest in this company! \n',
            4: '\U0001F534 poor business conduct. '
               'Investing in this company is not recommended! \n',
            5: '\U0001F534 poor business conduct. '
               'Investing in this company is not recommended! \n',
            6: '\U0001F7E1 rating is typical for a relatively stable business. '
               'It is possible to consider this company for investment \n',
            7: '\U0001F7E1 rating is typical for a relatively stable business. '
               'It is possible to consider this company for investment \n',
            8: '\U0001F7E1 average rating is typical for a stable business. '
               'This company should be considered for investment \n',
            9: '\U0001F7E1 average rating is typical for stable business. '
               'This company should be considered for investment \n',
            10: '\U0001F7E1 average rating is typical for stable business. '
               'This company should be considered for investment \n',
            11: '\U0001F7E2 high score indicates a stable company with financial strength. '
                'Good investment candidate! \n',
            12: '\U0001F7E2 high score indicates a stable company with financial strength. '
                'Good investment candidate! \n',
            13: '\U0001F7E2 high score indicates a stable company with financial strength. '
                'Good investment candidate! \n',
            14: '\U0001F7E2 high score indicates a stable company with financial strength. '
                'Good investment candidate! \n',
            15: '\U0001F7E2 high score indicates a stable company with financial strength. '
                'Good investment candidate! \n',
            16: '\U0001F7E2 high score indicates a stable company with financial strength. '
                'Good investment candidate! \n',
            None: '\n'
        },
    'other_rank':
        {
            0: '\U000026D4 no data to evaluate or extremely poor business conduct. '
               'You cannot invest in this company! \n',
            1: '\U0001F534 extremely poor business conduct. '
               'Investing in this company is not recommended! \n',
            2: '\U0001F534 extremely poor business conduct. '
               'Investing in this company is not recommended! \n',
            3: '\U0001F534 extremely poor business conduct. '
               'Investing in this company is not recommended! \n',
            4: '\U0001F7E1 average rating is typical for a relatively stable business \n',
            5: '\U0001F7E1 average rating is typical for relatively stable business \n',
            6: '\U0001F7E1 average rating is typical for relatively stable business \n',
            7: '\U0001F7E1 average is typical for relatively stable business \n',
            8: '\U0001F7E1 high score indicates a stable company with financial strength. '
               'Likely investment candidate! \n',
            9: '\U0001F7E2 high score indicates a stable company with financial strength. '
               'Likely investment candidate! \n',
            10: '\U0001F7E2 high score indicates a stable company with financial strength. '
               'Likely investment candidate! \n',
            11: '\U0001F7E2 high score indicates a stable company with financial strength. '
               'Likely investment candidate! \n',
            12: '\U0001F7E2 high score indicates a stable company with financial strength. '
                'Likely investment candidate! \n',
            None: '\n'
        }

}

all_seasons_s = '__All Season S vs SPY __ \n \n' \
               '__CAGR__ 11.19% vs 9.39% \n' \
               '__Sharpe__ 1.16 vs 0.6 \n' \
               '__Sortino__ 2 vs 0.89 \n' \
               '__Max Drawdown__ -17.67% vs -50.80% \n' \
               '__Volatility__ 8.75% vs 15.45% \n' \
               '__Skew__ -0.51 vs -0.63 \n' \
               '__Kurtosis__ 1.78 vs 1.47 \n' \
               '__cVaR__ -4.79% vs -10.04% \n' \
               '__Best Year__ 28.16% vs 32.31% \n' \
               '__Worst Year__ -8.14% vs -36.81% \n' \
               '__Beta__ 0.42 vs - \n' \
               '__Alpha__ 6.72% vs -'

all_seasons_m = '__All Season M vs SPY __ \n' \
               '__CAGR__ 12.35% vs 9.39% \n' \
               '__Sharpe__ 1.08 vs 0.6 \n' \
               '__Sortino__ 1.83 vs 0.89 \n' \
               '__Max Drawdown__ -27.11% vs -50.80% \n' \
               '__Volatility__ 10.49% vs 15.45% \n' \
               '__Skew__ -0.44 vs -0.63 \n' \
               '__Kurtosis__ 1.3 vs 1.47 \n' \
               '__cVaR__ -5.97% vs -10.04% \n' \
               '__Best Year__ 30.00% vs 32.31% \n' \
               '__Worst Year__ -16.58% vs -36.81% \n' \
               '__Beta__ 0.61 vs - \n' \
               '__Alpha__ 6.05% vs -'

all_seasons_l = '__All Season L vs SPY __ \n' \
               '__CAGR__ 13.46% vs 9.39% \n' \
               '__Sharpe__ 1.05 vs 0.6 \n' \
               '__Sortino__ 1.77 vs 0.89 \n' \
               '__Max Drawdown__ -32.12% vs -50.80% \n' \
               '__Volatility__ 11.84% vs 15.45% \n' \
               '__Skew__ -0.41 vs -0.63 \n' \
               '__Kurtosis__ 0.89 vs 1.47 \n' \
               '__cVaR__ -6.90% vs -10.04% \n' \
               '__Best Year__ 33.55% vs 32.31% \n' \
               '__Worst Year__ -20.65% vs -36.81% \n' \
               '__Beta__ 0.7 vs - \n' \
               '__Alpha__ 6.27% vs -'

instruction31 = '\U0001F4BC __All Seasons__ \n \n' \
                'All Seasons portfolios are passive, low risk and rebalanced annually. '\
                'The goal of the All Seasons S portfolio is stable results, low volatility (risk) and minimal' \
                'possible drawdown while maintaining profitability at the level of the broad market (SPY). '\
                'The portfolio consists only of ETFs, most of the funds are distributed between' \
                'the technology, consumer and health sectors. The rest of the funds are distributed between '\
                'funds for long-term US bonds, gold and commodities. Due to this distribution of funds' \
                'high stability of the portfolio is achieved in any macroeconomic environment. \n \n' \
                '__Advantages: __ \n' \
                '\U0001F537 minimum possible drawdown for a passive portfolio of this type \n' \
                '\U0001F537 higher long-term profitability compared to SPY \n' \
                '\U0001F537 stable capital growth \n \n' \
                '__ Who is All Seasons S suitable for? __ \n' \
                '\U0001F537 you need a calm and passive portfolio that does not require frequent maintenance and' \
                'attention \n' \
                '\U0001F537 if you are focused on the profitability of the broad market, but not even ready for medium risks. \n \n' \
                '__When to buy All Seasons S? __ \n' \
                '\U0001F537 on any trading day other than explosive capital gains. \n '\
                'In this case, you should wait for the portfolio to return to average growth rates. \n' \
                '\U0000267B __ Portfolio rebalancing is performed annually on any day during the period' \
                'from 20 to 30 December__'

instruction32 = '\U0001F4BC __All Seasons__ \n \n' \
                'All All Seasons portfolios are passive, low risk and rebalanced annually. '\
                'The goal of the All Seasons M portfolio is stable results, low volatility (risk) and significant' \
                'lower drawdown while maintaining profitability at the level of the broad market (SPY). '\
                'The portfolio consists only of ETFs, most of the funds are distributed between' \
                'the technology, consumer and health sectors. The rest of the funds are distributed between '\
                'funds for long-term US bonds, gold and commodities. Due to this distribution of funds' \
                'high stability of the portfolio is achieved in any macroeconomic environment. \n \n' \
                '__Advantages: __ \n' \
                '\U0001F537 2 times less drawdown compared to the broad market (SPY) \n' \
                '\U0001F537 higher yield versus broad market (SPY) \n' \
                '\U0001F537 stable capital growth \n \n' \
                '__ Who is All Seasons M suitable for? __ \n' \
                '\U0001F537 you need a calm and passive portfolio that does not require frequent maintenance and' \
                'attention \n' \
                '\U0001F537 if you are looking for higher returns than the broader market and ready for' \
                'medium risks. \n \n' \
                '__When to buy All Seasons M? __ \n' \
                '\U0001F537 on any trading day other than explosive capital gains. \n '\
                'In this case, you should wait for the portfolio to return to average growth rates. \n' \
                '\U0000267B __ Portfolio rebalancing is performed annually on any day during the period' \
                'from 20 to 30 December__'

instruction33 = '\U0001F4BC __All Seasons__ \n \n' \
                'All All Seasons portfolios are passive, low risk and rebalanced annually. '\
                'The goal of the All Seasons L portfolio is stable results, low volatility (risk) and significant' \
                'smaller drawdown while maintaining profitability at the level of the broad market (SPY). '\
                'The portfolio consists only of ETFs, most of the funds are distributed between' \
                'the technology, consumer and health sectors. The rest of the funds are distributed between '\
                'long-term US bond funds and the broad market (SPY). Due to this distribution of funds' \
                'high stability of the portfolio is achieved in any macroeconomic environment. \n \n' \
                '__Advantages: __ \n' \
                '\U0001F537 drawdown is significantly less compared to the broad market (SPY) \n' \
                '\U0001F537 highest yield versus broad market (SPY) for portfolios' \
                'like this \n' \
                '\U0001F537 low volatility (risk) \n' \
                '\U0001F537 stable capital growth \n \n' \
                '__ Who is All Seasons L suitable for? __ \n' \
                '\U0001F537 you need a calm and passive portfolio that does not require frequent maintenance and' \
                'attention \n' \
                '\U0001F537 if you are looking for higher returns than the broader market and ready for' \
                'medium risks. \n \n' \
                '__When to buy All Seasons L? __ \n' \
                '\U0001F537 on any trading day other than explosive capital gains. \n '\
                'In this case, you should wait for the portfolio to return to average growth rates. \n' \
                '\U0000267B __ Portfolio rebalancing is performed annually on any day during the period' \
                'from 20 to 30 December__'

passive_investments = 'Passive or index investing is an investment strategy aimed at' \
                      'to maximize profits by minimizing trades. \n' \
                      'Passive investing broadly refers to a buy and hold portfolio strategy for' \
                      'long-term investment horizons with minimal market trade. \n \n' \
                      '\U0001F537 index investing is the most common form of passive investing,' \
                      'where investors seek to replicate and maintain the broad market index. \n' \
                      '\U0001F537 passive investments are cheaper, less complex and often yield good results' \
                      'on long-term periods.'

scenario1 = 'The risk and premium (additional risk return) of your portfolio is greater than that of SPY (broad market),' \
            'and the ratio of the premium to risk is greater. The portfolio is efficient and will bring on average more '\
            'yield than the market. '\
            'You don\'t have to change anything, but if you want you can get the market profitability,' \
            'with less risk (that is, understate the profitability of your portfolio). '\
            'To do this, you need to reduce the amount of investment in your portfolio so that the drawdown' \
            'in the money has become equal to the market.'

scenario1_a = 'The risk and premium (additional risk return) of your portfolio is greater than that of' \
              'SPY (broad market), but the premium to risk ratio is lower. The portfolio is rational and will bring on average '\
              'more profitable than the market. But SPY is more efficient in relation to your portfolio. '\
              'If you buy SPY so that the drawdown in money becomes equal to the drawdown of your portfolio,' \
              'then it will bring more return, with the same risk as your portfolio.'

scenario2 = 'The risk of your portfolio is less than that of SPY (broad market), and the premium (additional return' \
            'for risk) and the ratio of the premium to risk is higher. The portfolio is as efficient as possible. Nothing should be changed. '

scenario2_a = 'The risk of your portfolio is less than that of SPY (broad market), and the premium (additional return' \
            'for risk) is higher, but the ratio of the premium to risk is less than the market one. The portfolio is effective. '\
              'Nothing should be changed.'

scenario3 = 'Your portfolio\'s risk and premium (additional risk return) is less than SPY (broad market),' \
            'and the premium to risk ratio is better. The portfolio is effective, but if you want, you can get more profitability '\
            'market, with the same risk as the market. To do this, you need to increase the amount of investment in your '\
            'a portfolio so that the drawdown in money becomes equal to the market drawdown.'

scenario3_a = 'The risk of your portfolio and its premium (additional return on risk) is less than that of SPY' \
              '(broad market),' \
            'and the ratio of the premium to risk is less than the market one. The portfolio is irrational even for an investor with '\
              'low risk threshold. SPY is more efficient in relation to your portfolio. '\
              'If you buy SPY so that the drawdown in money becomes equal to the drawdown of your portfolio,' \
              'then it will bring more profitability, with the same risk.'

scenario4 = 'The risk of your portfolio is higher than the market one, and its premium (additional return on risk)' \
            'less than SPY (broad market). The portfolio is irrational, '\
            'at least for now. '\
            'At the moment the portfolio has no statistical' \
            'advantages over buying SPY. Either the portfolio item weights or composition should be changed. '

scenario4_a = 'The risk of your portfolio is higher than the market one, and its premium (additional return on risk)' \
            'less than SPY (broad market). The portfolio is irrational and ineffective, '\
            'at least for now. '\
            'At the moment the portfolio has no statistical' \
            'advantages over buying SPY. Either the portfolio item weights or composition should be changed. '

inspector_input = 'You can enter ticker weight in number of pieces, as a percentage (%) or equal to zero, which means' \
                  'that you are entering an equal weighted portfolio. If you start entering weights in one of the three '\
                  'formats, then all other weights should be entered in the same way ❗ \n' \
                  'If you suddenly made a mistake with the ticker weight, you can enter it again with the correct weight and' \
                  'weight value will be corrected! \n \n' \
                  'Enter the ticker and the number of shares in the format: \n' \
                  '! ticker 100 (All weights will be in number of pieces) \n' \
                  '__Example__:! NVDA 100 \n \n' \
                  '! ticker 10% (All weights will be in percent) \n' \
                  '__Example__:! NVDA 10% \n \n' \
                  '! ticker 0 (All tickers will have equal weight) \n' \
                  '__Example__:! NVDA 0 \n \n' \
                  '__ Enter ticker: __'

instruction36 = '__Portfolio Inspector__ is a portfolio analytic tester to identify' \
                'efficiency' \
                'portfolio versus indices and popular ETFs. After analyzing the portfolio, you will receive '\
                'the simple answer if it is better invest or not to invest in this portfolio. \n \n' \
                '[Examples] (https://telegra.ph/Primery-ispolzovaniya-Inspektora-portfelej-04-27) \n \n' \
                'After Upsilon analyzes the portfolio, you will have three charts available: \n \n' \
                '🧩 __ Correlation Matrix__ - needed to evaluate low premium assets that have too much' \
                'strong connection with each other. Such assets should be removed from the portfolio. \n \n '\
                '🏅 __ Premium Chart__ - a diagram that helps to determine risk' \
                'There is a premium for your stock and portfolio. And the color palette and size will let you know '\
                'how effectively your asset deals with the risk. The higher the USharpe ratio is, '\
                'the more the risk is compensated. Between  ' \
                'assets with the same premium and risk levels you should choose an asset with a large' \
                'by the value of the USharpe coefficient. \n \n' \
                '📊 __Comparative diversification histogram__ is a tool for comparing portfolio with' \
                'indices and popular ETFs by diversification level. For example, the diversification level '\
                'equal to 100% in the corresponding ETF column means that the diversification is comparable. '\
                'Values less than 100% indicate that your portfolio is less diversified,' \
                'than the corresponding ETF. A diversification level of more than 100% means that your portfolio is' \
                'more diversified and heavier. The normal level of diversification '\
                'ranges from 60% to 120% can be considered. With a low level of diversification to indices and '\
                'low premium, you are more likely to suffer losses. '\
                'If the level of diversification is too high, the portfolio will become ineffective, that is,' \
                'the index will easily bypass it in terms of profitability and risk. \n \n' \
                'Upsilon gives a direct output at the end of the analysis, so there is no specific need' \
                'to analyze charts! '\
                '[More details about awards] (https://telegra.ph/Kak-pokupat-akcii-chtoby-ne-stat-sponsorom-zombi-i-ne-razoritsya-04-26)'



