import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as st
import math

np.random.RandomState(1)
# Note that np.random.RandomState(1) makes the code's behavior reproducible.


# We first establish a population, from a normal distribution, of size 1000 with mean 0 and standard deviation 1.
pop = np.random.normal(loc=0, scale=1, size=100000)

# Displaying the population.
sns.kdeplot(pop)
plt.show()

print('The mean of the population is {}'.format(pop.mean()))
print("The Z value of the confidence interval 95% is {}".format(st.norm.ppf(.975)))
# 1.96 is the value we get from looking at a table online, which matches the above.

# We will create a function which gives the confidence interval of a particular random sample from pop.

def get_con_interval(sample,level):
    """Takes a sample and a confidence level (a decimal representing a percent),
    then returns a confidence interval as a pair (x,y)."""
    # If the confidence level is, say, 95%, we have alpha = 5%, so alpha/2 = .025.
    margin_of_error = (st.norm.ppf(level+((1-level)/2)))*(sample.std()/math.sqrt(len(sample)))
    return (sample.mean()-margin_of_error,sample.mean()+margin_of_error)

# Let's test if this works.  
sample = np.random.choice(pop, size=36)
print(get_con_interval(sample,.95))
# In the future we will need the left and right endpoints of the interval.  Let's try to select only one of the endpoints.
print(get_con_interval(sample,.95)[0])

# We will compare vs computing manually here.

print("The mean and sample deviation of the sample are {} and {}".format(sample.mean(),sample.std()))

print("The margin of error is {}".format(st.norm.ppf(.975)*(sample.std()/6)))

# Comparing Z values.
print(st.norm.ppf(.975))
print(st.norm.ppf(.025))
print("The interval computed manually is",
      (sample.mean()-st.norm.ppf(.975)*(sample.std()/6),sample.mean()+st.norm.ppf(.975)*(sample.std()/6)))
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

def in_or_out(n, con_level=.95):
    """Takes a number of tests, n, and then generates n samples and confidence intervals (at con_level), collecting the
    number of times the population mean was inside the confidence interval."""
    inside=0
    outside=0
    pop_mean=pop.mean()
    for i in range(n):
        sample=np.random.choice(pop, size=36)
        interval=get_con_interval(sample,con_level)
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

# Testing the above function.
in_or_out(100)

# Testing for 10 different inputs between 1 and 1000.
for i in np.random.choice(range(1000), size=10):
    in_or_out(i)

# Let's compare our method for getting a confidence interval with the one from scipy.

test_sample=np.random.normal(loc=0, scale=1, size=40)
print("Our function finds the interval is",get_con_interval(test_sample,.9))
print("Using scipy the interval is",st.norm.interval(0.9, loc=np.mean(test_sample), scale=np.std(test_sample)/np.sqrt(40)))

# Note that the above only works for large samples (over about 30 elements).  But that was true of our function as well.