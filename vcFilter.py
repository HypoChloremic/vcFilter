# vcFilter
# (c) 2017 Ali Rassolie

from collections import Counter
import re, datetime
from math import ceil
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
			num = 0
			timestamp = datetime.datetime.today().timestamp()

			for row, rowlist in gen:
				num += 1
				if self.check_row(rowlist):
					file.write("{}".format(row))
					# print("Passed")
				if num > 1000:
					print(num/(ceil(datetime.datetime.today().timestamp()-timestamp) ) )
					num = 0


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


if __name__ == '__main__':
	run_instance = VcFilter(infile="fibs_uppmax_output_0.9.vcf", outfile="monovar_subset_out2.vcf", FILTER="PASS", QUAL=10)
run_instance.row_processer()