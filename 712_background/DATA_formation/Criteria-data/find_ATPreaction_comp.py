## !/usr/bin/python
## function: save main C#, C# of each reaction that uses ATP 
## output: '<root_dir>/ATPreaction_compoundPair.txt’ (Format: R#####, C#####, C#####)

## import modules
import itertools
import networkx as nx
import json
import urllib2, sys, re
from collections import defaultdict
from optparse import OptionParser
from time import strftime
import sys, getopt, os, glob, random
import shlex, subprocess, re

def main(argv):
	optparse_usage = 'find_ATPreaction_comp.py -i <ATPreaction_id> -r <root_dir>'
	parser = OptionParser(usage=optparse_usage)
	parser.add_option("-i", "--inputATPreaction", action="store", type="string",
                dest="input_ATP", help='The input text file of reaction id list, which are related to ATP')
	parser.add_option("-r", "--rootDir", action="store", type="string",
                dest="root_dir", help='The root directory. All files are generated here.')

	(options, args) = parser.parse_args()
	if options.input_ATP:
                input_ATP = os.path.abspath(options.input_ATP)
        else:
                print 'ERROR: please provide proper input file name'
	if options.root_dir:
                root_dir = os.path.abspath(options.root_dir)
        else:
                print 'ERROR: please provide proper root direcotory'
	#Run Functions
	print 'START time:\t%s' % (strftime("%Y-%m-%d %H:%M:%S"))
	make_file(input_ATP, root_dir)
	print 'END time:\t%s' % (strftime("%Y-%m-%d %H:%M:%S"))
 
## define the function#1 to download the information

def download_file(path):
	data = urllib2.urlopen(path, timeout = 200).read()
	data_split = data.split('\n')

	return data_split

## define the function#2 to read the file path

def read_file(path):
        with open(path) as f_in:
                txt = (line.rstrip() for line in f_in)
                txt = list(line for line in txt if line)
 
        return txt



### read file and parse the information
### format: (Reaction# , com_from, com_to) 
def make_file(input_ATP,root_dir):
	ATP_rn_name = read_file(input_ATP)
	output_file = "%s/ATPreaction_compoundPair.txt" %(root_dir)
	output = open(output_file, 'w')
	i = 0
	while i < len(ATP_rn_name):
        	rn_info = 'http://rest.kegg.jp/get/%s' % (ATP_rn_name[i])
        	rn_INFO = download_file(rn_info)
		for line in rn_INFO:
                	if re.findall('EQUATION' , line):
				if line.find('C00002') < line.find('<=>') and line.find('<=>') < line.find('C00008'):	
        				for line in rn_INFO:
                				if re.search(r'\smain',line):
                        				m = re.search(r'\s(C\d+_C\d+)\s',line)
                        				if not m:
                                				print line
                                				sys.exit()
                        				compound = re.search(r'\s(C\d+_C\d+)\s',line).group(1)
                        				compound_split = compound.split('_')
                        				output.write('%s,%s,%s\n' % (ATP_rn_name[i], compound_split[0], compound_split[1]))
				elif line.find('C00008') < line.find('<=>') and line.find('<=>') < line.find('C00002'):
					for line in rn_INFO:
                                        	if re.search(r'\smain',line):
                                                	m = re.search(r'\s(C\d+_C\d+)\s',line)
                                                	if not m:
                                                        	print line
                                                        	sys.exit()
                                                	compound = re.search(r'\s(C\d+_C\d+)\s',line).group(1)
                                                	compound_split = compound.split('_')
                                                	output.write('%s,%s,%s\n' % (ATP_rn_name[i], compound_split[0], compound_split[1]))
        	i += 1
	output.close()	


if __name__ == "__main__":
        main(sys.argv[1:])
