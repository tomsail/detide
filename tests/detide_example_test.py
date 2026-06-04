import holoviews as hv
import pandas as pd

from detide.constants import SHORT
from detide.constants import FULL
from detide.constants import NOAA

from detide.plotting import plot_df
from detide.plotting import plot_comparative_amplitudes

from detide.detide import pytides_surge
from detide.detide import pytides_get_coefs
from detide.detide import pytides_get_coefs_df
from detide.detide import resample


def test_detide_plots():
    df = pd.read_parquet("tests/data/cuxh.parquet")
    ts = df["elev"] # must be a pd.Series
    ts_hourly = resample(ts) # resample the twl signal for the tidal analysis: faster harmonic analysis

    # compute the surge signal for the 3 sets of tidal constituents
    surges = {}
    for astro, name in zip([SHORT, FULL, NOAA], ["SHORT", "FULL", "NOAA"]):
        coef = pytides_get_coefs(ts_hourly, astro)
        surge = pytides_surge(ts, coef)
        surges[name] = resample(surge) # resample the surge signal: surgeMIP exception

    # plot #1: compare the original signal and the detided signal obtained
    plot_ = plot_df(ts_hourly, "Total Water Level signal", "k") \
        * plot_df(surges["FULL"], "Detided Residual Signal", "r")
    hv.save(plot_.opts(height=700,responsive=True), "docs/assets/plot_demo.html")
    
    # plot #2: compare the surge signals obtained with the 3 sets of tidal constituents
    plot2_ = plot_df(ts_hourly, "Total Water Level signal", "k") \
        * plot_df(surges["SHORT"], "Detided Residual Signal - SHORT set of tidal constituents", "orange") \
        * plot_df(surges["FULL"], "Detided Residual Signal - FULL set of tidal constituents", "r") \
        * plot_df(surges["NOAA"], "Detided Residual Signal - NOAA set of tidal constituents", "g")
    hv.save(plot2_.opts(height=700, responsive=True, title="Differences induced by different Harmonic subsets"), "docs/assets/plot_compare.html")

    # plot #3: compare the amplitudes of the tidal constituents
    coef = pytides_get_coefs_df(ts_hourly, FULL)
    hv.save(plot_comparative_amplitudes(coef, "amplitude"), "docs/assets/tidal_decomposition.html")

