import holoviews as hv
import pandas as pd

from detide.constants import SHORT, FULL, NOAA, EXTENDED

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


def test_detide_yearlong_constituent_comparison():
    # hourly water level data for the whole of 2019 at two stations (one per column)
    df = pd.read_csv("tests/data/yearlong_ts_hourly_2019.csv", encoding="utf-8-sig")
    df.index = pd.date_range("2019-01-01 00:00", periods=len(df), freq="h", tz="UTC")

    for station in df.columns:
        ts_hourly = df[station].dropna() # must be a pd.Series; drop missing hours

        # compute the coefficients and surge signal for the 3 sets of tidal constituents
        coefs = {}
        surges = {}
        for astro, name in zip([FULL, NOAA, EXTENDED], ["FULL", "NOAA", "EXTENDED"]):
            coef = pytides_get_coefs(ts_hourly, astro)
            coefs[name] = pytides_get_coefs_df(ts_hourly, astro)
            surges[name] = pytides_surge(ts_hourly, coef)

        # the EXTENDED set should resolve at least as many constituents as the others
        assert len(coefs["EXTENDED"]) >= len(coefs["NOAA"]) >= len(coefs["FULL"])

        station_id = station.strip().split(",")[0].lower().replace(" ", "_")

        # plot: compare the surge signals obtained with the 3 sets of tidal constituents
        plot_ = plot_df(ts_hourly, "Total Water Level signal", "k") \
            * plot_df(surges["FULL"], "Detided Residual Signal - FULL set of tidal constituents", "r") \
            * plot_df(surges["NOAA"], "Detided Residual Signal - NOAA set of tidal constituents", "g") \
            * plot_df(surges["EXTENDED"], "Detided Residual Signal - EXTENDED set of tidal constituents", "b")
        hv.save(plot_.opts(height=700, responsive=True,
                title=f"Differences induced by different Harmonic subsets - {station.strip()}"),
                f"docs/assets/plot_compare_{station_id}.html")

        # plot: compare the amplitudes of the EXTENDED tidal constituents
        hv.save(plot_comparative_amplitudes(coefs["EXTENDED"], "amplitude"),
                f"docs/assets/tidal_decomposition_{station_id}.html")
