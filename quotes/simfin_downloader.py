import simfin as sf
from simfin.names import *

sf.set_api_key('free')

# Set the local directory where data-files are stored.
# The dir will be created if it does not already exist.
sf.set_data_dir('~/simfin_data/')


# Daily Share-Prices.
df_cap = sf.load_shareprices(variant='daily', market='us')


# Print the first rows of the data.
print(df_cap.iloc(500))


# Print all Revenue and Net Income for Microsoft (ticker MSFT).
print(df_cap.loc['MSFT', [CLOSE, SHARES_OUTSTANDING]])

























