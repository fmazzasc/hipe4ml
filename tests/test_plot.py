"""
Module used to test the plot functions
"""

import matplotlib
import pandas as pd
import xgboost as xgb
import numpy as np
from sklearn import datasets
from sklearn.model_selection import train_test_split
from hipe4ml import analysis_utils
from hipe4ml import plot_utils
from hipe4ml.model_handler import ModelHandler

# data preparation
DIGITS_DATA = datasets.load_digits(n_class=2)
DIGITS = pd.DataFrame(DIGITS_DATA.data[:, 0:10])     # pylint: disable=E1101
Y_DIGITS = DIGITS_DATA.target       # pylint: disable=E1101
SIG_DF = DIGITS[Y_DIGITS == 1]
BKG_DF = DIGITS[Y_DIGITS == 0]
TRAIN_SET, TEST_SET, Y_TRAIN, Y_TEST = train_test_split(
    DIGITS, Y_DIGITS, test_size=0.5, random_state=42)
DATA = [TRAIN_SET, Y_TRAIN, TEST_SET, Y_TEST]
# --------------------------------------------

# training and testing
INPUT_MODEL = xgb.XGBClassifier()
MODEL = ModelHandler(INPUT_MODEL)
MODEL.train_test_model(DATA)
Y_PRED = MODEL.predict(DATA[2])
EFFICIENCY, THRESHOLD = analysis_utils.bdt_efficiency_array(DATA[3], Y_PRED, n_points=10)
# --------------------------------------------


def test_plot_distr():
    """
    Test the feature distribution plot
    """
    assert isinstance(plot_utils.plot_distr(
        [SIG_DF, BKG_DF], SIG_DF.columns), np.ndarray)


def test_plot_corr():
    """
    Test the correlation matrix plot
    """
    assert isinstance(plot_utils.plot_corr(
        [SIG_DF, BKG_DF], SIG_DF.columns), list)


def test_plot_roc():
    """
    Test the roc curve plot
    """
    assert isinstance(plot_utils.plot_roc(DATA[3], Y_PRED), matplotlib.figure.Figure)


def test_plot_precision_recall():
    """
    Test the precision recall plot
    """
    assert isinstance(plot_utils.plot_precision_recall(
        DATA[3], Y_PRED), matplotlib.figure.Figure)


def test_plot_feature_imp():
    """
    Test the feature importance plot
    """
    assert isinstance(plot_utils.plot_feature_imp(
        DATA[0], DATA[1], MODEL, 50), list)


def test_plot_bdt_output():
    """
    Test the test-training bdt output plot
    """
    assert isinstance(plot_utils.plot_output_train_test(
        MODEL, DATA), list)


def test_plot_bdt_efficiency():
    """
    Test the bdt efficiency plot
    """
    assert isinstance(plot_utils.plot_bdt_eff(THRESHOLD, EFFICIENCY),
                      matplotlib.figure.Figure)
