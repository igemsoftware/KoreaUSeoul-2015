import sys, re, os
from optparse import OptionParser

def main(argv):
        optparse_usage = 'compound_table.py -i <input_paths> -f <table_format> -r <root_dir>'
        parser = OptionParser(usage=optparse_usage)
        parser.add_option("-i", "--inputpaths", action="store", type="string",
                dest="input_path", help='The input file is the kegg_compound_part.tsv')
        parser.add_option("-r", "--rootDir", action="store", type="string",
                dest="root_dir", help='The root directory. All files are generated here.')
        parser.add_option("-f", "--tableFormat", action="store", type="string",
                dest="format_path", help='The different number that you have given before.')
	
	(options, args) = parser.parse_args()
	if options.input_path:
                input_path = os.path.abspath(options.input_path)
        else:
                print 'Error: please provide proper input file name'
	if options.format_path:
                format_path = os.path.abspath(options.format_path)
        else:
                print 'Error: please provide proper input file name'
	if options.root_dir:
                root_dir = os.path.abspath(options.root_dir)
        else:
                print 'ERROR: please provide proper root direcotory'
	# Run functions
	print "working"
	make_file(input_path, format_path, root_dir)


def read_file(input_file):
        with open(input_file) as f_in:
                txt = (line.rstrip() for line in f_in)
                txt = list(line for line in txt if line)
        return txt
	
def make_file(input_path, format_path, root_dir):
	database = read_file(input_path)
	for lines in database:
    		raw = re.split('\t', lines)
		print raw
    		name = raw[1].split(';///')
    		chemical_name = '%s%s%s' % ('<td><center>', name[0], '</center></td>')
    		if 3 >= len(raw):
        		formula = '<td><center>No data</center></td>'
    		else:
        		formula = '%s%s%s' % ('<td><center>', raw[2], '</center></td>')
    		if 4 >= len(raw) :
        		exact_mass = '<td><center>No data</center></td>'
    		else:
        		exact_mass = '%s%s%s' % ('<td><center>', raw[3], '</center></td>')
    		if 5 >= len(raw) :
        		mol_weight = '<td><center>No data</center></td>'
    		else:
        		mol_weight = '%s%s%s' % ('<td><center>', raw[4], '</center></td>')
    		table_format = read_file(format_path)
    		final = ''
    		n1 = '<td class="tg-x0js"> <image src="http://www.genome.jp/Fig/compound/'
    		n2 = '.gif" width="150" height="100" ></td>'
    		img = '%s%s%s' % (n1, raw[0], n2)
    		j = 1
    		for sets in table_format:
        		if j == 6:
            			final += '%s%s%s' % ('<caption>', raw[0], '</caption>')
            			j += 1
        		elif j == 9:
            			final += chemical_name
            			j += 1
        		elif j == 13:
            			final += formula
            			j += 1
        		elif j == 17:
            			final += exact_mass
            			j += 1
        		elif j == 21:
            			final += mol_weight
            			j += 1
        		elif j == 25:
            			final += img
            			j += 1
        		else:
            			final += sets
            			j += 1
    			ff = '%s/%s.html' % (root_dir, raw[0])
    			output = open(ff, 'w')
    			output.write('%s' % (final))
    			output.close()

if __name__ == "__main__":
        main(sys.argv[1:])
