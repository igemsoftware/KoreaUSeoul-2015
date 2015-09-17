#!/usr/bin/python

from time import strftime
from optparse import OptionParser
import sys, getopt, os, glob, random
import shlex, subprocess, re
import itertools
from itertools import combinations
from collections import defaultdict

def main(argv):
	optparse_usage = 'process_blastn_output.py -i <reaction_id_file> -b <blast_output_file> -r <root_dir>'
	parser = OptionParser(usage=optparse_usage)
	parser.add_option("-i", "--inputFile", action="store", type="string",
		dest="input_file", help='The text file of KEGG Reaction IDs and Compound IDs of main pairs.')
	parser.add_option("-b", "--blastOutputFile", action="store", type="string",
		dest="blast_output", help='The blast output file.')
	parser.add_option("-r", "--rootDir", action="store", type="string",
		dest="root_dir", help='The root directory. All files are generated here.')

	(options, args) = parser.parse_args()
	if options.root_dir:
		root_dir = os.path.abspath(options.root_dir)
	else:
		print 'ERROR: please provide proper root direcotory'
	if options.blast_output:
		blast_output = os.path.abspath(options.blast_output)
	else:
		print 'Error: please provide proper input file'
	if options.input_file:
		input_file = os.path.abspath(options.input_file)
	else:
		print 'Error: please provide proper input file'

	#Run Fuctions
	start_time = strftime("%Y-%m-%d %H:%M:%S")
	dict_parts = filter_blast_output(blast_output, root_dir)
	add_biobrick_info(input_file, dict_parts, blast_output, root_dir)
	print 'START time:\t%s' % (start_time)
	print 'END time:\t%s' % (strftime("%Y-%m-%d %H:%M:%S"))
	

def filter_blast_output(blast_output, root_dir):
	with open(blast_output) as f_in:
          txt = (line.rstrip() for line in f_in)
          txt = list(line for line in txt if line)

	dict_parts = defaultdict(list)
	blast_output = blast_output.split('/')[-1]
	output_text_file = '%s/%s.filtered' %(root_dir, blast_output)
	output = open(output_text_file, 'w')
	for line in txt:
		line = line.split('\t')
		e_value = float(line[10])
		if e_value > 1e-5:
			continue
		line_output = '\t'.join(line)
		output.write('%s\n' %(line_output))
		dict_parts[line[1].rstrip()] += [line[0]]
	output.close()
	return dict_parts


def add_biobrick_info(reaction_id, dict_parts, blast_output, root_dir):
	with open(reaction_id) as f_in:
          txt = (line.rstrip() for line in f_in)
          reaction_list = list(line for line in txt if line)

	for reaction in reaction_list:
		reaction_link = '%s/%s' % (root_dir, reaction)
		output_html = '%s.html' % (reaction_link)
		output = open(output_html, 'w')
		with open(reaction_link) as f_in:
	          txt = (line.rstrip() for line in f_in)
	          txt = list(line for line in txt if line)
		output.write('##########You can search a gene ID using Ctrl+F, or Command+F if you are a Mac user. If the gene is orthologous to a specific BioBrick part, the "BioBrick" hyperlink at the end of the FASTA defline will be activated.')
		for line in txt:
			if line.startswith('>') == True:
				line_list = line.split('>')[-1]
				line_list = line_list.split(' ')
				gene_name = line_list[0]
				parts_id = dict_parts[gene_name]
				if parts_id != []:
					output.write('%s <a style="color:blue;" target="_blank" href="http://compbio.korea.ac.kr/712/BioBrick/%s.html">BioBrick</a>\n<br>' %(line, gene_name))
					output_gene_html = '%s/%s.html' %(root_dir, gene_name)
					output2 = open(output_gene_html, 'w')
					parts_list = []
					for part in parts_id:
						parts_list += [part]
					parts_list = list(set(parts_list))
					parts_list = sorted(parts_list)
					for item in parts_list:
						output2.write('<a style="color:blue;" href="http://parts.igem.org/Part:%s">%s</a>\n<br>' %(item, item))
					output2.close()
				else:
					output.write('%s\n<br>' %(line))
			else:
				output.write('%s\n<br>' %(line))
		output.close()
		print '%s\t%s' %(output_html, strftime("%Y-%m-%d %H:%M:%S"))



if __name__ == "__main__":
	main(sys.argv[1:])
