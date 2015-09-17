#!/usr/bin/python

'''
Download enzyme database
Column - E.C. number, Gene list
'''


### Import modules
from httplib import *
import re, sys, os, glob


### Parameters
output_dir = '/home/shkim/iGEM/GeneGene'

def read_file(input_file):
        with open(input_file) as f_in:
                #txt = (line.rstrip() for line in f_in)
		txt = (line for line in f_in)
                txt = list(line for line in txt if line)
        return txt

def write_txt(output_handle, en1):
	#tmp_list = []
	output_handle.write(en1)

        #tmp_list.append('%s' % (en1))

        #print '-- ', en1
        #output_handle.write(tmp_list)
        output_handle.write('\n')
	output_handle.write('##########\n')

	if en1 == '':	
		return

	idx = en1.find('-')
	if idx < 1:
		fname = 'ec:' + en1 + '.faa'
		fname = 'Enzyme3/' + fname
		print '... reading ', fname
		temp = read_file(fname)

		for line in temp[0:]:
			output_handle.write(line)

	return

reaction_txt = read_file('kegg_reaction_ec.tsv')

#D_compound = {}  #Key: kegg compound ID, Value: delta G0 prime

num = 1
for line in reaction_txt[0:]:
        line_split = line.split('\t')
        reaction_id = line_split[0]
	enzyme = line_split[1]
       
        # Download and write to file
        #output_faa_file = os.path.join(output_dir, '%s.faa' % (enzyme_element))
        output_faa_file = os.path.join(output_dir, '%s' % (reaction_id))
        output_handle = open(output_faa_file, 'w')

        #tmp_list = []

	idx = enzyme.find('///')
	while (idx > 0):
		en1 = enzyme[:idx]

		write_txt(output_handle, en1)
	

		enzyme = enzyme[idx+3:]
		idx = enzyme.find('///')

        en1 = enzyme.rstrip()
	if (en1 != ''):
		write_txt(output_handle, en1)

	output_handle.close()
