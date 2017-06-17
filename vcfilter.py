# vcFilter
# (c) 2017 Ali Rassolie

# from bokeh.io import output_notebook; output_notebook()
from collections import Counter, OrderedDict
from bokeh.charts import HeatMap, show, output_file
from bokeh.io import curdoc

import pandas as pd
import numpy as np
import re

class VcFilter():
	"""Note that index 5 is qual, index 0 is chrom, filter is 6""" 

	def __init__(self, infile, outfile, **kwargs):
		self.infile = infile
		self.outfile = outfile
		self.kwargs = kwargs
		self.index = {"FILTER": 6, "QUAL": 5}
		

	def row_generator(self):
		with open(self.infile, "r") as file:
			try:
				for row in file: 
					if "#" not in row: 
						yield row, row.split()
			
			except StopIteration as e:
				print(e)

	def row_processer(self):
		gen = self.row_generator()
		with open(self.outfile, "w") as file:
			file.write("")

		with open(self.outfile, "a") as file:
			for row, rowlist in gen:

				if self.check_row(rowlist):
					file.write("{}".format(row))


	def check_row(self, rowlist):
		for key in iter(self.kwargs):
			if float(rowlist[self.index["QUAL"]]) > self.kwargs["QUAL"]:
				try:
					if self.kwargs[key] in rowlist[self.index[key]]:
						count = Counter(rowlist[-1])
						if count["1"] >= 2: pass
						elif count["2"] >= 2: pass
						elif count["1"] and count["2"] >= 1: pass
						else:return False
					
					else:return False

				except TypeError as e:
					pass
			else:
				return False
		return True


	def heat_mapping(self, title= "heatmap", outfile="blah_output.html", rows=50):
		data = self.process_heat(rows=rows)

		hm = HeatMap(data, title="Heatmap", x="x", y="y", values="count", stat=None)
		output_file(outfile)
		curdoc().add_root(hm)
		show(hm)		

	def process_heat(self,  rows=50, start=0, stop=50):
		gen = self.row_generator()
		x = ['Fibroblast1', 'Fibroblast22', 'Fibroblast24', 'Fibroblast27', 'Fibroblast2', 'Fibroblast30', 'Fibroblast33', 'Fibroblast34', 'Fibroblast36', 'Fibroblast38', 'Fibroblast39', 'Fibroblast40', 'Fibroblast41', 'Fibroblast42', 'Fibroblast43', 'Fibroblast4', 'Fibroblast5', 'Fibroblast6']
		y = []
		x_count = []

		try: 
			for i in range(rows):
				_, rowlist = next(gen)
				del _
				y_append = ["chrom {} pos {}".format(rowlist[0], rowlist[1])] * 18
				
				for i in y_append:
					y.append(i)

				x_data = re.findall("\w", rowlist[-1])
				print(rowlist[-1])
				for each in x_data:
					try:
						x_count.append(int(each))
					except ValueError as e:
						each = -1
						x_count.append(int(each))

		except StopIteration as e: 
			print(len(y), len(x_count), len(x))

		data = { "x":x*rows, "y": y, "count": x_count }
		print(data["count"])
		return data

run_instance = VcFilter(infile="monovar_subset.txt", outfile="monovar_subset_out", FILTER="PASS", QUAL=10)
run_instance.heat_mapping(rows = 40)