import streamlit as st
import pandas as pd
from pycoingecko import CoinGeckoAPI
from datetime import datetime, timedelta

cg = CoinGeckoAPI()

# Place wsb image lol
url = 'https://sccaid.com/wp-content/uploads/2021/07/elon-' \
      'musk-noi-dogecoin-nhanh-hon-bitcoin-va-ethereum.jpg'
st.image(url, caption='Buy Low, Sell High')

st.write("""
# Crypto Calculator
Use the options in the sidebar to set your parameters for:
- Date You Wished You'd Bought
- Amount in USD You'd Wished You Invested
""")
st.write('---')

# Also display title in the sidebar
st.sidebar.title('Crypto Calculator')
option = st.sidebar.selectbox('Select Your Crypto :', ('BTC', 'ETH', 'DOGE'))

# Create a dictionary of crypto for selection
coins = {'BTC': 'bitcoin',
         'ETH': 'ethereum',
         'DOGE': 'dogecoin'}

current_price = cg.get_price(ids=coins[option],
                       vs_currencies='usd')[coins[option]]['usd']

# Date & Amount selection options
st.sidebar.write('Choose Date and Amount')
today = datetime.utcnow().date()
previous_day = today - timedelta(days=1)

HIST_DATE = st.sidebar.date_input('Date : ',
                                  value=previous_day,
                                  min_value=datetime(2014, 1, 1),
                                  max_value=previous_day)

ORG_USD = st.sidebar.number_input('USD Amount : ',
                                  min_value=1,
                                  max_value=999999999)

# Reformat Historical Date for next function
HIST_DATE_REFORMAT = HIST_DATE.strftime('%d-%m-%Y')
HIST_DATE_datetime = datetime.strptime(HIST_DATE_REFORMAT, '%d-%m-%Y')
coin_historic = cg.get_coin_history_by_id(id=coins[option],
                                          vs_currencies='usd',
                                          date=HIST_DATE_REFORMAT)['market_data']['current_price']['usd']

coin_historic = round(coin_historic, 5)

st.write('# Results')
st.write('## If You\'d Bought on {} :'.format(HIST_DATE_REFORMAT))
st.write('You would have bought: ***{:,.2f}*** ${}'.format(round((ORG_USD/coin_historic), 5),
                                                                      option))
st.write('At a price of ***{:,.9f}*** per ${}'.format(coin_historic,
                                                      option))

st.write('## As of Today on {} :'.format(today.strftime('%d-%m-%Y')))
total = ORG_USD/coin_historic
current_USD = total * current_price
perc_change = (current_USD - ORG_USD)/(ORG_USD)*100
usd_diff = current_USD - ORG_USD

st.write('That is worth: ***${:,.2f}***'.format(round(current_USD, 2)))
st.write('Which is a percentage change of ***{:,.2f}%***'.format(round(perc_change, 2)))

if usd_diff == 0:
   st.write('# You Broke Even')
elif usd_diff <= 0:
   st.write('# You Would Have Lost')
else:
   st.write('# You Missed Out On')
st.write('***${:,.2f}!!!***'.format(abs(round(usd_diff, 2))))

# Get prices from historical date up till now
now = datetime.now()
historical_prices = cg.get_coin_market_chart_range_by_id(id=coins[option],
                                                         vs_currency='usd',
                                                         from_timestamp=HIST_DATE_datetime.timestamp(),
                                                         to_timestamp=now.timestamp())['prices']

# Iterate and append prices and dates into a list and make a dictionary to create dataframe
dates = []
prices = []

for x,y in historical_prices:
  dates.append(x)
  prices.append(y)

dictionary = {'Prices': prices, 'Dates': dates}
df = pd.DataFrame(dictionary)
df['Dates'] = pd.to_datetime(df['Dates'],
                             unit='ms',
                             origin='unix')

# Plot line chart of prices against dates using dataframe
st.write('# {}'.format(option))
# Display current price
st.write('*Current Price :*', current_price)
st.line_chart(df.rename(columns={'Dates': 'index'}).set_index('index'))



