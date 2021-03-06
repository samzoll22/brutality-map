import pandas
import numpy as np
import os

# TODO: switch from Basemap to cartopy
from mpl_toolkits.basemap import Basemap

# load data
df_cases = pandas.read_excel('GeorgeFloyd Protest - police brutality videos on Twitter.xlsx', skiprows=6)

#######
# clean up some of the cases.....

# sorry Alaska, Hawaii, Puerto Rico :(
excludes = ['ak', 'hi', 'pr', 'mp', 'vi', 'as', 'gu']

mask = np.where(df_cases['City']!='Nationwide')

df_cases = df_cases.iloc[mask]

end_idx = 473 # manual; temporary while spreadsheet is non-rectangular.
df_cases = df_cases.iloc[:end_idx]

# TODO: replace city abbreviations, irregularities to help with lookups.

df_cases['City'] = df_cases['City'].str.lower()
df_cases['State'] = df_cases['State'].str.lower()

# a bunch of not-inline-replacements
df_cases.replace('nyc', 'new york city', inplace=True)
df_cases.replace('los angeles (van nuyes)', 'los angeles', inplace=True)
df_cases.replace('long beach', 'los angeles', inplace=True)
df_cases.replace('hollywood', 'los angeles', inplace=True)
df_cases.replace('altanta', 'atlanta', inplace=True)
df_cases.replace('west philadelphia', 'philadelphia', inplace=True)
df_cases.replace('cincinnatti', 'cincinnati', inplace=True)
df_cases.replace('cincinatti','cincinnati',inplace=True)
df_cases['City'].replace(':as vegas', 'las vegas', inplace=True)
df_cases['City'].replace('fredricksburg', 'fredericksburg', inplace=True)

df_cases['State'].replace('cd', 'dc', inplace=True)
df_cases['State'].replace('k', 'ky', inplace=True)
df_cases['Doucette Text'].replace(np.nan, '[no description]', inplace=True)

# group by incident
def fetch_incident(ind):
    gdn = df_cases.loc[ind]['TGD Number']
    if not np.isnan(gdn):
        candidate = str(gdn).split('.')[0]
    else:
        # seems to work universally; but can catch any quirk cases as "other" for now.
        candidate = 'other'
    #
    return candidate
#

grouper = df_cases.groupby(fetch_incident)

# just remake manually, dataframe index being a pain.

#incidents = np.tile('', (df_cases.shape[0],))
#df_cases['incident'] = incidents
#for g,df_s in grouper:
#    df_cases.loc[df_s.index]['incident'] = g
##

incidents = [str(gdn).split('.')[0] if not np.isnan(gdn) else 'other' for gdn in df_cases['TGD Number'].values]
df_cases['incident'] = incidents

###################
#
# get latlon lookup table if it exists, and make a dictionary.
# (you need to run fetch_location.py manually if it does not exist.)
#
if os.path.exists('latlon_lookup.tsv'):
    import pandas
    df = pandas.read_csv('latlon_lookup.tsv', delimiter='\t')
    latlon_lookup = {', '.join((c,s)) : (x,y) for (c,s,x,y) in df.values}
else:
    latlon_lookup = {}

######################
#
# load basemap files for county/state level outlines.
#
from mpl_toolkits.basemap import Basemap
state_map = Basemap()
state_map.readshapefile('state_shp/cb_2018_us_state_20m', 'states', drawbounds=False)
# for now don't care about which state is which; just draw boundaries.
state_xs = []
state_ys = []

for si,info in zip(state_map.states,state_map.states_info):
    if info['STUSPS'].lower() in excludes:
        continue
    _xs = [sii[0] for sii in si]
    _ys = [sii[1] for sii in si]
    state_xs.append(_xs)
    state_ys.append(_ys)
#

county_map = Basemap()
county_map.readshapefile('county_shp/cb_2018_us_county_20m', 'counties', drawbounds=False)
# for now don't care about which state is which; just draw boundaries.
county_xs = []
county_ys = []

# for ci,info in zip(county_map.counties,county_map.counties_info):
#     if info['STUSPS'].lower() in excludes:
#         continue
#     _xs = [sii[0] for sii in si]
#     _ys = [sii[1] for sii in si]
#     county_xs.append(_xs)
#     county_ys.append(_ys)

# misc
citystates = df_cases[['City', 'State']].values
