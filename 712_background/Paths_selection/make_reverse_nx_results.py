## !/usr/bin/python
## function: produce the file without paths that make errors due to their overlapping R#####
## output: The output file name that you want (we recommend the input name to be added ‘_reversed’)

### Import modlules
import sys, re, os
from optparse import OptionParser

def main(argv):
	optparse_usage = 'make_reverse_nx_results.py -i <input_path> -o <output_name> -r <root_dir>'
        parser = OptionParser(usage=optparse_usage)
        parser.add_option("-i", "--inputpath", action="store", type="string",
                dest="input_path", help='The input text file of paths of all compound pairs')
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
	# Run the function
        make_file(input_path, output_name, root_dir)
 


### Define functions
def read_file(input_file):
	with open(input_file) as f_in:
		txt = (line.rstrip() for line in f_in)
		txt = list(line for line in txt if line)
	return txt

def make_file(input_path, output_name, root_dir):
	nt_result_txt = read_file(input_path)
	output = ''.join(output_name)
	output_file = '%s/%s' %(root_dir, output)
	output_handle = open(output_file, 'w')
	i = 1
	for line in nt_result_txt:
		if i % 50000 == 0:
			print '%i lines have been complete' % i
		line_split = line.split('\t')
		compound_pair, paths = line_split
		compound_pair_reverse = '_'.join(compound_pair.split('_')[::-1])
	
		paths_split = paths.split('@')
		
		paths_split2 = [', '.join(x.split(', ')[::-1]) for x in paths_split]
		output_handle.write('%s\t%s\n' % (compound_pair_reverse, '@'.join(paths_split2)))
		i += 1

	output_handle.close()

if __name__ == "__main__":
        main(sys.argv[1:])
