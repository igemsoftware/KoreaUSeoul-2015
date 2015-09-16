## !/usr/bin/python
## function:
## input:
## output:

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
        optparse_usage = 'add_CO2reaction_info.py -i <CO2reaction_compoundPair> -r <root_dir>'
        parser = OptionParser(usage=optparse_usage)
        parser.add_option("-i", "--inputCO2reactionComp", action="store", type="string",
                dest="input_CO2", help='The input text file of reaction ids and compound pairs, which are related to CO2')
        parser.add_option("-r", "--rootDir", action="store", type="string",
                dest="root_dir", help='The root directory. All files are generated here.')
 
        (options, args) = parser.parse_args()
        if options.input_CO2:
                input_CO2 = os.path.abspath(options.input_CO2)
        else:
                print 'ERROR: please provide proper input file name'
        if options.root_dir:
                root_dir = os.path.abspath(options.root_dir)
        else:
                print 'ERROR: please provide proper root direcotory'
        #Run Functions
        print 'START time:\t%s' % (strftime("%Y-%m-%d %H:%M:%S"))
        make_file(input_CO2)
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


### read file and parse the information of CO2 change
### format:(Reaction# , com_from, com_to, CO2 change)
def make_file(input_CO2):
        CO2rn_comp1_comp2 = read_file(input_CO2)
        output_file = 'CO2reaction_compoundPair_change.txt'
        output = open(output_file, 'w')
	i = 1
	for target in CO2rn_comp1_comp2:
		print i
		i += 1
        	target_split = target.split(',')
        	rn_info = 'http://rest.kegg.jp/get/%s' % (target_split[0])
        	rn_INFO = download_file(rn_info)
		for line in rn_INFO:
                	if re.findall('EQUATION' , line):
                        	if re.findall(r'(\d+)\sC00011',line):
                                	num = re.findall(r'(\d+)\sC00011',line)
                               		Num = ''.join(num)
                                	if line.find('C00011') < line.find('<=>'):
                                        	if line.find(target_split[1]) < line.find('<=>'):
                                                	output.write('%s,-%s\n' % (target,int(Num)))
                                        	else:
                                                	output.write('%s,%s\n' % (target,int(Num)))
                                	else:
                                        	if line.find(target_split[1]) < line.find('<=>'):
                                                	output.write('%s,%s\n' % (target, int(Num)))
                                        	else:
                                                	output.write('%s,-%s\n' % (target,int(Num)))
                        	else:
                                	num = 1
                                	if line.find('C00011') < line.find('<=>'):
                                        	if line.find(target_split[1]) < line.find('<=>'):
                                                	output.write('%s,%s\n' % (target,-1))
                                        	else:
                                                	output.write('%s,%s\n' % (target,1))
                                	else:
                                        	if line.find(target_split[1]) < line.find('<=>'):
                                                	output.write('%s,%s\n' % (target, 1))
                                        	else:
                                                	output.write('%s,%s\n' % (target,-1))
	output.close()

if __name__ == "__main__":
        main(sys.argv[1:]) 
