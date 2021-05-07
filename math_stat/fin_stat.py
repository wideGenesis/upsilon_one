# Copyright 2019, Hudson and Thames Quantitative Research
# All rights reserved
# Read more: https://github.com/hudson-and-thames/mlfinlab/blob/master/LICENSE.txt

# Correlation based distances and various modifications (angular, absolute, squared) described in Cornell lecture notes:
# Codependence: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3512994&download=yes


import numpy as np
import pandas as pd
from scipy.spatial.distance import squareform, pdist
from scipy.stats import norm, spearmanr


# def angular_distance_correlation(returns_=None):
#
#     dist_matrix = fst.get_dependence_matrix(returns_, dependence_method='spearmans_rho')
#     angular_dist_matrix = fst.get_distance_matrix(dist_matrix, distance_metric='angular')
#     return angular_dist_matrix

def spearmans_rho(x: np.array, y: np.array) -> float:
    """
    Calculates a statistical estimate of Spearman's rho - a copula-based dependence measure.

    Formula for calculation:
    rho = 1 - (6)/(T*(T^2-1)) * Sum((X_t-Y_t)^2)

    It is more robust to noise and can be defined if the variables have an infinite second moment.
    This statistic is described in more detail in the work by Gautier Marti
    https://www.researchgate.net/publication/322714557 (p.54)

    This method is a wrapper for the scipy spearmanr function. For more details about the function and its parameters,
    please visit scipy documentation
    https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.stats.spearmanr.html

    :param x: (np.array/pd.Series) X vector.
    :param y: (np.array/pd.Series) Y vector (same number of observations as X).
    :return: (float) Spearman's rho statistical estimate.
    """

    # Coefficient calculationS
    rho, _ = spearmanr(x, y)

    return rho


def get_dependence_matrix(df: pd.DataFrame, dependence_method: str, theta: float = 0.5,
                          n_bins: int = None, normalize: bool = True,
                          estimator: str = 'standard', target_dependence: str = 'comonotonicity',
                          gaussian_corr: float = 0.7, var_threshold: float = 0.2) -> pd.DataFrame:
    """
    This function returns a dependence matrix for elements given in the dataframe using the chosen dependence method.

    List of supported algorithms to use for generating the dependence matrix: ``information_variation``,
    ``mutual_information``, ``distance_correlation``, ``spearmans_rho``, ``gpr_distance``, ``gnpr_distance``,
    ``optimal_transport``.

    :param df: (pd.DataFrame) Features.
    :param dependence_method: (str) Algorithm to be use for generating dependence_matrix.
    :param theta: (float) Type of information being tested in the GPR and GNPR distances. Falls in range [0, 1].
                          (0.5 by default)
    :param n_bins: (int) Number of bins for discretization in ``information_variation`` and ``mutual_information``,
                         if None the optimal number will be calculated. (None by default)
    :param normalize: (bool) Flag used to normalize the result to [0, 1] in ``information_variation`` and
                             ``mutual_information``. (True by default)
    :param estimator: (str) Estimator to be used for calculation in ``mutual_information``.
                            [``standard``, ``standard_copula``, ``copula_entropy``] (``standard`` by default)
    :param target_dependence: (str) Type of target dependence to use in ``optimal_transport``.
                                    [``comonotonicity``, ``countermonotonicity``, ``gaussian``,
                                    ``positive_negative``, ``different_variations``, ``small_variations``]
                                    (``comonotonicity`` by default)
    :param gaussian_corr: (float) Correlation coefficient to use when creating ``gaussian`` and
                                  ``small_variations`` copulas. [from 0 to 1] (0.7 by default)
    :param var_threshold: (float) Variation threshold to use for coefficient to use in ``small_variations``.
                                  Sets the relative area of correlation in a copula. [from 0 to 1] (0.2 by default)
    :return: (pd.DataFrame) Dependence matrix.
    """


    # Get the feature names
    features_cols = df.columns.values
    n = df.shape[1]
    np_df = df.values.T  # Make columnar access, but for np.array

    # Defining the dependence function
    if dependence_method == 'spearmans_rho':
        dep_function = spearmans_rho
    else:
        raise ValueError(f"{dependence_method} is not a valid method. Please use one of the supported methods \
                            listed in the docstring.")

    # Generating the dependence_matrix
    dependence_matrix = np.array([
        [
            dep_function(np_df[i], np_df[j]) if j < i else
            # Leave diagonal elements as 0.5 to later double them to 1
            0.5 * dep_function(np_df[i], np_df[j]) if j == i else
            0  # Make upper triangle 0 to fill it later on
            for j in range(n)
        ]
        for i in range(n)
    ])

    # Make matrix symmetrical
    dependence_matrix = dependence_matrix + dependence_matrix.T

    #  Dependence_matrix converted into a DataFrame
    dependence_df = pd.DataFrame(data=dependence_matrix, index=features_cols, columns=features_cols)

    return dependence_df


