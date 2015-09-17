#!/usr/bin/python

'''
Download enzyme database
Column - E.C. number, Gene list
'''


### Import modules
from httplib import *
import re, sys, os, glob
from optparse import OptionParser
from itertools import combinations

def main(argv):
	optparse_usage = 'download_KEGGenzyme.py -r <root_dir>'
	parser = OptionParser(usage=optparse_usage)
	parser.add_option("-r", "--rootDir", action="store", type="string",
		dest="root_dir", help='The root directory.You have to write it with new directory. All files are generated here.')
	(options, args) = parser.parse_args()
	if options.root_dir:
		root_dir = os.path.abspath(options.root_dir)
	else:
		print 'ERROR: please provide proper root direcotory'
	# Run the function
	make_file(root_dir)


def make_file(root_dir):
	# Get EC list from KEGG using REST-style API
	conn = HTTPConnection("rest.kegg.jp")
	conn.request("GET", "/list/enzyme")
	r1 = conn.getresponse()
	enzyme_list = r1.read().strip().split("\n")
	enzyme_list2 = [x.split('\t')[0] for x in enzyme_list]

	#num = 1
	for enzyme_element in enzyme_list2:
		print enzyme_element
		conn.request("GET", "/get/%s" % (enzyme_element))
		r2 = conn.getresponse() 
		ec_info = r2.read().strip().split("\n")

		# Parse ec_info
		genes_flag = False
		gene_list_enzyme = []
		for line in ec_info:
			if line.startswith('GENES       '):
				genes_flag = True
			elif re.search('^\S+', line):
				gene_flag = False
			
			if genes_flag:
				genome_code = line[12:15]
				genes_txt = line[17:]
				gene_list = genes_txt.split(' ')[0]
				gene_list_enzyme.append((genome_code, gene_list))
		
		# Download and write to file
		output_faa_file = os.path.join(root_dir, '%s.faa' % (enzyme_element))
		output_handle = open(output_faa_file, 'w')
		tmp_list = []
		for genome_code, gene_list in gene_list_enzyme:
			element2 = gene_list.split('(')[0]
			tmp_list.append('%s:%s' % (genome_code.lower(), element2))
			if len(tmp_list) == 5:
				conn.request("GET", "/get/%s/ntseq" % ('+'.join(tmp_list)))
				r3 = conn.getresponse()
				pro_fasta = r3.read().strip()
				output_handle.write(pro_fasta)
				output_handle.write('\n')
				tmp_list = [] # Initialization
			elif gene_list == gene_list_enzyme[len(gene_list_enzyme)-1]:
				conn.request("GET", "/get/%s/ntseq" % ('+'.join(tmp_list)))
				r3 = conn.getresponse()
				pro_fasta = r3.read().strip()
				output_handle.write(pro_fasta)
				output_handle.write('\n')
				tmp_list = [] # Initialization
		output_handle.close()
	### Some numbers
	print 'Number of E.C: %i' % (len(enzyme_list2))


