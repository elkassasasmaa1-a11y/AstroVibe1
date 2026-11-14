# AstroVibe: pull real NASA POWER data for any field and print JSON to paste into the app.
# Google Colab: paste this whole cell, set LAT / LON, run, then copy the JSON line it prints.
# Source: NASA POWER (https://power.larc.nasa.gov), community AG, parameters T2M, T2M_MAX, PRECTOTCORR.

import json
import calendar
import requests
import numpy as np

LAT = 31.0   # latitude of the field  (example: Nile Delta)
LON = 30.5   # longitude of the field
CLIM_START, CLIM_END = 2001, 2024   # years used for monthly normals and trends
HEAT_START, HEAT_END = 2015, 2024   # years used to count days above 35 C

BASE = "https://power.larc.nasa.gov/api/temporal"
MONTHS = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]


def get(url, params):
    r = requests.get(url, params=params, timeout=120)
    r.raise_for_status()
    return r.json()["properties"]["parameter"]


# 1) Monthly series 2001-2024: T2M (deg C) and PRECTOTCORR (mm/day)
monthly = get(f"{BASE}/monthly/point", {
    "parameters": "T2M,PRECTOTCORR", "community": "AG",
    "longitude": LON, "latitude": LAT,
    "start": CLIM_START, "end": CLIM_END, "format": "JSON",
})
years = list(range(CLIM_START, CLIM_END + 1))

T = np.full((len(years), 12), np.nan)
P = np.full((len(years), 12), np.nan)
for yi, y in enumerate(years):
    for m in range(12):
        key = f"{y}{m + 1:02d}"
        t = monthly["T2M"].get(key)
        p = monthly["PRECTOTCORR"].get(key)
        if t is not None and t > -900:
            T[yi, m] = t
        if p is not None and p > -900:
            P[yi, m] = p * calendar.monthrange(y, m + 1)[1]   # mm/day -> mm/month

T_norm = np.nanmean(T, axis=0)
P_norm = np.nanmean(P, axis=0)

# 2) Trends per decade (simple linear fit of annual values)
annT = np.nanmean(T, axis=1)
annP = np.nansum(P, axis=1)
tT = float(np.polyfit(years, annT, 1)[0] * 10)
tR = float(np.polyfit(years, annP, 1)[0] * 10 / max(annP.mean(), 1e-6) * 100)

# 3) Heat days: average number of days per year with T2M_MAX above 35 C
daily = get(f"{BASE}/daily/point", {
    "parameters": "T2M_MAX", "community": "AG",
    "longitude": LON, "latitude": LAT,
    "start": f"{HEAT_START}0101", "end": f"{HEAT_END}1231", "format": "JSON",
})["T2M_MAX"]
hot = sum(1 for v in daily.values() if v > 35)
heat = hot / (HEAT_END - HEAT_START + 1)

out = {
    "T": [round(float(x), 1) for x in T_norm],
    "P": [round(float(x), 1) for x in P_norm],
    "heat": round(heat),
    "tT": round(tT, 2),
    "tR": round(tR, 1),
}
print("Paste this into AstroVibe > Use your own NASA POWER data:\n")
print(json.dumps(out))
