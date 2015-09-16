## !/usr/bin/python
## function:
## input:
## output:

## import modules
from time import strftime
import urllib2, re, sys, os
from optparse import OptionParser
import itertools

def main(argv):
        optparse_usage = 'kegg_equat_name_data.py -k <KEGG_reaction_list> -r <root_dir>'
	parser = OptionParser(usage=optparse_usage)
	parser.add_option("-k", "--keggReaction", action="store", type="string",
                dest="kegg_reaction", help='The input text file including KEGG reaction IDs, compound ID pairs, and E. coli K-12 gene information')
        parser.add_option("-r", "--rootDir", action="store", type="string",
                dest="root_dir", help='The root directory. All files are generated here.')
	(options, args) = parser.parse_args()
	if options.kegg_reaction:
                kegg_reaction = os.path.abspath(options.kegg_reaction)
        else:
                print 'ERROR: please provide the proper name of kegg reaction text file'
	if options.root_dir:
                root_dir = os.path.abspath(options.root_dir)
        else:
                print 'ERROR: please provide proper root direcotory'

	#Run Fuctions
        print 'START time:\t%s' % (strftime("%Y-%m-%d %H:%M:%S"))
        make_file(kegg_reaction)
        print 'END time:\t%s' % (strftime("%Y-%m-%d %H:%M:%S"))

### Define functions
def read_file(input_file):
        with open(input_file) as f_in:
                txt = (line.rstrip() for line in f_in)
                txt = list(line for line in txt if line)
        return txt

def make_file(ReactionID_compoundPair):
	kegg_reaction = read_file(ReactionID_compoundPair)
	
	output_file = 'equ_name_data.txt'
	output = open(output_file, 'w')

	i = 0
	while i < len(kegg_reaction):
		try:
			R_C1_C2 = kegg_reaction[i].split(',')
			url = 'http://rest.kegg.jp/get/%s' % (R_C1_C2[0])
			data = urllib2.urlopen(url, timeout = 400).read()
			data_split = data.split('\n')
        		for line in data_split:
                		if re.search('DEFINITION',line):
					strip1 = line.strip('DEFINITION')
                                	reac_prod = strip1.split('<=>')
					if data_split[int(data_split.index(line))+1].find(R_C1_C2[1]) < data_split[int(data_split.index(line))+1].find('<=>'):
                                		output.write('%s, %s, %s, %s, %s\n' % (R_C1_C2[0],R_C1_C2[1],R_C1_C2[2],reac_prod[0].strip(),reac_prod[1].strip()))
					else:
						output.write('%s, %s, %s, %s, %s\n' % (R_C1_C2[0],R_C1_C2[1],R_C1_C2[2],reac_prod[1].strip(),reac_prod[0].strip()))

		except urllib2.HTTPError, e:
			print e.code
			print e.msg
			print e.headers
			print e.fp.read()		
		i += 1	
	output.close()







if __name__ == "__main__":
        main(sys.argv[1:])
