import pandas as pd
import matplotlib.pyplot as plt
# import the data of Facebook and Microsoft
import os
os.getcwd()
fb = pd.read_csv('/Users/mac/Documents/GitHub/For-financial-analysis//Files/facebook.csv',index_col=0)
ms = pd.read_csv('/Users/mac/Documents/GitHub/For-financial-analysis//Files/microsoft.csv',index_col=0)
# run this cell to ensure Microsoft's stock data is imported
print(ms.iloc[0, 0])
print(fb.head())
# print head of ms, 1 line
print(ms.head())
print(fb.shape)
# print summary statistics of Facebook
print(fb.describe())
# print the shape of ms, 1 line
print(ms.shape)
# print summary statistics of Microsoft
print(ms.describe())
# select all the price information of Facebook in 2016.
fb_2015 = fb.loc['2015-01-01':'2015-12-31']
# print the price of Facebook on '2015-03-16'
print(fb_2015.loc['2015-03-16'])
# select all the price information of Microsoft in 2016.
ms_2016=ms.loc['2016-01-01':'2016-12-31']
# print the price of Microsoft on '2016-03-16'
print(ms_2016.loc['2016-03-16'])
# print the opening price of the first row
print(fb.iloc[0, 0])
# print the opening price of the last row
print(ms.iloc[779,0])
plt.figure(figsize=(10, 8))
fb['Close'].plot()
plt.show()
plt.figure(figsize=(10, 8))
# plot only the Close price of 2016 of Microsoft, 1 line 
ms_2016['Close'].plot()
plt.show()
fb.index
fb.tail()
fb.describe()
fb.loc['2015-03-16'].plot()


##Create a new column in the DataFrame (1) - Price difference¶
#Create a new column PriceDiff in the DataFrame fb
fb['PriceDiff'] = fb['Close'].shift(-1) - fb['Close']
#Your turn to create PriceDiff in the DataFrame ms
ms['PriceDiff'] = ms['Close'].shift(-1) - ms['Close']
#Run this code to display the price difference of Microsoft on 2015-01-05
print(ms['PriceDiff'].loc['2015-01-05'])

##Create a new column in the DataFrame (2) - Daily return¶
#Daily Return is calcuated as PriceDiff/Close
#Create a new column Return in the DataFrame fb
fb['Return'] = fb['PriceDiff'] /fb['Close']
#Your turn to create a new column Return in the DataFrame MS
ms['Return'] = ms['PriceDiff'] /ms['Close']
#Run this code to print the return on 2015-01-05
print(ms['Return'].loc['2015-01-05'])


##Create a new column in the DataFrame using List Comprehension - Direction
#Create a new column Direction. 
#The List Comprehension means : if the price difference is larger than 0, denote as 1, otherwise, denote as 0,
#for every record in the DataFrame - fb
fb['Direction'] = [1 if fb['PriceDiff'].loc[ei] > 0 else 0 for ei in fb.index ]
# Your turn to create a new column Direction for MS
ms['Direction'] = [1 if ms['PriceDiff'].loc[ei] > 0 else 0 for ei in ms.index ]
# Run the following code to show the price difference on 2015-01-05
print('Price difference on {} is {}. direction is {}'.format('2015-01-05', ms['PriceDiff'].loc['2015-01-05'], ms['Direction'].loc['2015-01-05']))


##Create a new column in the DataFrame using Rolling Window calculation (.rolling()) - Moving average
fb['ma50'] = fb['Close'].rolling(50).mean()

#plot the moving average
plt.figure(figsize=(10, 8))
fb['ma50'].loc['2015-01-01':'2015-12-31'].plot(label='MA50')
fb['Close'].loc['2015-01-01':'2015-12-31'].plot(label='Close')
plt.legend()
plt.show()

# You can use .rolling() to calculate any numbers of days' Moving Average. This is your turn to calculate "60 days"
# moving average of Microsoft, rename it as "ma60". And follow the codes above in plotting a graph

ms['ma60'] = ms['Close'].rolling(60).mean()

#plot the moving average
plt.figure(figsize=(10, 8))
ms['ma60'].loc['2015-01-01':'2015-12-31'].plot(label='MA60')
ms['Close'].loc['2015-01-01':'2015-12-31'].plot(label='Close')
plt.legend()
plt.show()


#1. Munging the stock data and add two columns - MA10 and MA50
#import FB's stock data, add two columns - MA10 and MA50
#use dropna to remove any "Not a Number" data
fb['MA10'] = fb['Close'].rolling(10).mean()
fb['MA50'] = fb['Close'].rolling(50).mean()
fb = fb.dropna()
fb.head()

#2. Add "Shares" column to make decisions base on the strategy
#Add a new column "Shares", if MA10>MA50, denote as 1 (long one share of stock), otherwise, denote as 0 (do nothing)
fb['Shares'] = [1 if fb.loc[ei, 'MA10']>fb.loc[ei, 'MA50'] else 0 for ei in fb.index]
#Add a new column "Profit" using List Comprehension, for any rows in fb, if Shares=1, the profit is calculated as the close price of 
#tomorrow - the close price of today. Otherwise the profit is 0.

#Plot a graph to show the Profit/Loss

fb['Close1'] = fb['Close'].shift(-1)
fb['Profit'] = [fb.loc[ei, 'Close1'] - fb.loc[ei, 'Close'] if fb.loc[ei, 'Shares']==1 else 0 for ei in fb.index]
fb['Profit'].plot()
plt.axhline(y=0, color='red')

#3. Use .cumsum() to display our model's performance if we follow the strategy
#Use .cumsum() to calculate the accumulated wealth over the period

fb['wealth'] = fb['Profit'].cumsum()
fb.tail()
#plot the wealth to show the growth of profit over the period

fb['wealth'].plot()
plt.title('Total money you win is {}'.format(fb.loc[fb.index[-2], 'wealth']))
