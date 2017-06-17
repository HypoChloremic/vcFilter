# vcFilter
# (c) 2017 Ali Rassolie

# from bokeh.io import output_notebook; output_notebook()
try:
	
	from bokeh.charts import HeatMap, show, output_file
	from bokeh.io import curdoc
	import pandas as pd

except ModuleNotFoundError as e:
	print("problem")

from collections import Counter, OrderedDict, deque
import re, datetime, time
import numpy as np
from math import ceil




def isnumber(val):
	"""To assert whether val is an integer or not, returning
	True or False, to simplify eval"""
	try:
		assert int(val)
		return True
	except ValueError:
		return False

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [ atoi(c) for c in re.split('(\d+)', text) ]


class VcFilter():
	"""Note that index 5 is qual, index 0 is chrom, filter is 6""" 

	def __init__(self, infile, outfile, **kwargs):
		self.infile = infile
		self.outfile = outfile
		self.kwargs = kwargs
		self.index = {"FILTER": 6, "QUAL": 5}
		self.germgen = self.germ_gen()
		self.cell = ['Fibroblast1', 'Fibroblast22', 'Fibroblast24', 'Fibroblast27', 'Fibroblast2', 'Fibroblast30', 'Fibroblast33', 'Fibroblast34', 'Fibroblast36', 'Fibroblast38', 'Fibroblast39', 'Fibroblast40', 'Fibroblast41', 'Fibroblast42', 'Fibroblast43', 'Fibroblast4', 'Fibroblast5', 'Fibroblast6']
		

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
			# a = 0	
			# for row, rowlist in gen:
			# 	if self.check_row(rowlist):
			# 		file.write("{}".format(row))
			num = 0
			timestamp = datetime.datetime.today().timestamp()

			for row, rowlist in gen:
				num += 1
				if self.check_row(rowlist):
					file.write("{}".format(row))
					# print("Passed")
				if num > 100000:
					print(num/(ceil(datetime.datetime.today().timestamp()-timestamp) ) )
					timestamp = datetime.datetime.today().timestamp()
					num = 0


	def germ_gen(self, infile="FibBulk_conbase_locifile_q20_dp20.txt"):
		with open(infile, "r") as germfile:
			q = deque(maxlen=1) 
			q.append([int(i) for i in next(germfile).split("\t") if isnumber(i)])
			print(q)
			yield

			try: 
				while True:
					if self.grow <= q[0]:

						if  self.grow[0] == q[0][0] and self.grow[1] == q[0][1]:
							q.append([int(i) for i in next(germfile).split("\t") if isnumber(i)])
							yield False
						
						else:
							yield True
					
					elif self.grow > q[0]:

						q.append([int(i) for i in next(germfile).split("\t") if isnumber(i)])

					else: raise ValueError
			except StopIteration as e:
				print(e)

		while True:
			print("while")
			yield True


	def check_row(self, rowlist):

		for key in iter(self.kwargs):
			self.grow = [int(rowlist[0]), int(rowlist[1])]

			if next(self.germgen):
				if float(rowlist[self.index["QUAL"]]) > self.kwargs["QUAL"]:
					try:
						if self.kwargs[key] in rowlist[self.index[key]]:
							count = Counter(rowlist[-1])
							if count["1"] >= 2: pass
							elif count["2"] >= 2: pass
							elif count["1"] and count["2"] >= 1: pass
							else: return False
						
						else: return False

					except TypeError as e:
						pass
				else:
					return False
			else:
				return False

		return True



	def heat_mapping(self, title= "heatmap", outfile="blah_output.html", rows=50):
		data = self.process_heat(rows=rows)
		try:
			hm = HeatMap(data, title="Heatmap", x="x", y="y", values="count", stat=None)
		except AttributeError as e:
			return e

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
				cell = x
				"""y-axis definition"""
				y_append = ["chrom {} pos {}".format(rowlist[0], rowlist[1])] * 18
				
				for i in y_append:
					"""We want to create a one dimensional list, it seems"""
					y.append(i)

				x_data = re.findall("\w", rowlist[-1])
				print(f"{x_data}\n{cell}")
				x_data =  [x for (y,x) in sorted(zip(cell,x_data), key=lambda pair: natural_keys(pair[0]))]
				print(f"{x_data}\n{sorted(cell, key=natural_keys)}")

				for each in x_data:
					try:
						x_count.append(int(each))
					except ValueError as e:
						each = -1
						x_count.append(int(each))

		except StopIteration as e: 
			print(len(y), len(x_count), len(x))

		x = sorted(x, key=natural_keys)
		data = { "x":x*rows, "y": y, "count": x_count }
		
		return data

	def row_count(self, infile):
		with open(infile, "r") as file:
			row = 0
			for eachrow in file:
				row += 1



run_instance = VcFilter(infile="monovar_subset_out2.vcf", outfile="filtered_monovar.vcf", FILTER="PASS", QUAL=10)
run_instance.row_processer()
# run_instance.heat_mapping(rows = 40)