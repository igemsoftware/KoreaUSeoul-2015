#import modules

import sys, re
dictionary = open('/home/dhkim/reaction_table/reactionMain3.csv')
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
    
database = open('/home/dhkim/kegg_reaction.tsv')
for lines in database:
    raw = re.split('\t', lines)
    reaction_name = raw[0]
    equation = raw[2]
    C_equation = raw[3]
    table_format = open('/home/dhkim/reaction_table/table_format.txt', 'r')
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
    ff = '%s.html' % (raw[0])
    output = open(ff, 'w')
    output.write('%s' % (final))
    output.close()
