import pandas as pd
from pytides2.tide import constituent
from pytides2.tide import Tide

from scripts.constants import FULL
from scripts.constants import RESAMPLE


def align_ts(ts):
    # pytides2 has an off-by-one when len is odd: trim to even
    if len(ts) % 2 != 0:
        ts = ts.iloc[:-1]
    return ts


def resample(ts: pd.Series, resample: int = RESAMPLE) -> pd.Series:
    ts = ts.resample(f"{resample}min").mean()
    ts = ts.shift(freq=f"{resample / 2}min")  # Center the resampled points
    return ts.dropna()


def pytides_get_coefs(ts: pd.Series, constituents: list[constituent.BaseConstituent] = FULL,
) -> Tide:
    ts = align_ts(ts) # odd numbers don't work in pytides
    return Tide.decompose(ts.values, ts.index.to_pydatetime(), constituents=constituents)[0]


def pytides_get_coefs_df(ts: pd.Series, constituents: list[constituent.BaseConstituent] = FULL,
) -> pd.DataFrame:
    pytides_tide = pytides_get_coefs(ts, constituents)
    constituent_names = [c.name.upper() for c in pytides_tide.model["constituent"]]
    return pd.DataFrame(pytides_tide.model, index=constituent_names).drop(
        "constituent",
        axis=1,
    )


def pytides_surge(ts: pd.Series, tide: Tide) -> pd.Series:
    t0 = ts.index.to_pydatetime()[0]
    hours = (ts.index - ts.index[0]).total_seconds() / 3600
    times = Tide._times(t0, hours)
    return pd.Series(ts.values - tide.at(times), index=ts.index)

