import pandas as pd

obj = pd.read_csv('example_file.csv')
def split_data(dataframe, dataframe_pivot):
	unique_vals= dataframe_pivot.unique().tolist()
	dicty = dict.fromkeys(unique_vals)
	for key in unique_vals:
		dicty[key]=dataframe[obj.Period==key]
	return dicty,unique_vals
dicti = split_data(obj, obj.Period)
print(dicti['Roman'])
