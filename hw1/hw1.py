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



if __name__ == '__main__':		
	main()





