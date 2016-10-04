#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import math
from glob import glob
from optparse import OptionParser

print "Maldi2PCA - Prepares Maldi data for PCA: reduce & normalize TAB-delimited data files"
print "  Author:\tWim Fremout / Royal Institute for Cultural Heritage, Brussels, Belgium (4 Oct 2016)"
print "  Licence:\tGNU GPL version 3.0\n"

usage = "usage: %prog [options] INFILES"

parser = OptionParser(usage=usage, version="%prog 0.2")
parser.add_option("--nolimits", help="do not set X range", action="store_false", dest="FILT", default=True)
parser.add_option("--low", help="lower limit (default: 900)", action="store", type="int", dest="LOW", default=900)
parser.add_option("--high", help="higher limit (default: 2000)", action="store", type="int", dest="HIGH", default=2000)
parser.add_option("-n", help="normalize Y data, no normalization when zero (default: 999)", action="store", type="int", dest="NORM", default=999)
parser.add_option("-c", help="display columns (default: 15, 13 in case of -n0) \n 1-Xround\n 2-Xpeak\n 3-Ypeak\n 4-Ysum\n 5-Ypeak*\n 6-Ysum*\n 7-iterations", action="store", type="int", dest="COL", default="15")
parser.add_option("--headerless", help="do not display the table header", action="store_false", dest="HEADER", default=True)
parser.add_option("--comma", help="comma as digital separator", action="store_true", dest="COMMA", default=False)
parser.add_option("-o", help="output file", action="store", type="string", dest="OUTFILE")
parser.add_option("-v", "--verbose", help="be very verbose", action="store_true", dest="VERBOSE", default=False)
(options, args) = parser.parse_args()

if len(args) == 0:
  parser.error("incorrect number of arguments")

if options.FILT == False:	# set correct mass range
  options.LOW = 0
  options.HIGH = float('inf')
else: options.LOW = options.LOW -1
  
options.COL = str(options.COL)	# set correct columns
if (options.NORM == 0):
  options.COL = options.COL.replace("5","3")
  options.COL = options.COL.replace("6","4")

if options.COMMA == True:
  digsep = ","
else:
  digsep = "."

if options.VERBOSE:
  print "PARAMETERS"
  print "  mass range:", options.FILT
  print "    lower limit:", options.LOW
  print "    higher limit:", options.HIGH
  print "  normalization:", options.NORM
  print "  columns:", options.COL
  print "  header:", options.HEADER
  print "  digital separator:", digsep
  print "  OUTFILE:", options.OUTFILE
  print "  INFILES:", args, "\n"

### REDUCE DATA
# read sourcefile line by line
# ignore (near) zero mass values
# round the mass values (Xround)
# group equal rounded mass values
#   --> calculate Xsum, number of iterations
#   --> keep track of the exact mass (Xpeak) and peakheight (Ypeak) of the highest datapoint

#nfiles = len(args)	# number of files (as arguments) 
datapointindex = [0]	# keep track of the positions of the different files in our lists

xround = [0]
xpeak = [0]
ysum = [0]
ypeak = [0]
iterations = [0]
n=0

if options.VERBOSE: print "READING AND REDUCING THE DATASET..."

for z in args:
  sourcefile = open(z, 'r')
  if options.VERBOSE: print "  opening file:", z
  for line in sourcefile:
    line = line.strip()
    temp = line.split()
    xroundtemp = math.trunc(round(float(temp[0]),0))
    if xroundtemp <= options.LOW: pass
    elif xroundtemp > options.HIGH: break
    elif xroundtemp == xround[n]:
      # if the rounded x-value from this line is already in the table:
      #  --> add it to table[n] and don't increment n
      if options.COL.count("7") > 0: 
	iterations[n] = iterations[n] + 1
      if options.COL.count("4") + options.COL.count("6") > 0:
	ysum[n] = ysum[n] + round(float(temp[1]),0)
      if options.COL.count("2") + options.COL.count("3") + options.COL.count("5") > 0:
	ypeaktemp = round(float(temp[1]),0)
	if ypeaktemp > ypeak[n]:
	  ypeak[n] = ypeaktemp
	  if options.COL.count("2") > 0:
	    xpeak[n] = round(float(temp[0]),4)
      if options.VERBOSE: 
	print "    read line from " + z + ": ", line, " --> ADD"
    else:
      # if the rounded value from this line was not already in the table:
      #  --> add new line to table and increment n
      xround.append(xroundtemp)
      if options.COL.count("2") > 0: 
	xpeak.append(round(float(temp[0]),4))
      if options.COL.count("4") + options.COL.count("6") > 0:
	ysum.append(round(float(temp[1]),0))
      if options.COL.count("2") + options.COL.count("3") + options.COL.count("5") > 0: 
	ypeak.append(round(float(temp[1]),0))
      if options.COL.count("7") > 0:
	iterations.append(1)
      n = n + 1
      if options.VERBOSE:
	print "    read line from " + z + ": ", line, " --> NEW"
  
  # n => number of resulting datapoints for this file 
  if options.VERBOSE: print "  finished reading", z," (datapointindex", n, ")"
  datapointindex.append(n)
  sourcefile.close()

