#!/usr/bin/python

from time import strftime
from optparse import OptionParser
import sys, getopt, os, glob, random
import shlex, subprocess, re
import itertools
from itertools import combinations
import networkx as nx
from collections import defaultdict
import json

def main(argv):
	optparse_usage = 'search_paths.py -i <reaction_id_file> -c <networkX_cutoff> -r <root_dir>'
	parser = OptionParser(usage=optparse_usage)
	parser.add_option("-i", "--inputFile", action="store", type="string",
		dest="input_file", help='The text file of KEGG Reaction IDs and Compound IDs of main pairs.')
	parser.add_option("-c", "--cutoff", action="store", type="int",
	#parser.add_option("-c", "--cutoff", action="store", type="string",
		dest="cutoff", help='The value for networkX cutoff. The default value is 7.')
	parser.add_option("-r", "--rootDir", action="store", type="string",
		dest="root_dir", help='The root directory. All files are generated here.')

	(options, args) = parser.parse_args()
	if options.root_dir:
		root_dir = os.path.abspath(options.root_dir)
	else:
		print 'ERROR: please provide proper root direcotory'
	if options.input_file:
		input_file = os.path.abspath(options.input_file)
	else:
		print 'Error: please provide proper input file'
	if options.cutoff:
		networkx_cutoff = options.cutoff
	else:
		networkx_cutoff = 7 

	#Run Fuctions
	print 'cutoff:\t%s' % (networkx_cutoff)
	print 'START time:\t%s' % (strftime("%Y-%m-%d %H:%M:%S"))
	Dict_reactions, edge_list = parse_reaction_name(input_file)
	compound_pairs = find_all_possible_pairs(edge_list)
	result_paths = run_networkx(networkx_cutoff, compound_pairs, edge_list, root_dir)
	print 'END time:\t%s' % (strftime("%Y-%m-%d %H:%M:%S"))



#Parse reactions IDs using pairs of compounds
def parse_reaction_name(pathway_link):
	with open(pathway_link) as f_in:
	  txt = (line.rstrip() for line in f_in)
	  txt = list(line for line in txt if line)	

	edge_list = []
	dic = defaultdict(str)
	for line in txt:
        	line_split = line.split(',')
	        reaction = line_split[0]
	        edge_from = line_split[1]
        	edge_to = line_split[2]
        	edge_list.append((edge_from, edge_to))
	        compound_pair = (edge_from, edge_to)
        	dic[compound_pair] = (reaction)
	return dic, edge_list

###When it comes to find all possible pairs of compounds
def find_all_possible_pairs(edge_list):
        list_of_lists = [list(elem) for elem in edge_list]
        list_of_lists = list(itertools.chain(*list_of_lists))
        node_list = set(list_of_lists)
        print len(node_list)
        pairs = [",".join(map(str,comb)) for comb in combinations(node_list, 2)]
        return pairs

#Create a network by running networkX
def run_networkx(networkx_cutoff, compound_pairs, edge_list, root_dir):
	output_file = '%s/networkx_result_%s.txt' % (root_dir, networkx_cutoff)
	output = open(output_file, 'w')
	Dict_paths = defaultdict(list)
	for line in compound_pairs:
		compound = line.split(',')
		compound = sorted(compound)
		G=nx.Graph()
		G.add_edges_from(edge_list)
		paths = nx.all_simple_paths(G, source='C13482', target='C19621', cutoff=networkx_cutoff)
		#paths = nx.all_simple_paths(G, source=compound[0], target=compound[1], cutoff=networkx_cutoff)
		list_paths = list(paths)
		if list_paths == []:
			continue
		new_list_paths = []
		for path in list_paths:
			path = ', '.join(path)
			new_list_paths += [path]
		print '%s_%s\t%s\n' %(compound[0], compound[1], '@'.join(new_list_paths))
		sys.exit()
		output.write('%s\t%s\n' %('_'.join(compound), list_paths))
	output.close()


if __name__ == "__main__":
	main(sys.argv[1:])
