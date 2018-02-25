import plotly.plotly as py
from plotly.graph_objs import *
import pandas as pd
import argparse
import numpy as np

#make a txt file with your access key for mapbox
fobj = open('mapbox_accesstoken.txt')
mapbox_access_token = fobj.read()

def parse_args():
    """Parse the command line arguments"""
    parser = argparse.ArgumentParser(description='Make a map')
    parser.add_argument('csv_file', type=str,help='csv file containing data')
    parser.add_argument('title', type=str,help='write the title for the map')
    args = parser.parse_args()
    return args.csv_file, args.title

def main():
    input_filename, title = parse_args()
    Lat, Long, Site, Period = readcsv(input_filename)
    make_map(mapbox_access_token, Lat, Long, Site, Period, title)

def readcsv(input_file):
    data = pd.read_csv(input_file)
    return data.Lat.tolist(), data.Long.tolist(), data.Site.tolist(), data.Period.tolist()

def hovertextformat(site,period):
    site_str = ['<b>Site:</b> {}'.format(name) for name in site]
    period_str = ['<b>Period:</b> {}'.format(name) for name in period]
    return [[item[0] + "<br>" + item[1]] for item in zip(site_str, period_str)]

def split_data(dataframe, dataframe_pivot):
    unique_vals= dataframe_pivot.unique().tolist()
    dicty = dict.fromkeys(unique_vals)
    for key in unique_vals:
        dicty[key]=dataframe[obj.Period==key]
    return dicty,unique_vals

def map_data(lat, lon, text):
    data = Scattermapbox(
                        lat=lat,
                        lon=lon,
                        mode='scattermapbox+markers',
                        hoverinfo='text',
                        marker=Marker(
                                size=9
                        ),
                        text=text
                )
    return data

def map_layout(token, title, lat_centre, lon_centre):
    lay = Layout(
                autosize=True,
                title=title,
                hovermode='closest',
                mapbox=dict(
                        accesstoken=token,
                        bearing=0,
                        center=dict(
                                lat= lat_centre,
                                lon=lon_centre
                        ),
                        pitch=0,
                        zoom=3
                ))
    return lay

def make_map(token,latitude,longitude,site, period, title):
    data = Data([map_data(latitude, longitude, hovertextformat(site,period))
    ])
    layout =map_layout(token, title, np.median(latitude), np.median(longitude))

    fig = dict(data=data, layout=layout)
    py.plot(fig)


if __name__ == '__main__':
    main()


