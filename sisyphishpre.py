import math
import re
import sys
from pathlib import Path

# Zachary Frew
# LICENSE CC0 1.0 Universal
# This takes .thr files from https://github.com/jeffeb3/sandify and converts them to gcode for 'Sisyphish' - my kinetic art fish tank
# The compensation factor is equal to the motion of the linear axis for a given rotational movement
# For my setup, this is 46.7mm of movement for 360 degrees of rotation, and that's represented on line 49
# Make sure that your rotational axis is X and rho (linear) axis is Y
# Output assumes that X axis is in degrees and Y axis is in mm 
# USAGE: python thrtogco.py "input.thr" "output.gco"
# USAGE: Modify the below comp_factor variable for your machine. comp_factor must be set as the linear translation of your rho axis for 360 degrees of theta rotation

comp_factor = 46.7 #MODIFY
radius = 125

#make sure enough parameters are given 
if len(sys.argv) < 2:
	sys.exit("Error: Input and/or output filenames not provided")

#declare the input file and make sure that it exists
input_filename = Path(sys.argv[1])
if not input_filename.is_file():
	sys.exit("Error: The input file %s does not exist" % input_filename)

#specify the output filename
output_filename = Path(sys.argv[2])

#load the input file in read mode

f = open(input_filename, "r") #open the file
lines = [line.rstrip('\n') for line in f] #strip away newline characters

#create new list called splitline that contains only coordinate pairs
splitline = []
for x in lines: 
	if bool((re.search(r'#', x))) != True:
		splitline.append(x.split())

#convert the first thr values into degrees of rotation
i = 1 
while i < (len(splitline) - 1):
	#print(i)
	splitline[i][0] = float(splitline[i][0]) / math.pi * 180
	splitline[i][0] = round(splitline[i][0], 2)
	i += 1

#convert the second thr values into linear steps
j = 1
while j < (len(splitline) - 1): 
	#print(j)
	splitline[j][1] = (float(splitline[j][1]) * radius) + (float(splitline[j][0]) * (comp_factor / 360))
	splitline[j][1] = round(splitline[j][1], 2)
	j += 1

#concatenate X to the beginning of the first list subindex 
k = 1
while k < (len(splitline) - 1): 
	splitline[k][0] = "X" + str(splitline[k][0])
	k += 1

#concatenate "Y" to the beginning of the second list subindex
l = 1
while l < (len(splitline) - 1): 
	splitline[l][1] = "Y" + str(splitline[l][1])
	l += 1

#concatenate G01 to the beginning of each sublist
m = 1 
while m < (len(splitline) - 1): 
	splitline[m] = "G01 " + str(splitline[m])
	m += 1

splitline.insert(0, "G28 X Y") #make sure your axis are homed

#write to newfile
f = open(output_filename, "w")
for line in splitline: 
	#this line removes extraneous characters. It's a bit gross but easier to understand than a regex
	line = str(line).replace("[", "").replace("]", "").replace("'", "").replace(",", "")
	f.write(str(line) + '\n')

