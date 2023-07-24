import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as st
import math

# We first establish a population, from a normal distribution, of size 1000 with mean 0 and standard deviation 1.
pop = np.random.default_rng(1).normal(loc=0, scale=1, size=100000)
# Note that default_rng(1) makes the random choice reproducible.

sns.kdeplot(pop)
plt.show()

print('The mean of the population is {}'.format(pop.mean()))
print("The Z value of the confidence interval 95% is {}".format(st.norm.ppf(.975)))
# 1.96 is the value we get from looking at a table online.

# We will create a function which gives the confidence interval of a particular random sample from pop.

def get_con_interval(sample,level):
    """Takes a sample and a confidence level (a decimal representing a percent),
    then returns a confidence interval as a pair (x,y)."""
    # If the confidence level is, say, 95%, we have alpha = 5%, so alpha/2 = .025.
    margin_of_error = (st.norm.ppf(level+((1-level)/2)))*(sample.std()/math.sqrt(len(sample)))
    return (sample.mean()-margin_of_error,sample.mean()+margin_of_error)

# Let's test if this works.  
sample = np.random.default_rng(1).choice(pop, size=36)
print(get_con_interval(sample,.95))
print(get_con_interval(sample,.95)[0])
# We will compare vs computing manually here.

print("The mean and sample deviation of the sample are {} and {}".format(sample.mean(),sample.std()))

print("The margin of error is {}".format(st.norm.ppf(.975)*(sample.std()/6)))
# The function seems to be working correctly.
# We will take many samples, and see how many of the confidence intervals (at 95%) obtained contain the population mean.
inside=0
outside=0
pop_mean=pop.mean()
number_of_tests = 100
for i in range(number_of_tests):
    sample=np.random.default_rng(i).choice(pop, size=36)
    interval=get_con_interval(sample,.95)
    if pop_mean<interval[0] or pop_mean>interval[1]:
        outside=outside+1
    elif pop_mean>=interval[0] and pop_mean<=interval[1]:
        inside=inside+1
    else:
        print("There was an issue on test number {}".format(i))

print("After running the test {} times,".format(number_of_tests))
print("the population mean was inside the interval {} times and outside {} times.".format(inside,outside))

# We will create a function from the above code so we can test at whatever number of tests we like, again and again.

def in_or_out(n):
    """Takes a number of tests, n, and then generates n samples and confidence intervals, collecting the
    number of times the population mean was inside the confidence interval."""
    inside=0
    outside=0
    pop_mean=pop.mean()
    for i in range(n):
        sample=np.random.default_rng(i).choice(pop, size=36)
        interval=get_con_interval(sample,.95)
        if pop_mean<interval[0] or pop_mean>interval[1]:
            outside=outside+1
        elif pop_mean>=interval[0] and pop_mean<=interval[1]:
            inside=inside+1
        else:
            print("There was an issue on test number {}".format(i))
    print("After running the test {} times,".format(n))
    print("the population mean was inside the interval {} times and outside {} times.".format(inside,outside))
    success_percent = round(100*(inside/n),2)
    print("That is, the population mean was inside the interval {}% of the time.".format(success_percent))

in_or_out(100)
# This matches the above.

for i in np.random.default_rng(1).choice(range(1000), size=10):
    in_or_out(i)
