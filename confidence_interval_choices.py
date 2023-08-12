import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
import scipy.stats as st
import math

# We will see how accurate the confidence percentage is when forming confidence intervals for a normal population.
# Large samples will be drawn from a normal distribution with mean 0 and standard deviation 1.
# A typical sample (of size 40) will look like
# sample = np.random.default_rng(1).normal(loc=0, scale=1, size=40)

# We copy the following functions from confidence_interval_practice with slight alterations rather than importing.

def get_con_interval(sample,level):
    """Takes a sample and a confidence level (a decimal representing a percent),
    then returns a confidence interval as a pair (x,y)."""
    # If the confidence level is, say, 95%, we have alpha = 5%, so alpha/2 = .025.
    if level>1 or level<0:
        raise Exception("The level needs to be written as a decimal.  For a level of 95% input .95")
    margin_of_error = (st.norm.ppf(level+((1-level)/2)))*(sample.std()/math.sqrt(len(sample)))
    return (sample.mean()-margin_of_error,sample.mean()+margin_of_error)

def in_or_out(n,con_level=.95,sample_size=40):
    """Takes a number of tests, n, and then generates n samples of size sample_size and confidence intervals (at con_level), collecting the
    number of times the population mean was inside the confidence interval."""
    inside=0
    outside=0
    pop_mean=0
    for i in range(n):
        sample=np.random.normal(loc=0, scale=1, size=sample_size)
        interval=get_con_interval(sample,.95)
        if pop_mean<interval[0] or pop_mean>interval[1]:
            outside=outside+1
        elif pop_mean>=interval[0] and pop_mean<=interval[1]:
            inside=inside+1
        else:
            print("There was an issue on test number {}".format(i))
    print("After running the test {} times at {}% confidence,".format(n,con_level*100))
    print("the population mean was inside the interval {} times and outside {} times.".format(inside,outside))
    success_percent = round(100*(inside/n),2)
    print("That is, the population mean was inside the interval {}% of the time.".format(success_percent))

def in_or_out_pct(n,con_level=.95,sample_size=40):
    """Takes a number of tests, n, and then generates n samples of size sample_size and confidence intervals (at con_level), collecting the
        number of times the population mean was inside the confidence interval.  Prints nothing."""
    inside=0
    outside=0
    pop_mean=0
    for i in range(n):
        sample=np.random.normal(loc=0, scale=1, size=sample_size)
        interval=get_con_interval(sample,con_level)
        if pop_mean<interval[0] or pop_mean>interval[1]:
            outside=outside+1
        elif pop_mean>=interval[0] and pop_mean<=interval[1]:
            inside=inside+1
        else:
            print("There was an issue on test number {}".format(i))
    return round(100*(inside/n),2)


np.random.RandomState(1)
sample=np.random.normal(loc=0, scale=1, size=31)
print(get_con_interval(sample,.95))
print(sample.mean())


for i in range(100,1100,100):
    in_or_out(i,.95,50)
    print()


x = [i for i in range(10,1010,10)]

y=[in_or_out_pct(n,.95,34) for n in x]

sns.lineplot(x=x, y=y)
plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter())
plt.show()

plt.figure(figsize=(6,4))
sns.lineplot(x=[i for i in range(10,2010,10)], y=[in_or_out_pct(n,.95,32) for n in range(10,2010,10)])
plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter())
plt.show()

# Let us compare different confidence levels and sample sizes.
fig,axs = plt.subplots(3, 2, sharex='all', sharey='all', figsize=(10,6))

sns.lineplot(x=x, y=[in_or_out_pct(n,.90,30) for n in x], ax=axs[0,0])
sns.lineplot(x=x, y=[in_or_out_pct(n,.90,40) for n in x], ax=axs[0,1])
sns.lineplot(x=x, y=[in_or_out_pct(n,.95,30) for n in x], ax=axs[1,0])
sns.lineplot(x=x, y=[in_or_out_pct(n,.95,40) for n in x], ax=axs[1,1])
sns.lineplot(x=x, y=[in_or_out_pct(n,.975,30) for n in x], ax=axs[2,0])
sns.lineplot(x=x, y=[in_or_out_pct(n,.975,40) for n in x], ax=axs[2,1])
for ax in axs.reshape(-1): 
  ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=2))
plt.show()


