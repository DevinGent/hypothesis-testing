import numpy as np
import scipy.stats as st
# A type I error occurs when a null hypothesis is rejected despite being true.
# The significance level (1-confidence) is the likelihood of committing a type I error.
# In this script we will demonstrate with an example.
np.random.seed(3)

# First we will perform a single two-sided test at 90% confidence to test that the population mean is NOT 0.
sample=np.random.normal(loc=0, scale=1, size=13)
test=st.ttest_1samp(sample,popmean=0)
print(test)
# Note test is a tuple, so to access just the pvalue we can use:
print(test[1])
# Since the p-value is greater than the significance level, .10, we fail to reject the null hypothesis.
# But how often will this happen?  We will perform 100 tests, using 100 different samples, and see how often the 
# null hypothesis is rejected.
N=100
reject=0
for i in range(N):
    sample=np.random.normal(loc=0, scale=1, size=13)
    test=st.ttest_1samp(sample,popmean=0)
    if test[1]<.1:
        reject=reject+1

print("After {} hypothesis tests, the null hypothesis was rejected {} times.".format(N,reject))
print("That is a {}% rejection rate.".format(100*round(reject/N,4)))

# Let's do this a few more times.
N=1000
reject=0
for i in range(N):
    sample=np.random.normal(loc=0, scale=1, size=13)
    test=st.ttest_1samp(sample,popmean=0)
    if test[1]<.1:
        reject=reject+1

print("After {} hypothesis tests, the null hypothesis was rejected {} times.".format(N,reject))
print("That is a {}% rejection rate.".format(100*round(reject/N,4)))

N=10000
reject=0
for i in range(N):
    sample=np.random.normal(loc=0, scale=1, size=13)
    test=st.ttest_1samp(sample,popmean=0)
    if test[1]<.1:
        reject=reject+1

print("After {} hypothesis tests, the null hypothesis was rejected {} times.".format(N,reject))
print("That is a {}% rejection rate.".format(100*round(reject/N,4)))

# We can expect the null hypothesis to be (incorrectly) rejected about 10% of the time.