import numpy as np
import scipy.stats as st
import math

# We want to be able to quickly and efficient perform t-tests on sample data.  Before using the method in scipy.stats,
# it would be a good idea to test it against the t-test computed manually.

np.random.seed(2)
# To make the choice of a sample the same across multiple executions of this script.

sample=np.random.normal(loc=0, scale=1, size=15)
# We have pulled the sample (of 15 elements) from a normal distribution with mean 0 and standard deviation 1.

# In this script we will assume, throughout, that the null hypothesis is that the population mean=0 (which it actually is). 
#######################################################################################################################
# First we perform a one-sample t-test manually. We will use a left tailed test (i.e. we are testing
# the alternate hypothesis that the popmean<0).

# We first get the test statistic.
T=(sample.mean()-0)/(sample.std()/math.sqrt(len(sample)))
print("We are performing a t-test to test the hypothesis, at the 95% confidence level, that the population mean is < 0.")
print("The t statistic is",T)
print("Online the p-value associated to -0.8716... was 0.19905223 for a left-tailed test with df=14.")
p_value=st.t.cdf(T,df=14)
print("The p-value we find is",p_value)
t_test= st.ttest_1samp(sample,popmean=0,alternative='less')
print(t_test)
# Clearly there is a difference in the t-statistic obtained by the two methods.  Why?
# After researching the problem, it looks as if in obtaining the t-statistic ttest_1samp() uses
# s/sqrt(n-1) as the denominator (the standard error).  Let's try doing the same and see if the answers then match.
T=(sample.mean()-0)/(sample.std()/math.sqrt(len(sample)-1))
p_value=st.t.cdf(T,df=14)
print("On a second attempt, and using n-1 rather than n in the standard error formula, we have")
print('t-stat:',T)
print('p-value:',p_value)
# These now match!

##########################################################################################
# A two-sided and right tailed test should give the same t-stat.  
# We will also verify that they match with how we would find the p-value.
# Right-tailed:
print("For the right-tailed test:",st.ttest_1samp(sample,popmean=0,alternative='greater'))
print("Manually the p-value is",1-st.t.cdf(T,df=14))
print("For the two-sided test:",st.ttest_1samp(sample,popmean=0,alternative='two-sided'))
print("Manually the p-value is",2*(1-st.t.cdf(abs(T),df=14)))