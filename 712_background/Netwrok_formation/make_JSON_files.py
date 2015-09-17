## !/usr/bin/python
## function: produce the selected paths of compound pair into JSON files.
## output: json files that will be created in <root_dir>  (C#####_C#####.json)

# import modules
from time import strftime
from optparse import OptionParser
import sys, getopt, os, glob, random
import shlex, subprocess, re
import itertools
import networkx as nx
from collections import defaultdict
import json

def main(argv):
	optparse_usage = 'make_JSON_files -i <input_paths> -k <KEGG_reaction_list> -c <compound_name> -r <root_dir>'
	parser = OptionParser(usage=optparse_usage)
	parser.add_option("-i", "--inputPaths", action="store", type="string",
		dest="input_path", help='The input text file of paths, which are changed into JSON format.')
	parser.add_option("-k", "--keggReaction", action="store", type="string",
		dest="kegg_reaction", help='The input text file including KEGG reaction IDs, compound ID pairs, and E. coli K-12 gene information')
	parser.add_option("-c", "--compoundName", action="store", type="string",
                dest="compound_name", help='The input text file of KEGG compound IDs, which are changed into chemical names')
	parser.add_option("-r", "--rootDir", action="store", type="string",
                dest="root_dir", help='The root directory. All files are generated here.')

	output_number = []
	(options, args) = parser.parse_args()
	if options.root_dir:
		root_dir = os.path.abspath(options.root_dir)
	else:
		print 'ERROR: please provide proper root direcotory'
	if options.input_path:
		input_path = os.path.abspath(options.input_path)
	else:
		print 'ERROR: please provide proper input file name'
	if options.kegg_reaction:
		kegg_reaction = os.path.abspath(options.kegg_reaction)
	else:
		print 'ERROR: please provide the proper name of kegg reaction text file'
	if options.compound_name:
                compound_name = os.path.abspath(options.compound_name)
        else:
                print 'ERROR: please provide the proper name of text file including kegg compound IDs and chemical name'

	#Run Fuctions
	print 'START time:\t%s' % (strftime("%Y-%m-%d %H:%M:%S"))
	make_file(input_path, kegg_reaction, compound_name, root_dir)
	print 'END time:\t%s' % (strftime("%Y-%m-%d %H:%M:%S"))
### Define functions
def read_file(input_file):
        with open(input_file) as f_in:
                txt = (line.rstrip() for line in f_in)
                txt = list(line for line in txt if line)
        return txt

#Parse reactions IDs using pairs of compounds
def parse_reaction_name(pathway_link):
	with open(pathway_link) as f_in:
	  txt = (line.rstrip() for line in f_in)
	  txt = list(line for line in txt if line)	

	dic = defaultdict(str)
	dic2 = defaultdict(str)
	for line in txt:
        	line_split = line.split(',')
	        edge_from = line_split[1]
        	edge_to = line_split[2]
	        reaction = line_split[0]
		ecoli_info =  line_split[3]
	        compound_pair = (edge_from, edge_to)
        	dic[compound_pair] = (reaction)
		dic2[reaction] = (ecoli_info)
	return dic, dic2

def parse_compound(pathway_link):
	with open(pathway_link) as f_in:
          txt = (line.rstrip() for line in f_in)
          txt = list(line for line in txt if line)      
 
        dic = defaultdict(str)
	for line in txt:
		line_split = line.split('\t')
		compound = line_split[0].strip()
		Chem_name = line_split[1].strip()
		dic[compound] = Chem_name
	return dic

#parse the first degree compounds list
def parse_1st_degree_comp(pathway_link):
        Dict_degree_comp = defaultdict(str)
        first_degree_compounds = read_file(pathway_link)
        for line in first_degree_compounds:
                line_split = line.split('\t')
                compound = line_split[0]
                connected_compound_list = line_split[1::]
                Dict_degree_comp[compound] = connected_compound_list
        return Dict_degree_comp