# finally some cleanup: the first things in the lists are useless zeros
xround.pop(0)
xpeak.pop(0)
ypeak.pop(0)
ysum.pop(0)
iterations.pop(0)


### NORMALIZE DATA
# two new columns containing the normalized peak heights
if options.NORM > 0:
  if options.VERBOSE: print "\n\nNORMALIZING..."
  ypeaknorm = []
  ysumnorm = []
  for z in range(0, len(datapointindex)-1):		#loop files
    if options.VERBOSE: print "  normalizing file", args[z]
    if options.COL.count("5") > 0:  
      vMax = max(ypeak[datapointindex[z]:datapointindex[z+1]])
      for x in ypeak[datapointindex[z]:datapointindex[z+1]]:
	ypeaknorm.append(round(x/(vMax*1.0)*options.NORM,0))
    if options.COL.count("6") > 0: 
      vMax = max(ysum[datapointindex[z]:datapointindex[z+1]])
      for x in ysum[datapointindex[z]:datapointindex[z+1]]:
	ysumnorm.append(round(x/(vMax*1.0)*options.NORM,0))


### OUTPUT
if options.VERBOSE: print "\n\nCREATING OUTPUT...\n"
if options.OUTFILE <> None: outfile = open(options.OUTFILE, 'w')

# shared X column; if as the first column, do not repeat this in case of several datafiles
if options.COL[0] == "1": 
  options.COL = options.COL.replace("1","",1)
  xcolumn = True
else: xcolumn = False

# header
if options.HEADER == True:
  # shared X column
  if xcolumn:
    headerline1 = "\t"
    headerline2 = "X\t"
  else: headerline1 = headerline2 = ""
  # the other columns
  for z in args:
    for y in range (0,len(options.COL)):	#loop columns
      if options.COL[y] == "1":
	headerline1 = headerline1 + z + "\t"
	headerline2 = headerline2 + "X\t"
      elif options.COL[y] == "2":
	headerline1 = headerline1 + z + "\t"
	headerline2 = headerline2 + "Xpeak\t"
      elif options.COL[y] == "3":
	headerline1 = headerline1 + z + "\t"
	headerline2 = headerline2 + "Ypeak\t"
      elif options.COL[y] == "4":
	headerline1 = headerline1 + z + "\t"
	headerline2 = headerline2 + "Ysum\t"
      elif options.COL[y] == "5":
	headerline1 = headerline1 + z + "\t"
	headerline2 = headerline2 + "Ypeak*\t"
      elif options.COL[y] == "6":
	headerline1 = headerline1 + z + "\t"
	headerline2 = headerline2 + "Ysum*\t"
      elif options.COL[y] == "7":
	headerline1 = headerline1 + z + "\t"
	headerline2 = headerline2 + "iterations\t"
  if options.OUTFILE <> None: outfile.write(headerline1 + "\n" + headerline2 + "\n")
  else: print headerline1 + "\n" + headerline2 



#table body
n=0
for x in range(min(xround), max(xround)+1):		#loop datapoints (rows)
  # shared X column
  if xcolumn:  outputline = str(x) + "\t"  
  else: outputline = ""
  # all the other columns, grouped by file
  for z in range(0,len(datapointindex)-1):		#loop files
    if xround[datapointindex[z]] == x:
      for y in range(0,len(options.COL)):		#loop columns
	if options.COL[y] == "1":
	  outputline = outputline + str(xround[datapointindex[z]]).replace(".",digsep) + "\t"
	elif options.COL[y] == "2":
	  outputline = outputline + str(xpeak[datapointindex[z]]).replace(".",digsep) + "\t"
	elif options.COL[y] == "3":
	  outputline = outputline + str(ypeak[datapointindex[z]]).replace(".",digsep) + "\t"
	elif options.COL[y] == "4":
	  outputline = outputline + str(ysum[datapointindex[z]]).replace(".",digsep) + "\t"
	elif options.COL[y] == "5":
	  outputline = outputline + str(ypeaknorm[datapointindex[z]]).replace(".",digsep) + "\t"
	elif options.COL[y] == "6":
	  outputline = outputline + str(ysumnorm[datapointindex[z]]).replace(".",digsep) + "\t"
	elif options.COL[y] == "7":
	  outputline = outputline + str(iterations[datapointindex[z]]) + "\t"
      #things to do afterwards: pop and decrease indices
      xround.pop(datapointindex[z])
      if options.COL.count("2") > 0: xpeak.pop(datapointindex[z])
      if options.COL.count("3") > 0: ypeak.pop(datapointindex[z])
      if options.COL.count("4") > 0: ysum.pop(datapointindex[z])
      if options.COL.count("5") > 0: ypeaknorm.pop(datapointindex[z])
      if options.COL.count("6") > 0: ysumnorm.pop(datapointindex[z])
      if options.COL.count("7") > 0: iterations.pop(datapointindex[z])
      for y in range(z + 1, len(datapointindex) - 1):
	datapointindex[y] = datapointindex[y] - 1
    else: 	#if the datapoint does not occur in the file, add tabs (empty fields in the table)
      for y in range(0,len(options.COL)): outputline = outputline + "\t"
  if options.OUTFILE <> None: outfile.write(outputline + "\n")
  else: print outputline 

outfile.close()
print "All done."


