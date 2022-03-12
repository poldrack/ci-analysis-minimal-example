# likelihood ratio test
# adapted from https://stackoverflow.com/questions/69162676/statsmodels-metric-for-comparing-logistic-regression-models
# - added code to flip the models if the first one is more complex

from scipy.stats.distributions import chi2
from statsmodels.discrete.discrete_model import BinaryResultsWrapper
import typing


def likelihood_ratio(ll0, ll1):
    return -2 * (ll0 - ll1)


def lrtest(fitted_model0: BinaryResultsWrapper,
           fitted_model1: BinaryResultsWrapper) -> typing.Tuple[float, float]:

    # make sure less complex model is model0
    if fitted_model0.df_model > fitted_model1.df_model:
        fitted_model1, fitted_model0 = fitted_model0, fitted_model1

    L0, L1 = fitted_model0.llf, fitted_model1.llf
    df0, df1 = fitted_model0.df_model, fitted_model1.df_model

    chi2_stat = likelihood_ratio(L0, L1)
    p = chi2.sf(chi2_stat, df1 - df0)

    return (chi2_stat, p)
