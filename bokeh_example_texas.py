# via https://docs.bokeh.org/en/latest/docs/gallery/texas.html?highlight=texas

from bokeh.io import show
from bokeh.models import LogColorMapper
from bokeh.palettes import Viridis6 as palette
from bokeh.plotting import figure

import numpy as np

# my modification - if sample data not downloaded, do it.
try:
    from bokeh.sampledata.unemployment import data as unemployment
    from bokeh.sampledata.us_counties import data as counties
except:
    raise Exception('could not import data sets; run bokeh.sampledata.download() then re-run script.')
#

palette = tuple(reversed(palette))

# lower 48 plus dc for now
excludes = ['ak', 'hi', 'pr', 'mp', 'vi', 'as', 'gu']

counties = {
    code: county for code, county in counties.items() if county["state"] not in excludes
}

county_xs = [county["lons"] for county in counties.values()]
county_ys = [county["lats"] for county in counties.values()]

county_names = [county['name'] for county in counties.values()]
#county_rates = [unemployment[county_id] for county_id in counties]
county_rates = []
for county_id in counties:
    county_rates.append( unemployment.get(county_id, np.nan) )
color_mapper = LogColorMapper(palette=palette)

data=dict(
    x=county_xs,
    y=county_ys,
    name=county_names,
    rate=county_rates,
)

TOOLS = "pan,wheel_zoom,reset,hover,save"

p = figure(
    title="Texas Unemployment, 2009", tools=TOOLS,
    x_axis_location=None, y_axis_location=None,
    tooltips=[
        ("Name", "@name"), ("Unemployment rate", "@rate%"), ("(Long, Lat)", "($x, $y)")
    ],
    plot_width=1000,
    plot_height=600
    )
p.grid.grid_line_color = None
p.hover.point_policy = "follow_mouse"

p.patches('x', 'y', source=data,
          fill_color={'field': 'rate', 'transform': color_mapper},
          fill_alpha=0.7, line_color="white", line_width=0.5)

show(p)
