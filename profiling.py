### INSTRUCTIONS:
# python3 profiling.py "[filename].csv"
###

import pandas as pd
import matplotlib.pyplot as plt
import sys

# build dataframe from csv
testfile = sys.argv[1]
f = open(testfile)
data = []
hour = -1
lines = f.readlines()
for i, line in enumerate(lines):
    if line == '\n':
        N_lines = i + 2
        break
for i, line in enumerate(lines):
    if i == 1:
        cols = line.split(',')
    mod = i % N_lines
    if mod == 0:
        hour += 1
    if mod not in [0, 1, N_lines-2, N_lines-1]:
        lst = line.split(',')
        if '/' in lst[0]:
            lst0 = lst[0].split('/')
            lst[0] = (int(lst0[0]) + int(lst0[1])) // 2
        else:
            lst[0] = int(lst[0])
        for j in range(1,len(lst)-1):
            lst[j] = float(lst[j])
        lst.insert(0, hour)
        data.append(lst)
cols.insert(0, 'hour')
cols[-1] = 'function'
df = pd.DataFrame(data, columns=cols)

# scatter plot of hour vs. function completion time for all data
plt.scatter(df['hour'], df['tottime'])
xlab = 'Time since program started (hours)'
ylab = 'Function completion time (seconds)'
plt.xlabel(xlab)
plt.ylabel(ylab)
plt.title(testfile + ': All Functions')
plt.savefig(testfile + '_all_scatter.png')
# plot shows (maybe) 1 function with linear completion time

# find the problem function
problems = df[df['tottime']>5]['function']
print(problems)
# appears to be all one function

if len(problems) == 0:
    longer = df[df['tottime']>1]['function']
    print('No problems!')
    print(df.loc[longer.index[-1]]['function'])
    littleLonger = df[df['tottime']<1]
    littleLonger = littleLonger[littleLonger['tottime']>.15]['function']
    print(df.loc[littleLonger.index[-1]]['function'])
    exit()

#the function
problem = df.loc[problems.index[-1]]['function']

# df of only problem function
dfProb = df[df['function'] == problem]

# df of everything else
dfGood = df[df['function'] != problem]

# plot everything else
plt.figure()
plt.scatter(dfGood['hour'], dfGood['tottime'])
plt.xlabel(xlab)
plt.ylabel(ylab)
plt.title(testfile + ': Constant time functions')
plt.savefig(testfile + '_good_functions.png')
# one outlier --> remove
print(dfGood[dfGood['tottime'] > 7])
dfg2 = dfGood[dfGood['tottime'] < 7]
plt.figure()
plt.scatter(dfg2['hour'], dfg2['tottime'])
plt.xlabel(xlab)
plt.ylabel(ylab)
plt.title(testfile + ': Constant time functions, outlier removed')
plt.savefig(testfile + '_good_functions_no_outlier.png')
# now plot is good (no other linear time complexities)

# plot problem function
print(dfProb[dfProb['function'] != problem])
plt.figure()
plt.scatter(dfProb['hour'], dfProb['tottime'])
plt.xlabel(xlab)
plt.ylabel(ylab)
plt.title(testfile + ': Linear time function (problematic)')
plt.savefig(testfile + '_problem_function.png')

# this is it
print(problem)