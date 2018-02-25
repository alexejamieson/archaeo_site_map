import plotly.plotly as py
from plotly.graph_objs import *
import pandas as pd
import argparse
import numpy as np

mapbox_access_token ='MAPBOX_API_KEY'
plotly_username = 'USERNAME'
plotly_api_key = 'API_KEY'

py.set_credentials_file(username=plotly_username, api_key = plotly_api_key)


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
	
def make_map(token,latitude,longitude,site, period, title):


	data = Data([
		Scattermapbox(
			lat=latitude,
			lon=longitude,
			mode='scattermapbox+markers',
			hoverinfo='text',
			marker=Marker(
				size=9
			),
			text=hovertextformat(site,period)
		),
	])
	layout = Layout(
		autosize=True,
		title=title,
		hovermode='closest',
		mapbox=dict(
			accesstoken=token,
			bearing=0,
			center=dict(
				lat= np.median(latitude),
				lon=-np.median(longitude),
			), 
			pitch=0,
			zoom=3
		),
	)

	fig = dict(data=data, layout=layout)
	py.plot(fig)

	
if __name__ == '__main__':
	main()