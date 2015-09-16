## !/usr/bin/python
## function:
## input:
## output:

# import modules
from optparse import OptionParser
from time import strftime
import itertools
import urllib2, re, sys

def main(argv):
	optparse_usage = 'aad_reaction_info.py -i <KEGG_reaction_id> -r <root_dir>'
        parser = OptionParser(usage=optparse_usage)
        parser.add_option("-i", "--inputReaction", action="store", type="string",
                dest="input_reaction", help='The input text file of KEGG reaction id list.') 
        parser.add_option("-r", "--rootDir", action="store", type="string",
                dest="root_dir", help='The root directory. All files are generated here.')
 
        (options, args) = parser.parse_args()
        if options.input_reaction:
                input_reaction = os.path.abspath(options.input_reaction)
        else:
                print 'ERROR: please provide proper input file name'
        if options.root_dir:
                root_dir = os.path.abspath(options.root_dir)
        else:
                print 'ERROR: please provide proper root direcotory'
        #Run Functions
        print 'START time:\t%s' % (strftime("%Y-%m-%d %H:%M:%S"))
        make_file(input_reaction)
        print 'END time:\t%s' % (strftime("%Y-%m-%d %H:%M:%S"))

def make_file(input_file):
	with open(input_file) as f1_in:
        	txt = (line.rstrip() for line in f1_in)
        	txt =list(line for line in txt if line)

	#Read E. coli K-12 genes from keggrest
	url = 'http://rest.kegg.jp/link/reaction/eco'
	data = urllib2.urlopen(url, timeout = 200).read()
	data_split = data.split('\n')

	### parse the reacion IDs of ecoli
	eco_RN=''
	for line in data_split:
        	if re.findall('R\d+',line):
                	eco_rn=re.findall('R\d+',line)
                	eco_Rn = ''.join(eco_rn)
                	eco_RN += eco_Rn
                	eco_RN += ','
	eco = eco_RN.split(',')


	#Parse the main pairs from keggrest
	output_file = open("reaction_compoundPair_eco.txt",'w')
	i = 0
	while i < len(txt):
		reaction = txt[i]
		if eco.count(reaction) == 0:
			eco_gene = 0
		else:
			eco_gene = 1
		url = 'http://rest.kegg.jp/get/%s' % (reaction)
		data = urllib2.urlopen(url, timeout = 200).read()
		data_split = data.split('\n')
		for line in data_split:
			if re.search(r'\smain',line):
				m = re.search(r'\s(C\d+_C\d+)\s',line)
				if not m:
					sys.exit() #should ask smcho why she wrote this line.
				compound = re.search(r'\s(C\d+_C\d+)\s',line).group(1)
                		compound_pair = compound.split('_')
				output_file.write('%s,%s,%s,%s\n' % (txt[i], compound_pair[0], compound_pair[1], eco_gene)) 
		i += 1
	output_file.close()

if __name__ == "__main__":
        main(sys.argv[1:])
