import json
import csv
from itertools import zip_longest
from itertools import accumulate

# function used to make the parser of the fixed width file
def parser(fieldwidths):
    
    # slices defines the position of the end of each field within the fixed width file (fwf)
    slices  = tuple(slices for slices in accumulate(fw for fw in fieldwidths))
    
    # fields determines the length of each field as tuples (position a, position b)
    fields = tuple(zip_longest((0,)+slices, slices))[:-1]
    
    # takes index from positions defined above and then adds to line
    parse = lambda line: tuple(line[i:j] for i, j in fields)
    return parse

#------------------------------------------
# Generating the fixed width file
#------------------------------------------

# to read specification document
f = open('spec.json')
data = json.load(f)
f.close()

# assigning data to variables
columns = data['ColumnNames'] 
widths = data['Offsets']

# creating dimensions for each of the widths
dimen = tuple(zip(columns,map(int,widths)))

# generating fixed field file by attaching the fields with the corresponding widths to an empty string
fwf = ''.join([(field_name).ljust(width) for field_name, width in dimen])

#------------------------------------------
# running parser on fixed width file
#------------------------------------------

# creating a tuple with each of the widths of the fixed width file
fieldwidths = tuple(map(int,widths))
parse = parser(fieldwidths)
fields = parse(fwf)
fieldlist = list(fields)

#------------------------------------------
# writing list to a csv file
#------------------------------------------

with open('datachall.csv','w',newline='') as f:
    thewriter = csv.writer(f)
    thewriter.writerow(fieldlist)
