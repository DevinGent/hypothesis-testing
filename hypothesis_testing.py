import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import math

# We first establish a population, from a normal distribution, of size 1000 with mean 0 and standard deviation 1.
pop = np.random.default_rng(1).normal(loc=0, scale=1, size=1000)
# Note that default_rng(1) makes the random choice reproducible.

sns.kdeplot(pop)
plt.show()

print('The mean of the population is {}'.format(pop.mean()))

# This will allow us to pratice using hypothesis testing.  First we will consider a large two-tailed test of the population mean.
# We will use a Z test.
# We will use a 5% level of significance.
# The rejection region is cut off by +/- the z-score corresponding to .025, which is 
# (-inf, -1.960] and [1.960,inf)
# The null hypothesis is that the mean is 0, the alternative hypothesis is that the mean is different (higher or lower) than 0.

sample = np.random.default_rng(1).choice(pop, size=35)
sample_mean =sample.mean()
sample_std = sample.std()

zscore= (sample_mean)/(sample_std/(math.sqrt(35)))
print("The Z-score is {}".format(zscore))
print(len(sample))

# Now let us do this multiple times and see what happens.

def get_zscore(sample, pop_mean):
    """Returns the zscore of the given sample based on the population mean."""
    return (sample.mean()-pop_mean)/(sample.std()/(math.sqrt(len(sample))))
    

# Test this function.
print("The Z-score using our function is {}".format(get_zscore(sample, 0)))

reject=0
do_not_reject=0
tests=0
for i in range(100000):
    test_sample= np.random.default_rng(i).choice(pop, size=35)
    test_zscore = get_zscore(test_sample,pop.mean())
    tests=tests+1
    if test_zscore<=-1.96 or test_zscore >= 1.96:
        reject=reject+1
    else:
        do_not_reject=do_not_reject+1

print("After collecting samples {} times,".format(tests))
print("the null hypothesis was rejected {} times, and failed to be rejected {} times.".format(reject, do_not_reject))