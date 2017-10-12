import sys
import numpy as np
import pandas as pd
import scipy
import matplotlib
import math
from scipy import stats

## Main entry point
def main():
	
	# q1()
	q2()


	return

## Question (1)
def q1():

	np.random.seed(1234)

	n = 1000

	# Part (a)
	# ########
	# k (shape) = 100, theta (scale) = 1
	# 	mean = k*theta = 100*1 = 100	
	# 	std dev = theta*sqrt(k) 1*sqrt(100) = 10
	# 	var = k*(theta**2)
	a_k, a_theta = 100, 1
	a_samples = np.random.gamma(a_k, a_theta, n)	
	a_mu, a_var, a_sigma = np.mean(a_samples), np.var(a_samples), np.std(a_samples)
	print("part (a) sample mean: ", a_mu)
	print("part (a) sample variance: ", a_var)
	print("part (a) sample std dev: ", a_sigma)

	# Part (b)
	# ########
	# k (shape) = 1, theta (scale) = 100
	# 	mean = k*theta = 1*100 = 100	
	# 	std dev = theta*sqrt(k) = 100*sqrt(1) = 100
	# 	var = k*(theta**2)
	b_k, b_theta = 1, 100
	b_samples = np.random.gamma(b_k, b_theta, n)	
	b_mu, b_var, b_sigma = np.mean(b_samples), np.var(b_samples), np.std(b_samples)
	print("part (b) sample mean: ", b_mu)
	print("part (b) sample variance: ", b_var)	
	print("part (b) sample std dev: ", b_sigma)

	# Part (c)	
	# ########
	a_interval = stats.norm.interval(0.95, loc=a_mu, scale=a_sigma/np.sqrt(n))
	b_interval = stats.norm.interval(0.95, loc=b_mu, scale=b_sigma/np.sqrt(n))
	print("Part (a) 95% C.I.:", a_interval)
	print("Part (b) 95% C.I.:", b_interval)

	# Part (d)
	# ########
	# relative error	

	# Part (e)
	# ########
	# Recall for hypothesis testing, let 
	# 	H_o: null hypothesis 
	# 	H_a: alternative hypothesis
	# Then our Type I and Type II error are given by:
	# 	Type I: Reject H_o, given true H_o
	# 	Type II: Fail to reject H_o, given true H_a
	#
	# Recall power is the probability of correctly rejecting the null hypothesis. Define:
	#		alpha = P(Type I Error) = P(Reject H_o | H_o true) (error)
	#		1 - alpha = 1 - P(Type I Error) = P(Fail to reject H_o | H_o true) (correct)
	#		beta = P(Type II Error) = P(Fail to reject H_o | H_a true) (error)	
	# 	1 - beta = Power = 1 - P(Type II) = P(Reject H_o | H_o true) (correct)
	#
	# Effect size: mean of treatment - mean of control
	#
	# Rule of Thumb for sample size with 95% C.I. and desired power 80%:
	# n = 16*var / delta**2
	#
	# Where delta is the sensitivity, or the amount of change we want to detect (effect size)
	# 	--> in this case we are given delta = 10%
	delta = 0.1
	#
	# So, for the Part (a) distribution we would need a sample size of appx:
	a_n = math.ceil((16*a_var) / (delta**2))
	print("Part (a) experiment sample size:", a_n)	
	# 
	# And for the Part (b) distribution we would need a sample size of appx:
	b_n = math.ceil((16*b_var) / (delta**2))
	print("Part (b) experiment sample size:", b_n)

	# Part (f)
	# ########
	#	Assuming a constant rate of receiving data points in an AB test, so
	# for example, if we assume that we receive 1 data point per second,
	# then we would have to run the experiment on distribution (a) for almost 2 days:
	minutes, seconds = divmod(a_n, 60)	
	hours, minutes = divmod(minutes, 60)
	days, hours = divmod(hours, 24)
	print("Part (a) time:", days, "days", hours, "hours,", minutes, "minutes,", seconds, "seconds")

	# We would have to run the experiment on distribution (b) for about 161 days:
	minutes, seconds = divmod(b_n, 60)	
	hours, minutes = divmod(minutes, 60)
	days, hours = divmod(hours, 24)
	print("Part (b) time:", days, "days", hours, "hours,", minutes, "minutes,", seconds, "seconds")

	# Therefore, we would have to run the experiment for about 159 days longer on 
	# distribution (b) than on distribution (a) to get the same confidence:
	diff = b_n - a_n	
	minutes, seconds = divmod(diff, 60)	
	hours, minutes = divmod(minutes, 60)
	days, hours = divmod(hours, 24)
	print("Time difference:", days, "days", hours, "hours,", minutes, "minutes,", seconds, "seconds")


