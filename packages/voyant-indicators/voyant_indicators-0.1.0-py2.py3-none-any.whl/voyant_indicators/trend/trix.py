
import pandas as pd

from indicators.overlapping_studies.sma import sma
from indicators.overlapping_studies.ema import ema
from indicators.overlapping_studies.wma import wma
from indicators.overlapping_studies.dema import dema
from indicators.overlapping_studies.tema import tema

from indicators.momentum.roc import roc


def trix(df, price, trix, n):
    """
    TRIX is a momentum oscillator that displays the percent rate of change of a
    triple exponentially smoothed moving average.

    Parameters:
        df (pd.DataFrame): DataFrame which contain the asset price.
        price (string): the column name of the price of the asset.
        trix (string): the column name for the rate of change of a triple exponential moving average results.
        n (int): the total number of periods.

    Returns:
        df (pd.DataFrame): Dataframe with the rate of change of a triple exponential moving average of the asset calculated.

    """

    df = ema(df, price, trix + "_ema", n)
    df = ema(df[n - 1 :], trix + "_ema", trix + "_ema_2", n)
    df = ema(df[n - 1 :], trix + "_ema_2", trix + "_ema_3", n)
    df = roc(df, trix + "_ema_3", trix, 1)

    return df