#Change the format into JSON
def format_into_json(paths, pair, dic, dic2, dic3):
	all_compounds = []
	for i in paths:
		all_compounds.extend(i.split(', '))
		
	all_compounds_unique = list(set(all_compounds))
	
	D_compound = {} # Key: compound (C0000X, etc) Value: dict - key: path1, path2, path3, value: 0 or 1
	j = 0
	while j < len(paths):
		for compound in paths[j].split(', '):
			a = len(paths)/4
			if j < a:
                        	path_name = 'ATP_%s' % (j+1)
			elif  j < 2*a:
				path_name = 'CO2_%s' % (j+1-a)
			elif  j < 3*a:
                                path_name = 'NADH_%s' % (j+1-a-a)
			elif  j < 4*a:
                                path_name = 'NADPH_%s' % (j+1-a-a-a)
                        if not D_compound.has_key(compound):
                                 D_compound[compound] = defaultdict(int)
                        D_compound[compound][path_name] = 1
		j += 1
  	
	D_comp_num = {}
        i = 0
        for compound in D_compound.keys():
                 D_comp_num[compound] = i
                 i += 1

	D_json = defaultdict(list)
	for compound, tmp_dic in D_compound.items():
                 D_small = {}
                 D_small['name'] = compound
		 D_small['chemical_name'] = dic3[compound]
		 n = 0
		 while n < len(paths):
			a = len(paths)/4
                        if n < a:
                                path_name = 'ATP_%s' % (n+1)
                        elif  n < 2*a:
                                path_name = 'CO2_%s' % (n+1-a)
                        elif  n < 3*a:
                                path_name = 'NADH_%s' % (n+1-a-a)
                        elif  n < 4*a:
                                path_name = 'NADPH_%s' % (n+1-a-a-a)
                 	D_small['%s' %(path_name)] = D_compound[compound]['%s' %(path_name)]
                 	n += 1
                 D_json['nodes'].append(D_small)

	done_reaction = []
	y = 0
	while y < len(paths):
                 i = 0
                 while i < len(paths[y].split(', ')) - 1:
                         reaction = paths[y].split(', ')[i:i+2]
                         from_comp, to_comp = reaction
                         if dic[(from_comp, to_comp)]:
                                 reaction_id = dic[(from_comp, to_comp)]
				 ecoli_Info = dic2[(reaction_id)]
                         else:
                                 reaction_id = dic[(to_comp, from_comp)]
				 ecoli_Info = dic2[(reaction_id)]
                         from_num = D_comp_num[from_comp]
                         to_num = D_comp_num[to_comp]
			 

                         if (from_num, to_num) in done_reaction:
                                 i += 1
                                 continue

                         done_reaction.append((from_num, to_num))

                         D_small = {}
                         D_small['source'] = from_num
                         D_small['target'] = to_num
                         D_small['reaction'] = reaction_id
			 D_small['ecoli'] = ecoli_Info

        		 D_link = defaultdict(int)
        		 for j in range(1,len(paths)+1):
            		 	if from_comp in paths[j-1].split(', ') and to_comp in paths[j-1].split(', '):
                			Path = paths[j-1].split(', ') 
					idx_from_comp = Path.index(from_comp)
                			idx_to_comp = Path.index(to_comp)
                			difference = abs(idx_from_comp - idx_to_comp)
                	 		if difference == 1:
						a = len(paths)/4
                        			if j <= a:
                                			path_name = 'ATP_%s' % (j)
                        			elif  j <= 2*a:
                                			path_name = 'CO2_%s' % (j-a)
                        			elif  j <= 3*a:
                                			path_name = 'NADH_%s' % (j-a-a)
                        			elif  j <= 4*a:
                                			path_name = 'NADPH_%s' % (j-a-a-a)
                    	 			D_link['%s' % (path_name)] = 1

			 m = 1
			 while m < 1+len(paths):
				a = len(paths)/4
                        	if m <= a:
                                	path_name = 'ATP_%s' % (m)
                        	elif  m <= 2*a:
                                	path_name = 'CO2_%s' % (m-a)
                        	elif  m <= 3*a:
                                	path_name = 'NADH_%s' % (m-a-a)
                        	elif  m <= 4*a:
                                	path_name = 'NADPH_%s' % (m-a-a-a)
        	 	 	D_small['%s' %(path_name)] = D_link['%s' %(path_name)]
        	 	 	m += 1
                         D_json['links'].append(D_small)
                         i += 1
		 y += 1
	return D_json	


#Write the JSON file

def make_file(pathway_link, kegg_reaction, compound_name, root_dir):
	with open(pathway_link) as f_in:
          txt = (line.rstrip() for line in f_in)
          txt = list(line for line in txt if line)

	i = 0
	z = 1
	while i < len(txt)-1:
                pair, kind1, paths1 = txt[i].split('\t')
                pair, kind2, paths2 = txt[i+1].split('\t')
                pair, kind3, paths3 = txt[i+2].split('\t')
                pair, kind4, paths4 = txt[i+3].split('\t')
                
                Paths1 = paths1.split('@')
                Paths2 = paths2.split('@')
                Paths3 = paths3.split('@')
                Paths4 = paths4.split('@')
		 
                Paths1.extend(Paths2)
                Paths1.extend(Paths3)
                Paths1.extend(Paths4)
		
        	Dict_reaction, Dict_ecoli = parse_reaction_name(kegg_reaction)
        	Dict_chem_name = parse_compound(compound_name)
        	Dict_json = format_into_json(Paths1, pair, Dict_reaction, Dict_ecoli,Dict_chem_name)
		f = '%s/%s.json' % (root_dir, pair)
		output = open(f, 'w')
        	output.write(json.dumps(Dict_json).replace('}, ', '},\n'))
		output.close()
		i += 4	

if __name__ == "__main__":
	main(sys.argv[1:])