def get_distance_matrix(X: pd.DataFrame, distance_metric: str = 'angular') -> pd.DataFrame:
    """
    Applies distance operator to a dependence matrix.

    This allows to turn a correlation matrix into a distance matrix. Distances used are true metrics.

    List of supported distance metrics to use for generating the distance matrix: ``angular``, ``squared_angular``,
    and ``absolute_angular``.

    :param X: (pd.DataFrame) Dataframe to which distance operator to be applied.
    :param distance_metric: (str) The distance metric to be used for generating the distance matrix.
    :return: (pd.DataFrame) Distance matrix.
    """

    if distance_metric == 'angular':
        distfun = lambda x: ((1 - x).round(5) / 2.) ** .5
    elif distance_metric == 'absolute_angular':
        distfun = lambda x: ((1 - abs(x)).round(5) / 2.) ** .5
    else:
        raise ValueError(f'{distance_metric} is a unknown distance metric. Please use one of the supported methods \
                            listed in the docstring.')

    return distfun(X).fillna(0)


def angular_distance(x: np.array, y: np.array) -> float:
    """
    Returns angular distance between two vectors. Angular distance is a slight modification of Pearson correlation which
    satisfies metric conditions.

    Formula used for calculation:

    Ang_Distance = (1/2 * (1 - Corr))^(1/2)

    Read Cornell lecture notes for more information about angular distance:
    https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3512994&download=yes.

    :param x: (np.array/pd.Series) X vector.
    :param y: (np.array/pd.Series) Y vector.
    :return: (float) Angular distance.
    """
    corr_coef = np.corrcoef(x, y)[0][1]
    return np.sqrt(0.5 * (1 - corr_coef))


def absolute_angular_distance(x: np.array, y: np.array) -> float:
    """
    Returns absolute angular distance between two vectors. It is a modification of angular distance where the absolute
    value of the Pearson correlation coefficient is used.

    Formula used for calculation:

    Abs_Ang_Distance = (1/2 * (1 - abs(Corr)))^(1/2)

    Read Cornell lecture notes for more information about absolute angular distance:
    https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3512994&download=yes.

    :param x: (np.array/pd.Series) X vector.
    :param y: (np.array/pd.Series) Y vector.
    :return: (float) Absolute angular distance.
    """

    corr_coef = np.corrcoef(x, y)[0][1]
    return np.sqrt(0.5 * (1 - abs(corr_coef)))


# def distance_correlation(x: np.array, y: np.array) -> float:
#     """
#     Returns distance correlation between two vectors. Distance correlation captures both linear and non-linear
#     dependencies.
#
#     Formula used for calculation:
#
#     Distance_Corr[X, Y] = dCov[X, Y] / (dCov[X, X] * dCov[Y, Y])^(1/2)
#
#     dCov[X, Y] is the average Hadamard product of the doubly-centered Euclidean distance matrices of X, Y.
#
#     Read Cornell lecture notes for more information about distance correlation:
#     https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3512994&download=yes.
#
#     :param x: (np.array/pd.Series) X vector.
#     :param y: (np.array/pd.Series) Y vector.
#     :return: (float) Distance correlation coefficient.
#     """
#
#     x = x[:, None]
#     y = y[:, None]
#
#     x = np.atleast_2d(x)
#     y = np.atleast_2d(y)
#
#     a = squareform(pdist(x))
#     b = squareform(pdist(y))
#
#     A = a - a.mean(axis=0)[None, :] - a.mean(axis=1)[:, None] + a.mean()
#     B = b - b.mean(axis=0)[None, :] - b.mean(axis=1)[:, None] + b.mean()
#
#     d_cov_xx = (A * A).sum() / (x.shape[0] ** 2)
#     d_cov_xy = (A * B).sum() / (x.shape[0] ** 2)
#     d_cov_yy = (B * B).sum() / (x.shape[0] ** 2)
#     coef = np.sqrt(d_cov_xy) / np.sqrt(np.sqrt(d_cov_xx) * np.sqrt(d_cov_yy))
#     return coef


def tail_var(returns=None, confidence=0.99, days=21):
    # Generate Var-Cov matrix
    ticker_cov = returns.cov()
    ticker_mean = returns.mean()
    ticker_dev = np.sqrt(ticker_cov)
    var = norm.ppf(1 - confidence, ticker_mean, ticker_dev)

    # Calculate n Day VaR
    var_array = []
    num_days = int(days)
    for x in range(1, num_days + 1):
        var_array.append(np.round(var * np.sqrt(x), 2))
        print(str(x) + f" day VaR @ {confidence*100}% confidence: " + str(np.round(var * np.sqrt(x), 2)))
    # Build plot


def skew(returns):
    """
    calculates returns' skewness
    (the degree of asymmetry of a distribution around its mean)
    """
    return returns.skew()


def ulcer_index(returns, rf=0):
    """ calculates the ulcer index score (downside risk measurment) """
    dd = 1. - returns/returns.cummax()
    return np.sqrt(np.divide((dd**2).sum(), returns.shape[0] - 1))


def ulcer_performance_index(returns, rf=0):
    """
    calculates the ulcer index score
    (downside risk measurment)
    """
    dd = 1. - returns/returns.cummax()
    ulcer = np.sqrt(np.divide((dd**2).sum(), returns.shape[0] - 1))
    return returns.mean() / ulcer
