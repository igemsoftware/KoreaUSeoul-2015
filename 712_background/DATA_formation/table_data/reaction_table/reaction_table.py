import sys, re, os
from optparse import OptionParser

def main(argv):
        optparse_usage = 'reaction_table.py -i <input_paths> -g <deltaG_path> -f <table_format> -r <root_dir>'
        parser = OptionParser(usage=optparse_usage)
        parser.add_option("-i", "--inputpaths", action="store", type="string",
                dest="input_path", help='The input file is the kegg_reaction.tsv')
	parser.add_option("-g", "--deltaGpaths", action="store", type="string",
                dest="deltaG_path", help='The input file is the Info_deltaG.csv')
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
	if options.deltaG_path:
                deltaG_path = os.path.abspath(options.deltaG_path)
        else:
                print 'Error: please provide proper input file name'
        if options.root_dir:
                root_dir = os.path.abspath(options.root_dir)
        else:
                print 'ERROR: please provide proper root direcotory'
	# Run the funtion
	make_file(input_path,deltaG_path, format_path, root_dir)

def read_file(input_file):
        with open(input_file) as f_in:
                txt = (line.rstrip() for line in f_in)
                txt = list(line for line in txt if line)
        return txt
def make_file(input_path,deltaG_path, format_path, root_dir):
	dictionary = read_file(deltaG_path)
	dic = {}
	red = '<span style="color:red;">'
	blue = '<span style="color:blue;">'
	tale = '</span>'
	button1 = '<td><center><a target="_blank" class="btn focus" href="../Gene_download/'
	button2 = '.html">'
	for line in dictionary:
    		line_split = line.split(',')
    		if len(line_split) == 4:
        		dic[line_split[0]] = '%s,%s' % ('No Data', 'No Data')
    		else:
        		dic[line_split[0]] = '%s,%s' % (line_split[3], line_split[4])
    
	database = read_file(input_path)
	for lines in database:
    		raw = re.split('\t', lines)
    		reaction_name = raw[0]
    		equation = raw[2]
    		C_equation = raw[3]
		table_format = read_file(format_path)
    		delta_g = ''
    		mark = ''
    		final = ''
    		if dic.get(raw[0]) != None:
        		inf = dic[raw[0]].split(',')
        		delta_g = inf[0]
        		mark = inf[1].rstrip()
    		else:
        		delta_g = 'No Data'
        		mark = 'No Data'
        

    		j = 1
    		for sets in table_format:
        		if j == 7:
            			final += '%s%s%s%s%s' % ('<caption><a target="_blank" style="color:blue;" href="http://www.kegg.jp/dbget-bin/www_bget?rn:', reaction_name, '">', reaction_name, '</a></caption>')
            			j += 1
        		elif j == 10:
            			final += '%s%s%s' % ('<td><center>', equation, '</center></td>')
            			j += 1
        		elif j == 14:
            			final += '%s%s%s' % ('<td><center>', C_equation, '</center></td>')
            			j += 1
        		elif j == 18:
            			if mark == '#':
                			final += '%s%s%s%s%s' % ('<td><center>', blue, delta_g, tale, '</td></center>')
            			if mark == '*':
                			final += '%s%s%s%s%s' % ('<td><center>', red, delta_g, tale, '</td></center>')
            			if mark == 'No Data':
                			final += '%s%s%s' % ('<td><center>', 'No Data', '</td></center>')
            			j += 1
        		elif j == 22:
            			final += '%s%s%s' % (button1, raw[0].rstrip(), button2)
            			j += 1
        		else:
            			final += sets
            			j += 1
    		ff = '%s/%s.html' % (root_dir,raw[0])
    		output = open(ff, 'w')
    		output.write('%s' % (final))
    		output.close()


if __name__ == "__main__":
        main(sys.argv[1:])
