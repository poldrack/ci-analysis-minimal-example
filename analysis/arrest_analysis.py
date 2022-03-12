# use merged data to model arrest as function of impulsivity
# vs baseline model of age/sex
import os
import pandas as pd
import statsmodels.api as sm
from lrtest import lrtest


def load_alldata(datadir):
    """load full SRO dataset created by merge_data.py"""
    return(pd.read_csv(os.path.join(datadir, 'alldata.csv')))


def get_impulsivity_variables(alldata, impulsivity_vars=None):
    """get list of variables that are in impulsivity
    or sensation seeking surveys"""

    if impulsivity_vars is None:
        impulsivity_measures = [
            'dickman_survey',
            'upps_impulsivity_survey',
            'sensation_seeking_survey',
            'bis11_survey',
            'impulsive_venture_survey'
        ]
        impulsivity_vars = [
            var
            for var in alldata.columns
            if var.split('.')[0] in impulsivity_measures
        ]

    return(impulsivity_vars)


def select_variables(alldata, baseline_vars=None):
    """get impulsivity variables, arrest variable, and baseline variables"""
    if baseline_vars is None:
        baseline_vars = ['Age', 'Sex']

    alldata = alldata.copy()

    impulsivity_vars = get_impulsivity_variables(alldata)

    # create binary arrest variable
    arrest_var = 'ArrestedChargedLifeCount'
    arrestdata = alldata[impulsivity_vars + baseline_vars + [arrest_var]]
    arrestdata= arrestdata.assign(EverArrested = arrestdata.loc[:, arrest_var] > 0)
    del arrestdata[arrest_var]

    return(arrestdata.dropna())


def model_arrest(arrestdata, baseline_vars=None):
    """run logistic regression on arrest data
    - using both full model and model with only baseline variables"""

    if baseline_vars is None:
        baseline_vars = ['Age', 'Sex']

    y = arrestdata.loc[:, 'EverArrested']
    X = sm.add_constant(arrestdata.drop(columns=['EverArrested']))
    print(X.columns)
    log_reg = sm.Logit(y, X).fit()
    log_reg_baseline = sm.Logit(y, X[['const'] + baseline_vars]).fit()
    return(log_reg, log_reg_baseline)


def write_summary(summary, outfile):
    """write text summary of logistic regression results to text file"""
    with open(outfile, 'w') as f:
        f.write(summary)


def write_lrtest(log_reg, log_reg_baseline, resultsdir):
    """write lrtest results to file"""
    result = lrtest(log_reg, log_reg_baseline)
    with open(os.path.join(resultsdir, 'lrtest.txt'), 'w') as f:
        f.write('Likelihood ratio test results for full model vs baseline:\n')
        f.write(f'Chi-squared: {result[0]}, p = {result[1]}\n')


def save_output(log_reg, log_reg_baseline, resultsdir):
    """save logistic regression results to file"""
    write_summary(log_reg.summary().as_text(), os.path.join(resultsdir, 'log_reg.txt'))
    write_summary(log_reg_baseline.summary().as_text(), os.path.join(resultsdir, 'log_reg_baseline.txt'))
    write_lrtest(log_reg, log_reg_baseline, resultsdir)


if __name__ == "__main__":

    datadir = '../data'
    resultsdir = '../results'

    alldata = load_alldata(datadir)
    arrestdata = select_variables(alldata)

    log_reg, log_reg_baseline = model_arrest(arrestdata)
    save_output(log_reg, log_reg_baseline, resultsdir)
