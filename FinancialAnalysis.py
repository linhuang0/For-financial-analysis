import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
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


# roll two dice for multiple times
die = pd.DataFrame([1, 2, 3, 4, 5, 6])
sum_of_dice = die.sample(2, replace=True).sum().loc[0]
print('Sum of dice is', sum_of_dice)  

# you may get different outcomes as we now mimic the result of rolling 2 dice, but the range must be limited between 2 and 12. 

# It is your turn! let's replace the none with the code of rolling three dice, instead of two

np.random.seed(1)  # This is for checking answer, do NOT modify this line of code

#Modify the code, replace the None
sum_of_three_dice = None
print('Sum of three dice is', sum_of_three_dice)

# The following code mimics the roll dice game for 50 times. And the results are all stored into "Result"
# Lets try and get the results of 50 sum of faces.

trial = 50
result = [die.sample(2, replace=True).sum().loc[0] for i in range(trial)]


#print the first 10 results
print(result[:10])

# To recall, this is the code to mimic the roll dice game for 50 times

die = pd.DataFrame([1, 2, 3, 4, 5, 6])
trial = 50
results = [die.sample(2, replace=True).sum().loc[0] for i in range(trial)]

# This is the code for summarizing the results of sum of faces by frequency

freq = pd.DataFrame(results)[0].value_counts()
sort_freq = freq.sort_index()
print(sort_freq)

#plot the bar chart base on the result

sort_freq.plot(kind='bar', color='blue', figsize=(15, 8))
# Using relative frequency, we can rescale the frequency so that we can compare results from different number of trials
relative_freq = sort_freq/trial
relative_freq.plot(kind='bar', color='blue', figsize=(15, 8))
# assume that we have fair dice, which means all faces will be shown with equal probability
# then we can say we know the 'Distribtuion' of the random variable - sum_of_dice

X_distri = pd.DataFrame(index=[2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
X_distri['Prob'] = [1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1]
X_distri['Prob'] = X_distri['Prob']/36
X_distri
mean = pd.Series(X_distri.index * X_distri['Prob']).sum()
var = pd.Series(((X_distri.index - mean)**2)*X_distri['Prob']).sum()
#Output the mean and variance of the distribution. Mean and variance can be used to describe a distribution
print(mean, var)

# if we calculate mean and variance of outcomes (with high enough number of trials, eg 20000)...
trial = 20000
results = [die.sample(2, replace=True).sum().loc[0] for i in range(trial)]
#print the mean and variance of the 20000 trials
results = pd.Series(results)
print(results.mean(), results.var())

# let play around with ms data by calculating the log daily return
ms['LogReturn'] = np.log(ms['Close']).shift(-1) - np.log(ms['Close'])
# Plot a histogram to show the distribution of log return of Microsoft's stock. 
# You can see it is very close to a normal distribution
from scipy.stats import norm
mu = ms['LogReturn'].mean()
sigma = ms['LogReturn'].std(ddof=1)

density = pd.DataFrame()
density['x'] = np.arange(ms['LogReturn'].min()-0.01, ms['LogReturn'].max()+0.01, 0.001)
density['pdf'] = norm.pdf(density['x'], mu, sigma)

ms['LogReturn'].hist(bins=50, figsize=(15, 8))
plt.plot(density['x'], density['pdf'], color='red')
plt.show()


##Calculate the probability of the stock price will drop over a certain percentage in a day
# probability that the stock price of microsoft will drop over 5% in a day
prob_return1 = norm.cdf(-0.05, mu, sigma)
print('The Probability is ', prob_return1)

##Calculate the probability of the stock price will drop over a certain percentage in a year
# drop over 40% in 220 days
mu220 = 220*mu
sigma220 = (220**0.5) * sigma
print('The probability of dropping over 40% in 220 days is ', norm.cdf(-0.4, mu220, sigma220))

# drop over 20% in 220 days
mu220 = 220*mu
sigma220 = (220**0.5) * sigma
drop20 = norm.cdf(-0.2, mu220, sigma220)
print('The probability of dropping over 20% in 220 days is ', drop20)

##Calculate Value at risk (VaR)
# Value at risk(VaR)
VaR = norm.ppf(0.05, mu, sigma)
print('Single day value at risk ', VaR)