def q2():

	# Increase viewed rows
	pd.set_option('display.max_rows', 1000)

	# Read data	
	X = pd.read_csv('Expense_Budget.csv', low_memory=False)

	# Restrict to police department
	budgets_by_dept = X[X['Agency Name'] == 'POLICE DEPARTMENT']

	# Separate by year
	budgets_2017 = budgets_by_dept[budgets_by_dept['Fiscal Year'] == 2017]
	budgets_2018 = budgets_by_dept[budgets_by_dept['Fiscal Year'] == 2018]

	### (a)		

	# Group by Budget Code Name and sum by budget code's data
	budgets_grouped_2017 = budgets_2017[['Adopted Budget Amount', 'Budget Code Name']].groupby('Budget Code Name').sum().reset_index()
	budgets_grouped_2018 = budgets_2018[['Adopted Budget Amount', 'Budget Code Name']].groupby('Budget Code Name').sum().reset_index()

	# Join data for each year
	yearly_budget = budgets_grouped_2017.set_index('Budget Code Name').join(budgets_grouped_2018.set_index('Budget Code Name'), lsuffix=' 2017', rsuffix=' 2018')

	# To simplify, drop items that don't appear in each year
	yearly_budget = yearly_budget.dropna(axis=0, how='any')

	# Take differences between years
	bud_2017 = yearly_budget['Adopted Budget Amount 2017']
	bud_2018 = yearly_budget['Adopted Budget Amount 2018']
	yearly_budget['YoY Change'] = bud_2018 - bud_2017

	# View results
	# yearly_budget

	### (b)	

	# Restrict by Budget and Budget Code Name
	items_2017 = budgets_2017[['Adopted Budget Amount', 'Budget Code Name']]
	items_2018 = budgets_2018[['Adopted Budget Amount', 'Budget Code Name']]

	# Join data for each year
	items_yearly_budget = items_2017.set_index('Budget Code Name').join(items_2018.set_index('Budget Code Name'), lsuffix=' 2017', rsuffix=' 2018')

	# To simplify, drop items that don't appear in each year
	items_yearly_budget = items_yearly_budget.dropna(axis=0, how='any')

	# Take differences between years
	i_2017 = items_yearly_budget['Adopted Budget Amount 2017']
	i_2018 = items_yearly_budget['Adopted Budget Amount 2018']
	items_yearly_budget['YoY Change'] = i_2018 - i_2017

	# View results
	# items_yearly_budget

	## There are some weird things going on with the specific budget items.  There are too many
	## constant quantities within 2018, and 2017 all the specific items are constant.  Need to
	## think about the effect this is having on overestimating overall budget YoY
	
	return 

## Question 3

## Question 4
# (a) The difference between the "Push" and "Pull" workflow for getting data to people
# basically, for a data-driven company, these are the two primary strategies for 
# getting data into the hands of decision makers:  
#
# 	The "Push" strategy involves sending out or pushing out data to people, such that 
# 	the sender is choosing what information is important.  

#		The "Pull" strategy involves providing tools and access to data to pull
# 	people in, and then let decision makers access whatever data they deem important.

# In terms of email reports, dashboards, and slack message bots and how they fit into these
# categories: 
#		Email reports are pretty clearly a "Push" strategy in that the sender is choosing what 
#		data to send out via email.  Dashboards on the other hand are pretty clearly a "Pull"
#		strategy in that you create a dashboard, make lots of data available in a meaningful
# 	way, and then let users access the data they helps them make decisions. Finally, Slack
# 	Bots I would say are primarily a "Push" strategy as you set up the bot to send out
#		notifications or updates directly to users in slack, thus selecting what data is important.
#		At the same time, however, Slack Bots can also provide a "Pull" strategy in that the whole
#		purpose of bots is to provide and instant response mechanism for questions, etc. Therefore,
#		by allowing users to ask questions to a Slack Bot in order to access data, this represents
#		a "Pull" strategy (obviously restricted by the bot's response capabilities, but "Pull" nonetheless).
#		Furthermore, I would argue that, in reality, all three of these can have elements of both
#		"Push" and "Pull"—-as I've already exhibited with Slack Bots.  For email reports, you can 
# 	include links to additional data sets, etc which the readers can then choose whether or not
#		to access if they see it as important.  For dashboards, you could send out push notifications
#		at time-intervals or on an event-driven basis, for instance, to employ a "Push" strategy.
#
#
#	(b) If an author is producing a lot of content, it might be better to have a simple dashboard
# because dashboard reporting, as just discussed, in inherently a "Pull" strategy.  In other words,
#	it is more effective to allow the users to determine what data is important rather than decide for them.
# Therefore, when there is a lot of content, a simple dashboard that describes the performance 
# of each item might be better because the user isn't overwhelmed with an enormous amount of content
# upfront, but can instead view the high-level performance of individual items, and dig into detailed
# data for items they deem important, as the "Pull" strategy encourages.  Providing too detailed of 
# data tables describing all items together could likely distort the importance of performance data
#	for individual items. 
#
# (c) When you are sending data to a manager, it is likely because the manager has requested the data
#	and is already interested in the data.  Also, sending is inherently a "Push" strategy so as the sender,
# you are deciding what information is important. Therefore, it might be safer to send a very detailed data
# table to the manager, because you know they are interested in this data, and you are indicating what data
# you find important--it would be bad to leave out something that the manager might want to see.
# Alternatively, for their reports, reporting is a "Pull" strategy, and therefore, it again might be better
# to leave your reporting to more high-level data, and let decision makers dig more into data they find important
# rather than potentially obscuring key performance data with too much other noisy data. 

## Question 5
# See react_dashboard.tar 

if __name__ == '__main__':		
	main()





