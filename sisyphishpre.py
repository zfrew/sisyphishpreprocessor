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

#write to newfile
outfile = open(output_filename, "w")
outfile.write("G28 X Y\n") #make sure your axis are homed

for rawline in lines:
	# Remove everything up to the first comment char
	line = rawline.split("#")[0]
	# Get any elements left.
	elements = line.split()
	if len(elements) != 2:
		# wrong number of elements. Oops
		print("Wrong number of elements on line '{}'".format(line))
		continue
	(theta, rho) = elements
	
	angle = float(theta) / math.pi * 180.0
	linearSteps = float(rho) * radius) + angle * (comp_factor / 360)
	
	gcode_line = "G01 X{0.2f} Y{0.2f}\n".format(angle, linearSteps)
	
	#this line removes extraneous characters. It's a bit gross but easier to understand than a regex
	outfile.write(gcode_line.replace("[", "").replace("]", "").replace("'", "").replace(",", ""))
