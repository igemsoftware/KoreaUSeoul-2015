## !/usr/bin/python
## function:
## input:
## output:

### Import modules
import sys, re, os
from collections import defaultdict
from optparse import OptionParser
def main(argv):
        optparse_usage = 'remove_duplicated_edges.py -i <input_path> -k <kegg_reaction_list> -o <ouput_name> -r <root_dir>'
        parser = OptionParser(usage=optparse_usage)
        parser.add_option("-i", "--inputpath", action="store", type="string",
                dest="input_path", help='The input text file of top3 paths of all compound pairs')
	parser.add_option("-k", "--keggReaction", action="store", type="string",
		dest="kegg_reaction", help='The input text file including KEGG reaction IDs, compound ID pairs, and E. coli K-12 gene information')
        parser.add_option("-r", "--rootDir", action="store", type="string",
                dest="root_dir", help='The root directory. All files are generated here.')
        parser.add_option("-o", "--outputname", action="store", type="string",
                dest ="output_name",help='The output file name that you want')
 
        (options, args) = parser.parse_args()
        output_name= []
        if options.root_dir:
                root_dir = os.path.abspath(options.root_dir)
        else:
                print 'ERROR: please provide proper root direcotory'
	if options.kegg_reaction:
        	kegg_reaction = os.path.abspath(options.kegg_reaction)
	else:
        	print 'ERROR: please provide the proper name of kegg reaction text file'
 
        if options.input_path:
                input_path = os.path.abspath(options.input_path)
        else:
                print 'Error: please provide proper input file name'
        if options.output_name:
                output_name.append(options.output_name)
        else:
                print 'Error : please write output file name that you want'
        if len(args) > 0:
                output_name += args
	Dict_reactions = parse_reaction_name(kegg_reaction) 
        make_file(input_path, output_name,Dict_reactions)


### Define functions

def read_file(input_file):
	with open(input_file) as f_in:
		txt = (line.rstrip() for line in f_in)
		txt = list(line for line in txt if line)
	return txt

def parse_reaction_name(pathway_link):
        with open(pathway_link) as f_in:
          txt = (line.rstrip() for line in f_in)
          txt = list(line for line in txt if line)
 
        dic = defaultdict(str)
        for line in txt:
                line_split = line.split(',')
                edge_from = line_split[1]
                edge_to = line_split[2]
                reaction = line_split[0]
                compound_pair = (edge_from, edge_to)
                dic[compound_pair] = (reaction)
              
        return dic

def make_file(input_path, output_name, Dict_reactions):
	nx_txt = read_file(input_path)
	output = ''.join(output_name)
        output_file = '%s' %(output)
	output_handle = open(output_file, 'w')
	i = 1
	for line in nx_txt:
		if i % 50000 == 0: print '%i lines have been complete' % (i)
		line_split = line.split('\t')
		pair, paths = line_split

		paths_split = paths.split('@')
		tmp_list = []
		for element in paths_split:
			Reaction = []
			a= 0
			element_split = element.split(', ')
			while a <len(element_split)-1:
				reaction = element_split[a:a+2]
				from_comp, to_comp = reaction
				if Dict_reactions[(from_comp,to_comp)]:
					reaction_id = Dict_reactions[(from_comp, to_comp)]
                                	Reaction.append(reaction_id)
				else:
					reaction_id = Dict_reactions[(to_comp, from_comp)]
                                	Reaction.append(reaction_id)
				a += 1	
			

			if len(Reaction) != len(set(Reaction)): 
				continue
			
			tmp_list.append(', '.join(element_split))

		i += 1
		output_handle.write('%s\t%s\n' % (pair, '@'.join(tmp_list)))

	output_handle.close()

if __name__ == "__main__":
        main(sys.argv[1:])
