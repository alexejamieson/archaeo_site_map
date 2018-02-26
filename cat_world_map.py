import plotly.plotly as py
from plotly.graph_objs import *
import pandas as pd
import argparse
import numpy as np
import os

def parse_args():
    """Parse the command line arguments"""
    parser = argparse.ArgumentParser(description='Make a map')
    parser.add_argument('csv_file', type=str,help='csv file containing data')
    parser.add_argument('title', type=str,help='write the title for the map')
    args = parser.parse_args()
    return args.csv_file, args.title

def main():
    input_filename, title = parse_args()
    data = pd.read_csv(input_filename)
    mapbox_access_token = get_map_box_token()
    if mapbox_access_token:
       make_map(mapbox_access_token, data, title)

def get_map_box_token():
    """Check to see whether a text file containing the require mapbox access
       token is present. If it is not, then complain about it."""
    mapbox_access_token = None
    if(os.path.isfile('mapbox_accesstoken.txt')):
        fobj = open('mapbox_accesstoken.txt')
        mapbox_access_token = fobj.read()
    else:
        print("There is not mapbox access token file. To continue "
              "please create a file call 'mapbox_accesstoken.txt' "
               "can place your mapbox access token into it.")
    return mapbox_access_token

def hovertextformat(site,period):
    site_str = ['<b>Site:</b> {}'.format(name) for name in site]
    period_str = ['<b>Period:</b> {}'.format(name) for name in period]
    return [[item[0] + "<br>" + item[1]] for item in zip(site_str, period_str)]

def split_data(dataframe, dataframe_pivot):
    unique_vals= dataframe_pivot.unique().tolist()
    dicty = dict.fromkeys(unique_vals)
    for key in unique_vals:
        dicty[key]=dataframe[dataframe.Period==key]
    return dicty,unique_vals

def map_data(lat, lon, text, tracename):
    data = Scattermapbox(
                        lat=lat,
                        lon=lon,
                        mode='scattermapbox+markers',
                        hoverinfo='text',
                        marker=Marker(
                                size=9
                        ),
                        text=text,
                        name=tracename
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

def make_map(token, data, title):
    data_dict, unique_vals = split_data(data, data.Period)
    map_data_list = [] 
    for key in unique_vals:
         map_data_list.append(map_data(data_dict[key].Lat.tolist(),
                               data_dict[key].Long.tolist(),
                               hovertextformat(data_dict[key].Site.tolist(), data_dict[key].Period.tolist()),
                               str(key)))

    plot_data = Data(map_data_list)
    layout =map_layout(token, title, np.median(data.Lat.tolist()), np.median(data.Long.tolist()))

    fig = dict(data=plot_data, layout=layout)
    py.plot(fig)


if __name__ == '__main__':
    main()


