import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from numpy import mean, std
from utils.yf_utils import get_tickers_dataframe
from utils.jdk_rs_utils import rs_ratio, rs_momentum

st.title('Relative Rotation Graph w $SPY benchmark')

AllTickers = ['XLB', 'XLE', 'XLF', 'XLI', 'XLK', 'XLP', 'XLRE', 'XLU', 'XLV', 'XLY']

@st.cache
def load_data():
    
    spdr_tickers = AllTickers + ['RSP']
    
    data = get_tickers_dataframe(tickers=spdr_tickers) 

    prices_df = pd.DataFrame()
    prices_df['XLF'] = data['XLF']['Close']
    prices_df['XLE'] = data['XLE']['Close']
    prices_df['XLB'] = data['XLB']['Close']
    prices_df['XLI'] = data['XLI']['Close']
    prices_df['XLK'] = data['XLK']['Close']
    prices_df['XLP'] = data['XLP']['Close']
    prices_df['XLU'] = data['XLU']['Close']
    prices_df['XLV'] = data['XLV']['Close']
    prices_df['XLY'] = data['XLY']['Close']
    prices_df['XLRE'] = data['XLRE']['Close']
    
    #rs_ratio_df = rs_ratio(prices_df, data['SPY']['Close'])
    rs_ratio_df = rs_ratio(prices_df, data['RSP']['Close'])
    rm_momentum_df = rs_momentum(prices_df)
    
    return rs_ratio_df, rm_momentum_df

ratio, momentum = load_data()

st.subheader('JdK RS-Ratio')
st.dataframe(ratio)

print(ratio.columns)

st.subheader('JdK RS-Momentum')
st.dataframe(momentum)

'''fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

# Move left y-axis and bottim x-axis to centre, passing through (0,0)
ax.spines['left'].set_position('center')
ax.spines['bottom'].set_position('center')

# Eliminate upper and right axes
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')

# Show ticks in the left and lower axes only
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')'''

ratioW = ratio
momentumW = momentum

# Convert the 'Date' index to datetime if it's not already
ratioW.index = pd.to_datetime(ratioW.index)
momentumW.index = pd.to_datetime(momentumW.index)

# Resample the DataFrame to weekly frequency starting from Friday
ratioW_df = ratioW.resample('W-Fri').last()
momentumW_df = momentumW.resample('W-Fri').last()

# Print the resulting DataFrame
print(ratioW_df.head())
print(momentumW_df.head())

# Select columns ending with "_rs_rm"
selected_columns = ratioW_df.filter(regex='_rs_rm$')
ratioCol = ratioW_df.filter(regex='_rs$')
momCol = momentumW_df.filter(regex='_rm$')


fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
# Move left y-axis and bottim x-axis to centre, passing through (0,0)
ax.spines['left'].set_position('center')
ax.spines['bottom'].set_position('center')

# Eliminate upper and right axes
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')

# Show ticks in the left and lower axes only
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')

# Plot scatter plot for each selected column
#for column in selected_columns:
for ticker in AllTickers:
    ratioc = ticker + '_rs'
    momc = ticker + '_rm'
    #ax.scatter(ratioW_df.index, ratioW_df[column], label=column)
    ax.plot(ratioW_df[ratioc], momentumW_df[momc], label=ticker)
    ax.scatter(ratioW_df[ratioc][-1],momentumW_df[momc][-1], marker='o', s=100)

# Add labels and legend to the plot
#ax.xlabel('Date')
#ax.ylabel('Value')
ax.legend()

# Display the plot
plt.show()
















