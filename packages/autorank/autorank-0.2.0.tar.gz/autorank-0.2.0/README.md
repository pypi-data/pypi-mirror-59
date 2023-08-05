# autorank

## Summary

Autorank is a simple Python package with one task: simplify the comparison between (multiple) paired populations. 
The package basically implements Demsar's guidelines for the the comparison of classifiers. This package provides the single function 
`autorank` which automatically determines suitable statistical tests, confidence intervals, etc. based on the normality and homogeneity of 
the data. 

## Installation

Autorank is available on PyPi and can be installed using pip.

```
pip install autorank
```

## Description

Autorank uses the following strategy for the statistical comparison of paired populations:
- First all populations are checked with the Shapiro-Wilk test for normality. We use Bonferoni correction for these
  tests, i.e., alpha/#populations.
- If all columns are normal, we use Bartlett's test for homogeneity, otherwise we use Levene's test.
- Based on the normality and the homogeneity, we select appropriate tests, effect sizes, and methods for determining
  the confidence intervals of the central tendency.

If all columns are normal, we calculate:
- The mean value as central tendency.
- The empirical standard deviation as measure for the variance.
- The confidence interval for the mean value.
- The effect size in comparison to the highest mean value using Cohen's d.

If at least one column is not normal, we calculate:
- The median as central tendency.
- The median absolute deviation from the median as measure for the variance.
- The confidence interval for the median.
- The effect size in comparison to the highest ranking approach using Cliff's delta.

For the statistical tests, there are four variants:
- If there are two populations and both populations are normal, we use the paired t-test.
- If there are two populations and at least one populations is not normal, we use Wilcoxon's signed rank test.
- If there are more than two populations and all populations are normal and homoscedastic, we use repeated measures
  ANOVA with Tukey's HSD as post-hoc test.
- If there are more than two populations and at least one populations is not normal or the populations are
  heteroscedastic, we use Friedman's test with the Nemenyi post-hoc test.
  
We use the paired t-test, the Wilcoxon signed rank test, and the Friedman test from [scipy](https://www.scipy.org/). The
repeated measures ANOVA and Tukey's HSD test (including the calculation of the confidence intervals) are used from
[statsmodels](statsmodels). We use own implementations for the calculation of critical distance of the Nemenyi test,
the calculation of the effect sizes, and the calculation of the confidence intervals (with the exception of Tukey's
HSD).  
  
## Usage Example

The following example shows the usage of `autorank`.
```python
import numpy as np
import pandas as pd
from autorank.autorank import autorank

np.random.seed(42)
pd.set_option('display.max_columns', 7)
std = 0.3
means = [0.2, 0.3, 0.5, 0.8, 0.85, 0.9]
sample_size = 50
data = pd.DataFrame()
for i, mean in enumerate(means):
    data['pop_%i' % i] = np.random.normal(mean, std, sample_size).clip(0, 1)
res = autorank(data, alpha=0.05)
print(res)
```

The code yields the following output (added some newlines for better readability of this README).
```
Rejecting null hypothesis that data is normal for column pop_0 (p=0.000016<0.008333)
Fail to reject null hypothesis that data is normal for column pop_1 (p=0.060517>=0.008333)
Fail to reject null hypothesis that data is normal for column pop_2 (p=0.138845>=0.008333)
Rejecting null hypothesis that data is normal for column pop_3 (p=0.000100<0.008333)
Rejecting null hypothesis that data is normal for column pop_4 (p=0.000002<0.008333)
Rejecting null hypothesis that data is normal for column pop_5 (p=0.000002<0.008333)
Using Levene's test for homoscedacity of non-normal data.
Fail to reject null hypothesis that all variances are equal (p=0.266318>=0.050000)
Using Friedman test as omnibus test
Rejecting null hypothesis that there is no difference between the distributions (p=0.000000)
Using Nemenyi post-hoc test.
Differences are significant, if the distance between the mean ranks is greater than the critical distance.
RankResult(rankdf=
       meanrank    median       mad  ci_lower  ci_upper  effect_size    mangitude
pop_5      2.18  0.912005  0.130461  0.692127         1  2.66454e-17   negligible
pop_4      2.29  0.910437  0.132786  0.654001         1       -0.024   negligible
pop_3      2.47  0.858091  0.210394  0.573879         1       0.1364   negligible
pop_2      3.95  0.505057  0.333594  0.227184   0.72558       0.6424        large
pop_1      4.71  0.313824  0.247339  0.149473  0.546571       0.8516        large
pop_0      5.40  0.129756  0.192377         0  0.349014       0.9192        large
pvalue=2.3412212612346733e-28,
cd=1.0662484349869374,
omnibus='friedman',
posthoc='nemenyi',
all_normal=False,
pvals_shapiro=[1.646607051952742e-05, 0.0605173334479332, 0.13884511590003967, 0.00010030837438534945,
               2.066387423838023e-06, 1.5319776593969436e-06],
homoscedastic=True,
pval_homogeneity=0.2663177301695518,
homogeneity_test='levene')
```

You can also use Autorank to generate a plot that visualizes the statistical analysis. Autorank creates plots of the
confidence interval in case of the paired t-test and repeated measures ANOVA and a critical distance diagram for the
post-hoc Nemenyi test. 

```python
from autorank.autorank import plot_stats

plot_stats(res)
```

For the above example, the following plot is created:
![CD Diagram](example/cd_diagram.png)

You can also get a report in natural language about the results of the statistical tests. 
```python
import matplotlib.pyplot as plt
from autorank.autorank import create_report

create_report(res)
plt.show()

```

For example, the following report is created for the example above:

> The statistical analysis was conducted for 6 populations with 50 paired samples.
We rejected the null hypothesis that the population is normal for the populations pop_5, pop_2, pop_1, and pop_0 (adjusted alpha=0.008333). Therefore, we assume that not all populations are normal.
We reject the null hypothesis (alpha=0.050000) of the Friedman test that there is no difference in the central tendency of the populations pop_5 (MD=0.912005, MAD=0.130461), pop_4 (MD=0.910437, MAD=0.132786), pop_3 (MD=0.858091, MAD=0.210394), pop_2 (MD=0.505057, MAD=0.333594), pop_1 (MD=0.313824, MAD=0.247339), and pop_0 (MD=0.129756, MAD=0.192377). Therefore, we assume that there is a statistically significant difference between the median values of the populations.
Based the post-hoc Nemenyi test, we assume that there are no significant differences within the following groups: pop_5, pop_4, and pop_3; pop_2 and pop_1; pop_1 and pop_0. All other differences are significant.


## Planned Features

The core of Autorank is finished. The next potential feature would be the generation of the report in Latex, that
combines (and extends) the current report generation functions. 

## License

Autorank is published under the Apache 2.0 Licence.
