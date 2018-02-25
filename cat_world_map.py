import plotly.plotly as py
from plotly.graph_objs import *
import pandas as pd
import argparse

mapbox_access_token = 'pk.eyJ1IjoiYWxpamFtNDIiLCJhIjoiY2o0NGp0MW1hMWVkdTJwb3pqMnZ5MWE1aSJ9.pp_ayB2JvSsoIcTkykTqEA'
Test = 'nameoftest'

def parse_args():
	"""Parse the command line arguments"""
	parser = argparse.ArgumentParser(description='Make a map')
	parser.add_argument('csv_file', type=str,help='csv file containing data')
	args = parser.parse_args()
	return args.csv_file

def main():
	input_file2 = parse_args()
	Lat, Long, Site, Period = readcsv(input_file2)	
	make_map(mapbox_access_token, Lat, Long, Site, Test)

def readcsv(input_file):
	data = pd.read_csv(input_file)
	return data.Lat.tolist(), data.Long.tolist(), data.Site.tolist(), data.Period.tolist()


def make_map(token,latitude,longitude,hovertext,filename):


	data = Data([
		Scattermapbox(
			lat=latitude,
			lon=longitude,
			mode='markers',
			marker=Marker(
				size=9
			),
			text=hovertext,
		)
	])
	layout = Layout(
		autosize=True,
		hovermode='closest',
		mapbox=dict(
			accesstoken=token,
			bearing=0,
			center=dict(
				lat=38.92,
				lon=-77.07
			),
			pitch=0,
			zoom=10
		),
	)

	fig = dict(data=data, layout=layout)
	py.plot(fig, filename=filename)

	
if __name__ == '__main__':
	main()