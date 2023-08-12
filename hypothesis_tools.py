import numpy as np
import scipy.stats as st
import math
import warnings
def get_zscore(sample, pop_mean):
    """Returns the z-score of the given sample (an array like) based on the population mean."""
    if len(sample)<30:
        warnings.warn("Warning: You should usually only use the z-test for large samples (of size 30+)")
    return (sample.mean()-pop_mean)/(sample.std()/(math.sqrt(len(sample))))
# The following tests how the warning message works.
# get_zscore(np.array([3,7,8]),7)

def z_test(sample,popmean,alternative='two-sided', confidence=None):
    """Takes an array_like sample and computes the z-statistic given the null hypothesis popmean.
    Returns a dictionary with two to three entries: the z-statistic, the p-value, and whether to reject the null hypothesis.
    alternative can take three values: 'less' for a left handed test (testing whether the actual population mean
    is less than the null hypothesis popmean), 'more' for a right handed test, and 'two-sided'
    confidence should be a percent written as a decimal."""
    Z=get_zscore(sample,popmean)

    if alternative=='less':
        p= st.norm.cdf(Z)
    elif alternative=='more':
        p=1-st.norm.cdf(Z)
    elif alternative=='two-sided':
        p=(1-st.norm.cdf(abs(Z)))*2
    else:
        raise Exception("alternative must take one of the values 'less', 'more', or 'two-sided'.")

    dict={'z-statistic':Z,'p-value':p}
    
    if confidence!= None:
        if confidence>=0 and confidence<=1:
            if p<=1-confidence:
                reject='reject null'
            else: reject='fail to reject null'
            dict['decision']=reject
        else:
            raise Exception("confidence must be a float between 0 and 1")
    return dict
# Testing st.norm.cdf:
"""
print(2*(1-st.norm.cdf(3.29)))
print(1-st.norm.cdf(2.49))
print(st.norm.cdf(-1.55))
"""